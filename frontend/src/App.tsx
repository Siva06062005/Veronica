import { FormEvent, useEffect, useState } from 'react'
import { Activity, Cpu, Database, Mic, Power, Send, ShieldCheck, Terminal } from 'lucide-react'
import { api } from './services/api'
import type { SystemStatus, ToolResult, Activity as ActivityItem } from './types'
import { Orb } from './components/Orb'
import { Metric } from './components/Metric'

export default function App() {
  const [system,setSystem]=useState<SystemStatus | null>(null), [events,setEvents]=useState<ActivityItem[]>([]), [text,setText]=useState(''), [state,setState]=useState('idle'), [result,setResult]=useState<ToolResult | null>(null), [online,setOnline]=useState(false), [pending,setPending]=useState<string | null>(null)
  const refresh=async()=>{ try { const [health, sys, history]=await Promise.all([api.health(),api.system(),api.activity()]); setOnline(health.status==='online'); setSystem(sys); setEvents(history) } catch {setOnline(false)} }
  useEffect(()=>{refresh(); const timer=setInterval(refresh,5000); return()=>clearInterval(timer)},[])
  const submit=async(e?:FormEvent, confirmed=false)=>{ e?.preventDefault(); const request=pending ?? text.trim(); if(!request)return; setState('thinking'); const response=await api.command(request,confirmed); setResult(response); setState(response.success?'idle':'error'); if(response.error==='confirmation_required') setPending(request); else { setPending(null); setText('') }; refresh() }
  const metrics=system?.data
  return <main>
    <header><div className="brand"><span className="mark">V</span><div><h1>VERONICA</h1><p>PERSONAL AI OPERATING ASSISTANT</p></div></div><div className={online?'status online':'status'}><span/> {online?'SYSTEM ONLINE':'BACKEND OFFLINE'}</div></header>
    <section className="layout">
      <aside className="metrics"><div className="panel-title"><Cpu size={16}/> SYSTEM</div><Metric label="CPU" value={`${Math.round(metrics?.cpu_percent ?? 0)}%`}/><Metric label="MEMORY" value={`${Math.round(metrics?.memory_percent ?? 0)}%`}/><Metric label="DISK" value={`${Math.round(metrics?.disks?.[0]?.percent ?? 0)}%`}/><div className="host">HOST <b>{metrics?.hostname ?? '---'}</b></div></aside>
      <section className="core"><div className="eyebrow">VERONICA CORE</div><Orb state={state}/><div className="voice-state"><Mic size={16}/>{state==='thinking'?'Thinking...':state==='error'?'Attention required':'Ready for a request'}</div><div className="visualizer">{Array.from({length:28},(_,i)=><i key={i} style={{height:`${18+(i*13)%38}%`}}/>)}</div></section>
      <aside className="activity"><div className="panel-title"><Activity size={16}/> ACTIVITY</div><div className="event-list">{events.slice(0,6).map(event=><div className="event" key={event.id}><span className={event.success?'ok':'bad'}/><div><b>{event.tool ?? 'conversation'}</b><p>{event.result}</p></div></div>)}{!events.length&&<p className="muted">No activity yet.</p>}</div></aside>
    </section>
    <section className="console"><div className="result"><Terminal size={17}/><span>{result?.message ?? 'Veronica is connected and ready.'}</span>{result?.error&&<small>{result.error}</small>}</div>{pending&&<div className="confirm"><ShieldCheck size={18}/><span>This action requires your confirmation.</span><button onClick={()=>submit(undefined,true)}>Confirm</button><button className="quiet" onClick={()=>setPending(null)}>Cancel</button></div>}<form onSubmit={submit}><input value={text} onChange={e=>setText(e.target.value)} placeholder="Ask Veronica to check your PC, open an app, or inspect Docker..."/><button aria-label="Send request"><Send size={18}/></button></form></section>
    <footer><span><Database size={14}/> Local audit log enabled</span><button className="stop" onClick={()=>{setText('Stop Veronica');submit()}}><Power size={14}/> STOP VERONICA</button></footer>
  </main>
}
