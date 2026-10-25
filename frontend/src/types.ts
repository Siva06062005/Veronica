export type ToolResult = { success: boolean; tool: string; action: string; message: string; data: Record<string, unknown>; error: string | null }
export type SystemStatus = ToolResult & { data: { cpu_percent: number; memory_percent: number; disks: { device: string; percent: number }[]; hostname: string; uptime_seconds: number } }
export type Activity = { id: number; timestamp: string; user_request: string; tool: string | null; success: boolean; result: string; risk: string }
