from __future__ import annotations

from pathlib import Path
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")
    veronica_host: str = "127.0.0.1"
    veronica_port: int = 8765
    veronica_data_dir: Path = Path("data")
    ai_provider: str = "mock"
    ai_model: str = "gpt-4.1-mini"
    openai_api_key: str | None = None
    llm_base_url: str | None = None
    llm_api_key: str | None = None
    ollama_base_url: str = "http://127.0.0.1:11434"
    voice_provider: str = "none"
    stt_model: str | None = None
    tts_model: str | None = None
    veronica_wake_word: str = "veronica"
    veronica_automation_enabled: bool = True
    veronica_allowed_roots: str = ""

    @property
    def data_dir(self) -> Path:
        path = self.veronica_data_dir.resolve()
        path.mkdir(parents=True, exist_ok=True)
        return path

    @property
    def allowed_roots(self) -> list[Path]:
        roots = [Path(p.strip()).resolve() for p in self.veronica_allowed_roots.split(";") if p.strip()]
        return roots or [Path.home().resolve()]


settings = Settings()
