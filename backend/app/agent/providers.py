from __future__ import annotations

from abc import ABC, abstractmethod
import httpx
from app.config import settings


class AIProvider(ABC):
    @abstractmethod
    async def respond(self, prompt: str) -> str: ...


class MockProvider(AIProvider):
    async def respond(self, prompt: str) -> str:
        return "I can help with system health, approved developer tools, Docker, Git, applications, and stored preferences."


class OpenAIProvider(AIProvider):
    async def respond(self, prompt: str) -> str:
        if not settings.openai_api_key:
            return "OpenAI is selected but OPENAI_API_KEY is not configured."
        from openai import AsyncOpenAI
        client = AsyncOpenAI(api_key=settings.openai_api_key)
        response = await client.responses.create(model=settings.ai_model, input=prompt)
        return response.output_text


class OpenAICompatibleProvider(AIProvider):
    """Works with endpoints implementing the OpenAI chat-completions contract."""
    async def respond(self, prompt: str) -> str:
        if not settings.llm_base_url:
            return "An OpenAI-compatible provider is selected but LLM_BASE_URL is not configured."
        headers = {"Content-Type": "application/json"}
        if settings.llm_api_key:
            headers["Authorization"] = f"Bearer {settings.llm_api_key}"
        base = settings.llm_base_url.rstrip("/")
        endpoint = base if base.endswith("/chat/completions") else f"{base}/chat/completions"
        try:
            async with httpx.AsyncClient(timeout=45) as client:
                response = await client.post(endpoint, headers=headers, json={"model": settings.ai_model,
                    "messages": [{"role": "system", "content": "You are VERONICA, a concise Windows desktop assistant."},
                                 {"role": "user", "content": prompt}], "temperature": 0.3})
                response.raise_for_status()
                content = response.json()["choices"][0]["message"]["content"]
                return str(content).strip() or "The provider returned an empty response."
        except (httpx.HTTPError, KeyError, IndexError, TypeError) as exc:
            return f"The configured LLM endpoint could not respond: {exc}"


class OllamaProvider(AIProvider):
    async def respond(self, prompt: str) -> str:
        try:
            async with httpx.AsyncClient(timeout=45) as client:
                response = await client.post(f"{settings.ollama_base_url.rstrip('/')}/api/chat", json={"model": settings.ai_model,
                    "messages": [{"role": "system", "content": "You are VERONICA, a concise Windows desktop assistant."},
                                 {"role": "user", "content": prompt}], "stream": False})
                response.raise_for_status()
                content = response.json()["message"]["content"]
                return str(content).strip() or "Ollama returned an empty response."
        except (httpx.HTTPError, KeyError, TypeError) as exc:
            return f"Ollama could not respond. Confirm it is running and the model is installed: {exc}"


def get_provider() -> AIProvider:
    providers: dict[str, AIProvider] = {"openai": OpenAIProvider(), "ollama": OllamaProvider(),
                                        "openai_compatible": OpenAICompatibleProvider(), "mock": MockProvider()}
    return providers.get(settings.ai_provider.lower(), MockProvider())
