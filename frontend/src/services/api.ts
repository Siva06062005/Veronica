import type { Activity, SystemStatus, ToolResult } from '../types'
const BASE = 'http://127.0.0.1:8765'
async function get<T>(path: string): Promise<T> { const r = await fetch(`${BASE}${path}`); if (!r.ok) throw new Error(`Backend error ${r.status}`); return r.json() }
export const api = { health: () => get<{status:string; automation_enabled:boolean}>('/health'), system: () => get<SystemStatus>('/system/status'), activity: () => get<Activity[]>('/activity'), command: async (text:string, confirmed=false) => { const r=await fetch(`${BASE}/command`, {method:'POST', headers:{'Content-Type':'application/json'},body:JSON.stringify({text,confirmed})}); return r.json() as Promise<ToolResult> } }
