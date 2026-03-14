import { useState, useEffect, useRef, useCallback } from "react";

// ─── Inline styles as a constant ───────────────────────────────────────────
const CSS = `
  @import url('https://fonts.googleapis.com/css2?family=Share+Tech+Mono&family=Rajdhani:wght@400;500;600;700&family=Orbitron:wght@400;700;900&display=swap');
  :root {
    --bg:#020409;--surface:#070d18;--border:#0e2040;--accent:#00d4ff;
    --accent2:#00ff9d;--danger:#ff3b5c;--warn:#ffb830;--muted:#2a4060;
    --text:#c8dff5;--text-dim:#4a6a90;
  }
  .aegis-root *{box-sizing:border-box;margin:0;padding:0;}
  .aegis-root{background:var(--bg);color:var(--text);font-family:'Rajdhani',sans-serif;font-size:15px;min-height:100vh;overflow-x:hidden;position:relative;}
  .aegis-root::before{content:'';position:fixed;inset:0;background:repeating-linear-gradient(0deg,transparent,transparent 2px,rgba(0,212,255,.015) 2px,rgba(0,212,255,.015) 4px);pointer-events:none;z-index:999;}
  .aegis-root::after{content:'';position:fixed;inset:0;background-image:linear-gradient(rgba(0,212,255,.04) 1px,transparent 1px),linear-gradient(90deg,rgba(0,212,255,.04) 1px,transparent 1px);background-size:60px 60px;pointer-events:none;z-index:0;}
  @keyframes blink{0%,100%{opacity:1}50%{opacity:.3}}
  @keyframes shieldPulse{0%,100%{filter:drop-shadow(0 0 8px #00d4ff)}50%{filter:drop-shadow(0 0 20px #00d4ff) drop-shadow(0 0 40px #00ff9d)}}
  @keyframes threatPulse{0%,100%{box-shadow:none}50%{box-shadow:0 0 16px rgba(255,59,92,.4)}}
  @keyframes rowIn{from{opacity:0;transform:translateX(-8px)}to{opacity:1;transform:translateX(0)}}
  @keyframes confFill{from{width:0}}
  .aegis-header{position:sticky;top:0;z-index:100;display:flex;align-items:center;justify-content:space-between;padding:0 32px;height:64px;background:rgba(2,4,9,.92);border-bottom:1px solid var(--border);backdrop-filter:blur(12px);}
  .aegis-logo{font-family:'Orbitron',monospace;font-size:22px;font-weight:900;letter-spacing:6px;color:var(--accent);text-shadow:0 0 30px var(--accent);display:flex;align-items:center;gap:12px;}
  .logo-shield{width:32px;height:32px;background:linear-gradient(135deg,var(--accent),var(--accent2));clip-path:polygon(50% 0%,100% 25%,100% 75%,50% 100%,0% 75%,0% 25%);animation:shieldPulse 2s ease-in-out infinite;}
  .header-right{display:flex;align-items:center;gap:24px;}
  .nav-tabs{display:flex;gap:4px;}
  .nav-tab{padding:6px 16px;border:1px solid var(--muted);border-radius:2px;background:transparent;color:var(--text-dim);font-family:'Share Tech Mono',monospace;font-size:10px;letter-spacing:2px;cursor:pointer;transition:all .2s;text-transform:uppercase;}
  .nav-tab.active,.nav-tab:hover{border-color:var(--accent);color:var(--accent);background:rgba(0,212,255,.07);}
  .status-pill{display:flex;align-items:center;gap:8px;padding:6px 14px;border:1px solid var(--accent2);border-radius:2px;font-size:12px;letter-spacing:2px;color:var(--accent2);font-family:'Share Tech Mono',monospace;}
  .status-dot{width:8px;height:8px;border-radius:50%;background:var(--accent2);box-shadow:0 0 8px var(--accent2);animation:blink 1.2s ease infinite;}
  .clock{font-family:'Share Tech Mono',monospace;font-size:13px;color:var(--text-dim);letter-spacing:2px;}
  .threat-badge{padding:6px 14px;background:rgba(255,59,92,.12);border:1px solid var(--danger);border-radius:2px;font-size:12px;letter-spacing:2px;color:var(--danger);font-family:'Share Tech Mono',monospace;animation:threatPulse 2s ease infinite;}
  .aegis-main{position:relative;z-index:1;padding:28px 32px;display:flex;flex-direction:column;gap:24px;}
  .section-title{font-family:'Orbitron',monospace;font-size:11px;letter-spacing:4px;color:var(--text-dim);text-transform:uppercase;margin-bottom:16px;display:flex;align-items:center;gap:12px;}
  .section-title::after{content:'';flex:1;height:1px;background:linear-gradient(90deg,var(--border),transparent);}
  .metrics-row{display:grid;grid-template-columns:repeat(4,1fr);gap:16px;}
  .metric-card{background:var(--surface);border:1px solid var(--border);border-radius:4px;padding:22px 24px;position:relative;overflow:hidden;transition:border-color .3s,transform .3s;}
  .metric-card:hover{border-color:var(--accent);transform:translateY(-2px);}
  .metric-card::before{content:'';position:absolute;top:0;left:0;right:0;height:2px;background:linear-gradient(90deg,transparent,var(--accent),transparent);opacity:.6;}
  .metric-card.danger::before{background:linear-gradient(90deg,transparent,var(--danger),transparent);}
  .metric-card.warn::before{background:linear-gradient(90deg,transparent,var(--warn),transparent);}
  .metric-card.green::before{background:linear-gradient(90deg,transparent,var(--accent2),transparent);}
  .metric-label{font-size:11px;letter-spacing:3px;color:var(--text-dim);text-transform:uppercase;font-family:'Share Tech Mono',monospace;}
  .metric-value{font-family:'Orbitron',monospace;font-size:32px;font-weight:700;margin:8px 0 4px;color:var(--accent);}
  .metric-card.danger .metric-value{color:var(--danger);}
  .metric-card.warn .metric-value{color:var(--warn);}
  .metric-card.green .metric-value{color:var(--accent2);}
  .metric-delta{font-size:12px;letter-spacing:1px;color:var(--text-dim);}
  .metric-delta.up{color:var(--danger);}
  .metric-delta.down{color:var(--accent2);}
  .metric-icon{position:absolute;right:20px;top:50%;transform:translateY(-50%);font-size:40px;opacity:.06;}
  .two-col{display:grid;grid-template-columns:1fr 1fr;gap:24px;}
  .three-col{display:grid;grid-template-columns:2fr 1fr;gap:24px;}
  .panel{background:var(--surface);border:1px solid var(--border);border-radius:4px;padding:24px;position:relative;}
  .panel-corner{position:absolute;width:12px;height:12px;border-color:var(--accent);border-style:solid;}
  .panel-corner.tl{top:-1px;left:-1px;border-width:2px 0 0 2px;}
  .panel-corner.tr{top:-1px;right:-1px;border-width:2px 2px 0 0;}
  .panel-corner.bl{bottom:-1px;left:-1px;border-width:0 0 2px 2px;}
  .panel-corner.br{bottom:-1px;right:-1px;border-width:0 2px 2px 0;}
  .mode-tabs{display:flex;gap:6px;flex-wrap:wrap;margin-bottom:20px;}
  .tab{padding:7px 16px;border:1px solid var(--muted);border-radius:2px;background:transparent;color:var(--text-dim);font-family:'Share Tech Mono',monospace;font-size:11px;letter-spacing:2px;cursor:pointer;text-transform:uppercase;transition:all .2s;}
  .tab:hover,.tab.active{border-color:var(--accent);color:var(--accent);background:rgba(0,212,255,.07);box-shadow:0 0 12px rgba(0,212,255,.15);}
  .ai-box{border:1px solid var(--border);border-radius:3px;padding:16px;margin-bottom:12px;position:relative;}
  .ai-box-label{position:absolute;top:-10px;left:12px;background:var(--surface);padding:0 8px;font-size:10px;letter-spacing:3px;font-family:'Share Tech Mono',monospace;color:var(--text-dim);}
  .ai-box.detected{border-color:var(--danger);}
  .ai-box.detected .ai-box-label{color:var(--danger);}
  .ai-box.response{border-color:var(--warn);}
  .ai-box.response .ai-box-label{color:var(--warn);}
  .ai-box.explain{border-color:var(--accent2);}
  .ai-box.explain .ai-box-label{color:var(--accent2);}
  .ai-box p{font-size:13px;color:var(--text);line-height:1.6;}
  .conf-bar{height:4px;background:var(--muted);border-radius:2px;margin-top:10px;overflow:hidden;}
  .conf-fill{height:100%;border-radius:2px;background:linear-gradient(90deg,var(--danger),var(--warn));animation:confFill 1.2s cubic-bezier(.4,0,.2,1) both;}
  .ip-grid{display:grid;grid-template-columns:1fr 1fr;gap:10px;margin-top:12px;}
  .ip-cell{background:rgba(0,0,0,.4);border:1px solid var(--border);border-radius:3px;padding:12px;}
  .ip-cell-label{font-size:10px;letter-spacing:2px;color:var(--text-dim);font-family:'Share Tech Mono',monospace;}
  .ip-cell-val{font-family:'Orbitron',monospace;font-size:14px;color:var(--accent);margin-top:4px;}
  .speed-readout{background:rgba(0,0,0,.35);border:1px solid var(--border);border-radius:4px;padding:16px;}
  .speed-direction{font-family:'Share Tech Mono',monospace;font-size:11px;letter-spacing:3px;margin-bottom:6px;}
  .speed-big{font-family:'Orbitron',monospace;font-size:36px;font-weight:700;line-height:1;transition:color .3s;}
  .speed-unit{font-family:'Share Tech Mono',monospace;font-size:11px;letter-spacing:2px;color:var(--text-dim);margin-bottom:10px;}
  .speed-bar-wrap{height:4px;background:var(--muted);border-radius:2px;overflow:hidden;margin-bottom:8px;}
  .speed-bar{height:100%;border-radius:2px;transition:width .6s cubic-bezier(.4,0,.2,1);}
  .speed-sub{font-family:'Share Tech Mono',monospace;font-size:10px;letter-spacing:1px;color:var(--text-dim);}
  .speed-stat{background:rgba(0,0,0,.3);border:1px solid var(--border);border-radius:3px;padding:10px 12px;}
  .ss-label{font-family:'Share Tech Mono',monospace;font-size:9px;letter-spacing:2px;color:var(--text-dim);margin-bottom:4px;}
  .ss-val{font-family:'Orbitron',monospace;font-size:13px;font-weight:700;}
  .ntp-live-badge{font-family:'Share Tech Mono',monospace;font-size:10px;letter-spacing:2px;color:var(--accent2);border:1px solid var(--accent2);padding:4px 10px;border-radius:2px;display:flex;align-items:center;gap:6px;}
  .ntp-blink{animation:blink 1s infinite;}
  .ntp-summary{display:grid;grid-template-columns:repeat(4,1fr);gap:10px;margin-bottom:16px;}
  .ntp-sum-cell{background:rgba(0,0,0,.3);border:1px solid var(--border);border-radius:3px;padding:10px 12px;text-align:center;}
  .ntp-sum-label{font-family:'Share Tech Mono',monospace;font-size:9px;letter-spacing:2px;color:var(--text-dim);margin-bottom:4px;}
  .ntp-sum-val{font-family:'Orbitron',monospace;font-size:20px;font-weight:700;}
  .ntp-sum-val.accent2{color:var(--accent2);}
  .ntp-sum-val.warn{color:var(--warn);}
  .ntp-sum-val.danger{color:var(--danger);}
  .ntp-header-row{display:grid;grid-template-columns:120px 1fr 70px 100px 90px 90px;gap:8px;padding:6px 10px;background:rgba(0,212,255,.04);border:1px solid var(--border);border-radius:3px 3px 0 0;font-family:'Share Tech Mono',monospace;font-size:9px;letter-spacing:2px;color:var(--text-dim);text-transform:uppercase;margin-bottom:2px;}
  .ntp-feed{display:flex;flex-direction:column;gap:2px;max-height:240px;overflow-y:auto;}
  .ntp-feed::-webkit-scrollbar{width:3px;}
  .ntp-feed::-webkit-scrollbar-thumb{background:var(--muted);border-radius:2px;}
  .ntp-row{display:grid;grid-template-columns:120px 1fr 70px 100px 90px 90px;gap:8px;align-items:center;padding:8px 10px;border:1px solid transparent;border-radius:3px;font-family:'Share Tech Mono',monospace;font-size:11px;transition:background .2s;animation:rowIn .3s ease both;}
  .ntp-row:hover{background:rgba(0,212,255,.04);border-color:var(--border);}
  .ntp-status{padding:2px 7px;border-radius:2px;font-size:9px;letter-spacing:2px;text-align:center;white-space:nowrap;}
  .ntp-status.synced{background:rgba(0,255,157,.12);color:var(--accent2);border:1px solid var(--accent2);}
  .ntp-status.drifting{background:rgba(255,184,48,.12);color:var(--warn);border:1px solid var(--warn);}
  .ntp-status.offline{background:rgba(255,59,92,.12);color:var(--danger);border:1px solid var(--danger);}
  .offset-val.good{color:var(--accent2);}
  .offset-val.warn{color:var(--warn);}
  .offset-val.bad{color:var(--danger);}
  .log-filter{padding:4px 10px;border:1px solid var(--muted);border-radius:2px;background:transparent;color:var(--text-dim);font-family:'Share Tech Mono',monospace;font-size:9px;letter-spacing:2px;cursor:pointer;transition:all .2s;}
  .log-filter:hover,.log-filter.active{border-color:var(--accent);color:var(--accent);background:rgba(0,212,255,.07);}
  .log-header-row{display:grid;grid-template-columns:88px 90px 1fr 130px 130px 90px 90px 1fr;gap:8px;padding:7px 12px;background:rgba(0,212,255,.04);border:1px solid var(--border);border-radius:3px 3px 0 0;font-family:'Share Tech Mono',monospace;font-size:9px;letter-spacing:2px;color:var(--text-dim);text-transform:uppercase;margin-bottom:2px;}
  .log-feed{display:flex;flex-direction:column;gap:2px;max-height:420px;overflow-y:auto;}
  .log-feed::-webkit-scrollbar{width:3px;}
  .log-feed::-webkit-scrollbar-thumb{background:var(--muted);border-radius:2px;}
  .log-row{display:grid;grid-template-columns:88px 90px 1fr 130px 130px 90px 90px 1fr;gap:8px;align-items:center;padding:7px 12px;border:1px solid transparent;border-radius:3px;font-family:'Share Tech Mono',monospace;font-size:11px;transition:background .15s;animation:rowIn .25s ease both;}
  .log-row:hover{background:rgba(0,212,255,.03);border-color:rgba(0,212,255,.15);}
  .log-row.crit{border-left:2px solid rgba(255,59,92,.5);background:rgba(255,59,92,.02);}
  .log-row.warn{border-left:2px solid rgba(255,184,48,.4);background:rgba(255,184,48,.015);}
  .log-row.info{border-left:2px solid rgba(14,32,64,.9);}
  .sev{padding:3px 8px;border-radius:2px;font-size:10px;letter-spacing:2px;text-align:center;font-weight:600;}
  .sev.CRITICAL{background:rgba(255,59,92,.15);color:#d94f65;border:1px solid rgba(255,59,92,.5);}
  .sev.WARNING{background:rgba(255,184,48,.12);color:#c8962a;border:1px solid rgba(255,184,48,.45);}
  .sev.INFO{background:rgba(0,212,255,.1);color:#2a90a8;border:1px solid rgba(0,212,255,.35);}
  .action-pill{padding:2px 7px;border-radius:2px;font-size:9px;letter-spacing:1px;text-align:center;font-weight:600;}
  .action-pill.blocked{background:rgba(255,59,92,.12);color:#b84055;border:1px solid rgba(255,59,92,.4);}
  .action-pill.allowed{background:rgba(0,255,157,.1);color:#2a9968;border:1px solid rgba(0,255,157,.35);}
  .action-pill.monitor{background:rgba(255,184,48,.1);color:#b08030;border:1px solid rgba(255,184,48,.4);}
  .status-bar{display:flex;align-items:center;gap:32px;padding:14px 24px;background:var(--surface);border:1px solid var(--border);border-radius:4px;font-family:'Share Tech Mono',monospace;font-size:11px;color:var(--text-dim);letter-spacing:2px;}
  .status-item{display:flex;align-items:center;gap:8px;}
  .status-dot-sm{width:6px;height:6px;border-radius:50%;background:var(--accent2);box-shadow:0 0 6px var(--accent2);}
  .status-dot-sm.warn{background:var(--warn);box-shadow:0 0 6px var(--warn);}
  .req-btn{display:flex;align-items:center;gap:8px;padding:9px 12px;border-radius:3px;font-family:'Share Tech Mono',monospace;font-size:10px;letter-spacing:1.5px;text-transform:uppercase;cursor:pointer;transition:all .2s;width:100%;background:rgba(0,0,0,.3);}
  .req-btn.primary{border:1px solid rgba(0,212,255,.35);color:#2a8aaa;}
  .req-btn.primary:hover{background:rgba(0,212,255,.08);border-color:rgba(0,212,255,.6);color:#4ab0cc;}
  .req-btn.danger{border:1px solid rgba(255,59,92,.35);color:#904050;}
  .req-btn.danger:hover{background:rgba(255,59,92,.08);border-color:rgba(255,59,92,.6);color:#c05060;}
  .req-btn.warn{border:1px solid rgba(255,184,48,.35);color:#886830;}
  .req-btn.warn:hover{background:rgba(255,184,48,.08);border-color:rgba(255,184,48,.6);color:#b08840;}
  .req-btn.muted{border:1px solid rgba(42,64,96,.8);color:#3a5878;}
  .req-btn.muted:hover{background:rgba(0,212,255,.04);color:#4a7090;}
  .req-btn:active{transform:scale(.97);opacity:.85;}
  .unblock-page-btn{width:100%;padding:10px;border:1px solid rgba(0,212,255,.3);border-radius:3px;background:rgba(0,212,255,.05);color:#2a8aaa;font-family:'Share Tech Mono',monospace;font-size:10px;letter-spacing:2px;cursor:pointer;transition:all .2s;display:flex;align-items:center;justify-content:center;gap:8px;}
  .unblock-page-btn:hover{background:rgba(0,212,255,.1);border-color:rgba(0,212,255,.6);color:#4ab0cc;}
  .ubp-wrap{display:grid;grid-template-columns:280px 1fr 300px;gap:20px;padding:24px 32px;min-height:calc(100vh - 64px);}
  .alert-feed{display:flex;flex-direction:column;gap:6px;overflow-y:auto;max-height:calc(100vh - 260px);}
  .alert-feed::-webkit-scrollbar{width:3px;}
  .alert-feed::-webkit-scrollbar-thumb{background:var(--muted);border-radius:2px;}
  .alert-item{padding:10px 12px;border-radius:3px;border:1px solid transparent;font-family:'Share Tech Mono',monospace;font-size:10px;letter-spacing:.5px;animation:rowIn .3s ease both;cursor:default;transition:background .2s;}
  .alert-item:hover{background:rgba(0,212,255,.03);}
  .alert-item.crit{border-color:rgba(255,59,92,.25);background:rgba(255,59,92,.04);}
  .alert-item.warn{border-color:rgba(255,184,48,.2);background:rgba(255,184,48,.03);}
  .alert-item-hdr{display:flex;align-items:center;justify-content:space-between;margin-bottom:4px;}
  .agent-feed{display:flex;flex-direction:column;gap:8px;overflow-y:auto;max-height:calc(100vh - 280px);}
  .agent-feed::-webkit-scrollbar{width:3px;}
  .agent-feed::-webkit-scrollbar-thumb{background:var(--muted);border-radius:2px;}
  .agent-card{padding:12px 14px;border-radius:3px;border:1px solid var(--border);background:rgba(0,0,0,.25);animation:rowIn .3s ease both;transition:border-color .2s;}
  .agent-card:hover{border-color:rgba(0,212,255,.25);}
  .agent-card-top{display:flex;align-items:center;justify-content:space-between;margin-bottom:6px;}
  .agent-name{font-family:'Orbitron',monospace;font-size:11px;color:var(--text);letter-spacing:1px;}
  .agent-status-badge{padding:2px 8px;border-radius:2px;font-family:'Share Tech Mono',monospace;font-size:9px;letter-spacing:2px;}
  .agent-status-badge.online{background:rgba(0,255,157,.1);color:#2a9968;border:1px solid rgba(0,255,157,.3);}
  .agent-status-badge.busy{background:rgba(255,184,48,.1);color:#886830;border:1px solid rgba(255,184,48,.3);}
  .agent-status-badge.offline{background:rgba(255,59,92,.1);color:#904050;border:1px solid rgba(255,59,92,.3);}
  .agent-meta{font-family:'Share Tech Mono',monospace;font-size:9px;color:var(--text-dim);line-height:1.7;}
  .agent-bar-wrap{height:3px;background:var(--muted);border-radius:2px;margin-top:8px;overflow:hidden;}
  .agent-bar{height:100%;border-radius:2px;transition:width 1.2s ease;}
  .ubp-stat{background:rgba(0,0,0,.3);border-radius:3px;padding:10px;text-align:center;border:1px solid var(--border);}
  .ubp-stat.danger{border-color:rgba(255,59,92,.25);}
  .ubp-stat.warn{border-color:rgba(255,184,48,.25);}
  .ubp-stat.green{border-color:rgba(0,255,157,.2);}
  .ubp-stat-val{font-family:'Orbitron',monospace;font-size:22px;font-weight:700;}
  .ubp-stat.danger .ubp-stat-val{color:#904050;}
  .ubp-stat.warn .ubp-stat-val{color:#886830;}
  .ubp-stat.green .ubp-stat-val{color:#2a9968;}
  .ubp-stat-lbl{font-family:'Share Tech Mono',monospace;font-size:9px;letter-spacing:2px;color:var(--text-dim);margin-top:3px;}
  .ub-header{display:grid;grid-template-columns:70px 130px 1fr 80px 100px 80px 90px;gap:8px;padding:6px 12px;background:rgba(0,212,255,.03);border:1px solid var(--border);border-radius:3px 3px 0 0;font-family:'Share Tech Mono',monospace;font-size:9px;letter-spacing:2px;color:var(--text-dim);margin-bottom:2px;}
  .ub-list{display:flex;flex-direction:column;gap:2px;max-height:420px;overflow-y:auto;}
  .ub-list::-webkit-scrollbar{width:3px;}
  .ub-list::-webkit-scrollbar-thumb{background:var(--muted);border-radius:2px;}
  .ub-row{display:grid;grid-template-columns:70px 130px 1fr 80px 100px 80px 90px;gap:8px;align-items:center;padding:9px 12px;border:1px solid rgba(255,59,92,.15);border-left:2px solid rgba(255,59,92,.45);border-radius:3px;background:rgba(255,59,92,.03);font-family:'Share Tech Mono',monospace;font-size:11px;animation:rowIn .25s ease both;transition:background .15s;}
  .ub-row:hover{background:rgba(255,59,92,.06);}
  .ub-filter{padding:5px 10px;border:1px solid var(--muted);border-radius:2px;background:transparent;color:var(--text-dim);font-family:'Share Tech Mono',monospace;font-size:9px;letter-spacing:1.5px;cursor:pointer;transition:all .2s;text-transform:uppercase;}
  .ub-filter.active,.ub-filter:hover{border-color:var(--accent);color:var(--accent);background:rgba(0,212,255,.07);}
  .unblock-tag{padding:2px 7px;border-radius:2px;font-size:9px;letter-spacing:2px;background:rgba(255,59,92,.12);color:#904050;border:1px solid rgba(255,59,92,.35);}
  .unblock-btn{padding:4px 10px;border:1px solid rgba(0,255,157,.3);border-radius:2px;background:rgba(0,255,157,.06);color:#2a9968;font-family:'Share Tech Mono',monospace;font-size:9px;letter-spacing:2px;cursor:pointer;transition:all .2s;white-space:nowrap;}
  .unblock-btn:hover{background:rgba(0,255,157,.12);border-color:rgba(0,255,157,.6);color:#44bb88;}
  .unblock-input{flex:1;background:rgba(0,0,0,.4);border:1px solid var(--border);border-radius:3px;color:var(--text);font-family:'Share Tech Mono',monospace;font-size:11px;letter-spacing:1px;padding:8px 12px;outline:none;transition:border-color .2s;}
  .unblock-input::placeholder{color:var(--text-dim);}
  .unblock-input:focus{border-color:rgba(0,212,255,.4);}
  .unblock-submit-btn{padding:8px 14px;border:1px solid rgba(0,212,255,.35);border-radius:3px;background:rgba(0,212,255,.07);color:#2a8aaa;font-family:'Share Tech Mono',monospace;font-size:10px;letter-spacing:2px;cursor:pointer;transition:all .2s;white-space:nowrap;}
  .unblock-submit-btn:hover{background:rgba(0,212,255,.12);border-color:rgba(0,212,255,.6);color:#4ab0cc;}
`;

// ─── Helpers ────────────────────────────────────────────────────────────────
const rand = (a, b) => Math.floor(Math.random() * (b - a + 1)) + a;
const randFloat = (a, b) => (Math.random() * (b - a) + a);

const LOG_EVENTS = [
  {ev:'Brute Force Login',proto:'SSH',action:'blocked'},
  {ev:'Port Scan Detected',proto:'TCP',action:'monitor'},
  {ev:'DDoS Flood',proto:'UDP',action:'blocked'},
  {ev:'SQL Injection Attempt',proto:'HTTP',action:'blocked'},
  {ev:'Malware Beacon',proto:'DNS',action:'blocked'},
  {ev:'Credential Stuffing',proto:'HTTPS',action:'blocked'},
  {ev:'Lateral Movement',proto:'SMB',action:'monitor'},
  {ev:'Normal Web Traffic',proto:'HTTPS',action:'allowed'},
  {ev:'API Rate Limit',proto:'HTTP',action:'monitor'},
  {ev:'Suspicious Upload',proto:'FTP',action:'blocked'},
];
const DESTINATIONS = ['10.0.1.5','10.0.2.18','10.0.3.44','172.16.0.1','192.168.1.254','10.0.0.1'];
const NTP_HOSTNAMES = ['srv-web-01','srv-db-02','srv-api-03','wks-fin-07','wks-hr-12','srv-mail-04','srv-proxy-05','cam-lobby-01','cam-floor2-03','wks-dev-09','srv-auth-06','wks-exec-02','iot-hvac-01','wks-ops-15','srv-backup-08'];
const DONUT_LABELS = ['DDoS','Brute Force','Malware','Port Scan','Phishing'];
const DONUT_COLORS = ['#ff3b5c','#ffb830','#00d4ff','#00ff9d','#a78bfa'];
const ALERT_TYPES = [
  {type:'Brute Force Login',sev:'CRITICAL'},{type:'DDoS Flood Detected',sev:'CRITICAL'},
  {type:'SQL Injection Attempt',sev:'CRITICAL'},{type:'Port Scan Sweep',sev:'WARNING'},
  {type:'Anomalous DNS Query',sev:'WARNING'},{type:'Repeated Auth Failure',sev:'WARNING'},
  {type:'Lateral Movement',sev:'CRITICAL'},{type:'Malware Beacon',sev:'CRITICAL'},
];
const AGENTS_DATA = [
  {name:'SENTINEL-01',role:'Intrusion Detection',load:72,tasks:14},
  {name:'GUARDIAN-02',role:'Firewall Manager',load:48,tasks:8},
  {name:'ORACLE-03',role:'Log Analyzer',load:91,tasks:31},
  {name:'WARDEN-04',role:'ACL Controller',load:33,tasks:5},
  {name:'NEXUS-05',role:'Threat Intelligence',load:60,tasks:18},
  {name:'CIPHER-06',role:'Packet Inspector',load:85,tasks:22},
  {name:'AEGIS-07',role:'AI Threat Engine',load:55,tasks:11},
  {name:'RECON-08',role:'Port Monitor',load:20,tasks:3},
];

const makeLog = () => {
  const ev = LOG_EVENTS[rand(0,LOG_EVENTS.length-1)];
  const sev = ev.action==='blocked'?(Math.random()<.4?'CRITICAL':'WARNING'):'INFO';
  return {
    sev, t: new Date().toTimeString().slice(0,8),
    ev:ev.ev, ip:`${rand(1,223)}.${rand(0,255)}.${rand(0,255)}.${rand(1,254)}`,
    dest:DESTINATIONS[rand(0,DESTINATIONS.length-1)],
    proto:ev.proto, action:ev.action,
    details:[`Port ${rand(1024,65535)}`,`PID-${rand(1000,9999)}`,`Sig #${rand(100,999)}`,`Seq ${rand(10000,99999)}`,`Rule R-${rand(10,99)}`][rand(0,4)],
    id: Math.random()
  };
};

const makeNTPClients = () => NTP_HOSTNAMES.map((host,i) => ({
  ip:`10.${Math.floor(i/5)+1}.${Math.floor(i%5)+1}.${10+i*7}`,
  host, stratum:[1,2,2,3,3,3][rand(0,5)],
  offset:+(randFloat(-2,2)).toFixed(3),
  lastSync:rand(0,30),
  status:Math.random()<.75?'synced':Math.random()<.6?'drifting':'offline'
}));

const initBlocked = [
  {ip:'45.33.32.156',reason:'DDoS Flood',since:'02:14:08',attempts:847,duration:'3h 22m'},
  {ip:'192.168.4.201',reason:'Brute Force Login',since:'03:41:22',attempts:312,duration:'1h 55m'},
  {ip:'103.21.244.0',reason:'SQL Injection',since:'04:07:55',attempts:119,duration:'1h 28m'},
  {ip:'185.220.101.33',reason:'Malware Beacon',since:'04:55:10',attempts:64,duration:'0h 41m'},
  {ip:'66.249.66.1',reason:'Port Scan',since:'05:12:38',attempts:28,duration:'0h 23m'},
  {ip:'77.88.55.80',reason:'Credential Stuffing',since:'01:30:00',attempts:1203,duration:'4h 06m'},
  {ip:'94.102.49.190',reason:'DDoS Flood',since:'02:58:14',attempts:589,duration:'2h 37m'},
  {ip:'5.188.210.5',reason:'Port Scan',since:'05:44:01',attempts:17,duration:'0h 08m'},
];

// ─── Chart canvas component ──────────────────────────────────────────────────
function ChartCanvas({ id, height = 200, init, update, deps = [] }) {
  const canvasRef = useRef(null);
  const chartRef = useRef(null);

  useEffect(() => {
    if (!window.Chart) return;
    if (chartRef.current) chartRef.current.destroy();
    chartRef.current = init(canvasRef.current.getContext('2d'));
    return () => { if (chartRef.current) chartRef.current.destroy(); };
  }, []);

  useEffect(() => {
    if (chartRef.current && update) update(chartRef.current);
  }, deps);

  return <canvas ref={canvasRef} id={id} height={height} />;
}

// ─── DONUT CHART ─────────────────────────────────────────────────────────────
function DonutChart({ data }) {
  return (
    <ChartCanvas
      id="donutChart"
      height={220}
      init={(ctx) => new window.Chart(ctx, {
        type: 'doughnut',
        data: {
          labels: DONUT_LABELS,
          datasets: [{
            data: data,
            backgroundColor: DONUT_COLORS.map(c => c+'33'),
            borderColor: DONUT_COLORS,
            borderWidth: 2, hoverOffset: 8
          }]
        },
        options: {
          cutout:'68%',
          plugins:{ legend:{display:false}, tooltip:{callbacks:{label:ctx=>` ${ctx.label}: ${ctx.parsed} events`}} },
          animation:{duration:600}
        }
      })}
      update={(chart) => { chart.data.datasets[0].data = data; chart.update(); }}
      deps={[data]}
    />
  );
}

// ─── NET CHART ────────────────────────────────────────────────────────────────
function NetChart({ latency, errors, reqRate, duration }) {
  const len = latency.length;
  const labels = Array.from({length:len},(_,i)=>i);
  return (
    <ChartCanvas
      id="netChart"
      height={120}
      init={(ctx) => new window.Chart(ctx, {
        type:'line',
        data:{
          labels,
          datasets:[
            {label:'Latency (ms)',data:latency,borderColor:'#ffb830',backgroundColor:'rgba(255,184,48,.06)',tension:.4,borderWidth:2,pointRadius:0,fill:true},
            {label:'Error Ratio',data:errors,borderColor:'#ff3b5c',backgroundColor:'rgba(255,59,92,.06)',tension:.4,borderWidth:2,pointRadius:0,fill:true},
            {label:'Request Rate',data:reqRate,borderColor:'#00d4ff',backgroundColor:'rgba(0,212,255,.06)',tension:.4,borderWidth:2,pointRadius:0,fill:true},
            {label:'Conn Duration',data:duration,borderColor:'#00ff9d',backgroundColor:'rgba(0,255,157,.06)',tension:.4,borderWidth:2,pointRadius:0,fill:true},
          ]
        },
        options:{
          responsive:true,animation:{duration:300},
          scales:{x:{display:false},y:{grid:{color:'rgba(14,32,64,.8)'},ticks:{color:'#4a6a90',font:{family:'Share Tech Mono',size:10}}}},
          plugins:{legend:{labels:{color:'#4a6a90',font:{family:'Share Tech Mono',size:10},boxWidth:12}}}
        }
      })}
      update={(chart) => {
        chart.data.datasets[0].data = latency;
        chart.data.datasets[1].data = errors;
        chart.data.datasets[2].data = reqRate;
        chart.data.datasets[3].data = duration;
        chart.update('none');
      }}
      deps={[latency, errors, reqRate, duration]}
    />
  );
}

// ─── SPEED CHART ──────────────────────────────────────────────────────────────
function SpeedChart({ upHistory, dnHistory }) {
  return (
    <ChartCanvas
      id="speedChart"
      height={140}
      init={(ctx) => new window.Chart(ctx, {
        type:'line',
        data:{
          labels: Array(upHistory.length).fill(''),
          datasets:[
            {label:'Send (Mbps)',data:upHistory,borderColor:'#00ff9d',backgroundColor:'rgba(0,255,157,.08)',borderWidth:2,pointRadius:0,tension:.35,fill:true},
            {label:'Receive (Mbps)',data:dnHistory,borderColor:'#00d4ff',backgroundColor:'rgba(0,212,255,.08)',borderWidth:2,pointRadius:0,tension:.35,fill:true},
          ]
        },
        options:{
          responsive:true,animation:{duration:0},
          scales:{x:{display:false},y:{min:0,max:150,grid:{color:'rgba(14,32,64,.7)'},ticks:{color:'#4a6a90',font:{family:'Share Tech Mono',size:10},callback:v=>v+'M'}}},
          plugins:{legend:{labels:{color:'#4a6a90',font:{family:'Share Tech Mono',size:10},boxWidth:10}}}
        }
      })}
      update={(chart) => {
        chart.data.datasets[0].data = upHistory;
        chart.data.datasets[1].data = dnHistory;
        chart.update('none');
      }}
      deps={[upHistory, dnHistory]}
    />
  );
}

// ─── OFFSET CHART ─────────────────────────────────────────────────────────────
function OffsetChart({ ntpClients }) {
  const buckets = ['<-8','-8:-4','-4:-2','-2:0','0:2','2:4','4:8','>8'];
  const getDistData = (clients) => {
    const b = Array(8).fill(0);
    clients.forEach(c => {
      const o = c.offset;
      if(o<-8)b[0]++;else if(o<-4)b[1]++;else if(o<-2)b[2]++;else if(o<0)b[3]++;
      else if(o<2)b[4]++;else if(o<4)b[5]++;else if(o<8)b[6]++;else b[7]++;
    });
    return b;
  };
  return (
    <ChartCanvas
      id="offsetChart"
      height={60}
      init={(ctx) => new window.Chart(ctx, {
        type:'bar',
        data:{
          labels: buckets,
          datasets:[{
            data: getDistData(ntpClients),
            backgroundColor: buckets.map((_,i)=>i===3||i===4?'rgba(0,255,157,.5)':i===2||i===5?'rgba(255,184,48,.5)':'rgba(255,59,92,.5)'),
            borderColor: buckets.map((_,i)=>i===3||i===4?'#00ff9d':i===2||i===5?'#ffb830':'#ff3b5c'),
            borderWidth:1,borderRadius:2
          }]
        },
        options:{
          responsive:true,animation:{duration:400},
          scales:{x:{grid:{display:false},ticks:{color:'#4a6a90',font:{family:'Share Tech Mono',size:8}}},y:{grid:{color:'rgba(14,32,64,.7)'},ticks:{color:'#4a6a90',font:{family:'Share Tech Mono',size:9},stepSize:1}}},
          plugins:{legend:{display:false}}
        }
      })}
      update={(chart) => { chart.data.datasets[0].data = getDistData(ntpClients); chart.update(); }}
      deps={[ntpClients]}
    />
  );
}

// ─── SCRIPT LOADER ────────────────────────────────────────────────────────────
function useChartJS(cb) {
  const [ready, setReady] = useState(!!window.Chart);
  useEffect(() => {
    if (window.Chart) { setReady(true); return; }
    const s = document.createElement('script');
    s.src = 'https://cdnjs.cloudflare.com/ajax/libs/Chart.js/4.4.1/chart.umd.min.js';
    s.onload = () => setReady(true);
    document.head.appendChild(s);
  }, []);
  return ready;
}

// ─── DASHBOARD PAGE ───────────────────────────────────────────────────────────
function DashboardPage({ onNavigate }) {
  const chartReady = useChartJS();
  const [clock, setClock] = useState('');
  const [mode, setMode] = useState('All Traffic');
  const [conf, setConf] = useState(89);
  const [metrics, setMetrics] = useState({alerts:18,ips:47,events:13,load:62,ip:'192.168.1.78',attempts:341});
  const [donutData, setDonutData] = useState(DONUT_LABELS.map(()=>rand(5,40)));
  const [netData, setNetData] = useState({latency:Array.from({length:40},()=>rand(10,80)),errors:Array.from({length:40},()=>+Math.random().toFixed(2)),reqRate:Array.from({length:40},()=>+(Math.random()*3).toFixed(2)),duration:Array.from({length:40},()=>rand(1,15))});
  const [speeds, setSpeeds] = useState({upH:Array(60).fill(0),dnH:Array(60).fill(0),upVal:0,dnVal:0,totalUp:0,totalDn:0,peakUp:0,peakDn:0,avgUp:0,avgDn:0});
  const [ntpClients, setNtpClients] = useState(makeNTPClients);
  const [logs, setLogs] = useState(() => Array.from({length:30},makeLog));
  const [logFilter, setLogFilter] = useState('ALL');
  const [reqStatus, setReqStatus] = useState(null);

  // Clock
  useEffect(() => {
    const t = setInterval(() => setClock(new Date().toTimeString().slice(0,8)+' UTC'), 1000);
    setClock(new Date().toTimeString().slice(0,8)+' UTC');
    return () => clearInterval(t);
  }, []);

  // Metrics flicker
  useEffect(() => {
    const t = setInterval(() => setMetrics({
      alerts:rand(10,30),ips:rand(20,70),events:rand(5,20),load:rand(30,80),
      ip:`192.168.${rand(0,5)}.${rand(1,254)}`,attempts:rand(100,999)
    }), 4000);
    return () => clearInterval(t);
  }, []);

  // Donut refresh
  useEffect(() => {
    const t = setInterval(() => setDonutData(DONUT_LABELS.map(()=>rand(5,40))), 5000);
    return () => clearInterval(t);
  }, []);

  // Network chart scroll
  useEffect(() => {
    const t = setInterval(() => {
      setNetData(prev => {
        const lat=[...prev.latency]; lat.shift(); lat.push(rand(10,80));
        const err=[...prev.errors]; err.shift(); err.push(+Math.random().toFixed(2));
        const req=[...prev.reqRate]; req.shift(); req.push(+(Math.random()*3).toFixed(2));
        const dur=[...prev.duration]; dur.shift(); dur.push(rand(1,15));
        return {latency:lat,errors:err,reqRate:req,duration:dur};
      });
    }, 1500);
    return () => clearInterval(t);
  }, []);

  // Speed ticker
  useEffect(() => {
    let upBase=40, dnBase=70;
    const t = setInterval(() => {
      setSpeeds(prev => {
        const up = Math.max(0.5, Math.min(150, upBase + (Math.random()-.5)*18));
        const dn = Math.max(0.5, Math.min(150, dnBase + (Math.random()-.5)*18));
        upBase=up; dnBase=dn;
        const upH=[...prev.upH]; upH.shift(); upH.push(up);
        const dnH=[...prev.dnH]; dnH.shift(); dnH.push(dn);
        const totalUp = prev.totalUp + (up*1e6)/8/1e9/7200;
        const totalDn = prev.totalDn + (dn*1e6)/8/1e9/7200;
        const peakUp = Math.max(prev.peakUp, up);
        const peakDn = Math.max(prev.peakDn, dn);
        const avgUp = upH.reduce((a,b)=>a+b,0)/upH.filter(v=>v>0).length||0;
        const avgDn = dnH.reduce((a,b)=>a+b,0)/dnH.filter(v=>v>0).length||0;
        return {upH,dnH,upVal:up,dnVal:dn,totalUp,totalDn,peakUp,peakDn,avgUp,avgDn};
      });
    }, 500);
    return () => clearInterval(t);
  }, []);

  // NTP refresh
  useEffect(() => {
    const t = setInterval(() => {
      setNtpClients(prev => prev.map(c => {
        if (Math.random() < .25) {
          let offset = +(c.offset + (Math.random()-.5)*0.8).toFixed(3);
          offset = Math.max(-15, Math.min(15, offset));
          let lastSync = Math.max(0, c.lastSync + rand(0,2));
          let status = lastSync>120?'offline':Math.abs(offset)>8?'drifting':'synced';
          if (Math.random()<.05 && status==='offline') { lastSync=0; status='synced'; }
          return {...c, offset, lastSync, status};
        }
        return c;
      }));
    }, 3000);
    return () => clearInterval(t);
  }, []);

  // Log ticker
  useEffect(() => {
    const t = setInterval(() => {
      setLogs(prev => {
        const l = makeLog();
        return [l, ...prev].slice(0, 80);
      });
    }, 1200);
    return () => clearInterval(t);
  }, []);

  const filteredLogs = logFilter === 'ALL' ? logs : logs.filter(l => l.sev === logFilter);
  const displayLogs = filteredLogs.slice(0, 30);

  const handleMode = (m) => {
    setMode(m);
    const c = rand(80,95);
    setConf(c);
  };

  const showReqStatus = (msg, type) => {
    setReqStatus({msg, type});
    setTimeout(() => setReqStatus(null), 5000);
  };

  const handleRequest = (type) => {
    if (type==='investigation') {
      showReqStatus(`◈ Ticket INC-${rand(1000,9999)} opened — navigating to Manager…`, 'primary');
      setTimeout(() => onNavigate('unblock'), 800);
    } else if (type==='report') {
      showReqStatus(`◈ Generating report… navigating to Manager.`, 'warn');
      setTimeout(() => onNavigate('unblock'), 800);
    } else if (type==='lockdown') {
      showReqStatus('⊗ LOCKDOWN INITIATED — Perimeter ACLs enforced.', 'danger');
    } else if (type==='escalate') {
      showReqStatus('▲ ESCALATED TO SOC — Priority 1 alert raised.', 'muted');
    }
  };

  const reqStatusStyles = {
    primary:{bg:'rgba(0,212,255,.1)',border:'rgba(0,212,255,.35)',color:'#2a8aaa'},
    warn:{bg:'rgba(255,184,48,.1)',border:'rgba(255,184,48,.35)',color:'#886830'},
    danger:{bg:'rgba(255,59,92,.1)',border:'rgba(255,59,92,.35)',color:'#904050'},
    muted:{bg:'rgba(0,212,255,.07)',border:'rgba(42,64,96,.8)',color:'#3a5878'},
  };

  return (
    <main className="aegis-main">
      {/* METRICS */}
      <div>
        <div className="section-title">OPERATIONAL METRICS</div>
        <div className="metrics-row">
          <div className="metric-card danger">
            <div className="metric-icon">⚠</div>
            <div className="metric-label">Active Alerts</div>
            <div className="metric-value">{metrics.alerts}</div>
            <div className="metric-delta up">↑ +12% vs last hour</div>
          </div>
          <div className="metric-card warn">
            <div className="metric-icon">🚫</div>
            <div className="metric-label">Blocked IPs</div>
            <div className="metric-value">{metrics.ips}</div>
            <div className="metric-delta up">↑ +8 in last 5 min</div>
          </div>
          <div className="metric-card">
            <div className="metric-icon">◉</div>
            <div className="metric-label">Anomalous Events</div>
            <div className="metric-value">{metrics.events}</div>
            <div className="metric-delta down">↓ −3% vs baseline</div>
          </div>
          <div className="metric-card green">
            <div className="metric-icon">≋</div>
            <div className="metric-label">Network Load</div>
            <div className="metric-value">{metrics.load}%</div>
            <div className="metric-delta">Stable — normal range</div>
          </div>
        </div>
      </div>

      {/* AI + DONUT */}
      <div className="three-col">
        <div className="panel">
          <div className="panel-corner tl"/><div className="panel-corner tr"/>
          <div className="panel-corner bl"/><div className="panel-corner br"/>
          <div className="section-title">AI THREAT ENGINE</div>
          <div className="mode-tabs">
            {['All Traffic','Login Attack','Network Attack','Port Scan','Malware Activity'].map(m => (
              <button key={m} className={`tab${mode===m?' active':''}`} onClick={()=>handleMode(m)}>{m}</button>
            ))}
          </div>
          <div className="ai-box detected">
            <span className="ai-box-label">THREAT DETECTED</span>
            <p>Attack Type: <strong style={{color:'var(--danger)'}}>{mode}</strong></p>
            <p style={{marginTop:6}}>Confidence: <strong style={{color:'var(--warn)'}}>{conf}%</strong></p>
            <div className="conf-bar"><div className="conf-fill" style={{width:`${conf}%`}}/></div>
          </div>
          <div className="ai-box response">
            <span className="ai-box-label">AUTOMATED RESPONSE</span>
            <p>IP automatically blocked — ACL rule applied at perimeter firewall. Admin notified via SIEM alert <strong style={{color:'var(--warn)'}}>#7841</strong>.</p>
          </div>
          <div className="ai-box explain">
            <span className="ai-box-label">AI EXPLANATION</span>
            <p>Detected statistically anomalous request pattern: 340 req/s from single source, deviation 6.2σ above baseline. Matching known DDoS signature <strong style={{color:'var(--accent2)'}}>CVE-2024-3182</strong>.</p>
          </div>
          <div className="ip-grid">
            <div className="ip-cell"><div className="ip-cell-label">THREAT IP</div><div className="ip-cell-val">{metrics.ip}</div></div>
            <div className="ip-cell"><div className="ip-cell-label">GEO ORIGIN</div><div className="ip-cell-val">UNKNOWN</div></div>
            <div className="ip-cell"><div className="ip-cell-label">FIRST SEEN</div><div className="ip-cell-val">04:17:22</div></div>
            <div className="ip-cell"><div className="ip-cell-label">ATTEMPTS</div><div className="ip-cell-val">{metrics.attempts}</div></div>
          </div>
          <div style={{marginTop:16,borderTop:'1px solid var(--border)',paddingTop:16}}>
            <button className="unblock-page-btn" onClick={()=>onNavigate('unblock')}>
              <span>⊘</span> Open IP Unblock Manager
            </button>
          </div>
        </div>

        <div className="panel">
          <div className="panel-corner tl"/><div className="panel-corner tr"/>
          <div className="panel-corner bl"/><div className="panel-corner br"/>
          <div className="section-title">THREAT DISTRIBUTION</div>
          {chartReady && <DonutChart data={donutData}/>}
          <div style={{display:'flex',flexWrap:'wrap',gap:10,marginTop:16}}>
            {DONUT_LABELS.map((l,i) => (
              <div key={l} style={{display:'flex',alignItems:'center',gap:6,fontSize:11,fontFamily:'Share Tech Mono',color:DONUT_COLORS[i],letterSpacing:1}}>
                <div style={{width:8,height:8,borderRadius:1,background:DONUT_COLORS[i]}}/>
                {l}
              </div>
            ))}
          </div>
          <div style={{marginTop:20,borderTop:'1px solid var(--border)',paddingTop:16}}>
            <div style={{fontFamily:'Share Tech Mono',fontSize:9,letterSpacing:3,color:'var(--text-dim)',marginBottom:10}}>INCIDENT RESPONSE</div>
            <div style={{display:'grid',gridTemplateColumns:'1fr 1fr',gap:8}}>
              <button className="req-btn primary" onClick={()=>handleRequest('investigation')}><span>⚑</span><span>Request Investigation</span></button>
              <button className="req-btn danger" onClick={()=>handleRequest('lockdown')}><span>⊗</span><span>Force Lockdown</span></button>
              <button className="req-btn warn" onClick={()=>handleRequest('report')}><span>◈</span><span>Generate Report</span></button>
              <button className="req-btn muted" onClick={()=>handleRequest('escalate')}><span>▲</span><span>Escalate to SOC</span></button>
            </div>
            {reqStatus && (
              <div style={{marginTop:10,padding:'8px 12px',borderRadius:3,fontFamily:'Share Tech Mono',fontSize:10,letterSpacing:1,background:reqStatusStyles[reqStatus.type].bg,border:`1px solid ${reqStatusStyles[reqStatus.type].border}`,color:reqStatusStyles[reqStatus.type].color}}>
                {reqStatus.msg}
              </div>
            )}
          </div>
        </div>
      </div>

      {/* NET CHART */}
      <div className="panel">
        <div className="panel-corner tl"/><div className="panel-corner tr"/>
        <div className="panel-corner bl"/><div className="panel-corner br"/>
        <div className="section-title">NETWORK PERFORMANCE</div>
        {chartReady && <NetChart {...netData}/>}
      </div>

      {/* SPEED + NTP */}
      <div className="two-col">
        <div className="panel">
          <div className="panel-corner tl"/><div className="panel-corner tr"/>
          <div className="panel-corner bl"/><div className="panel-corner br"/>
          <div className="section-title">LIVE DATA THROUGHPUT</div>
          <div style={{display:'grid',gridTemplateColumns:'1fr 1fr',gap:16,marginBottom:20}}>
            <div className="speed-readout">
              <div className="speed-direction" style={{color:'var(--accent2)'}}>▲ SEND</div>
              <div className="speed-big" style={{color:speeds.upVal>120?'var(--danger)':'var(--accent2)'}}>{speeds.upVal.toFixed(2)}</div>
              <div className="speed-unit">Mbps</div>
              <div className="speed-bar-wrap"><div className="speed-bar" style={{background:'var(--accent2)',width:`${speeds.upVal/150*100}%`}}/></div>
              <div className="speed-sub">Total: {speeds.totalUp.toFixed(3)} GB</div>
            </div>
            <div className="speed-readout">
              <div className="speed-direction" style={{color:'var(--accent)'}}>▼ RECEIVE</div>
              <div className="speed-big" style={{color:speeds.dnVal>130?'var(--danger)':'var(--accent)'}}>{speeds.dnVal.toFixed(2)}</div>
              <div className="speed-unit">Mbps</div>
              <div className="speed-bar-wrap"><div className="speed-bar" style={{background:'var(--accent)',width:`${speeds.dnVal/150*100}%`}}/></div>
              <div className="speed-sub">Total: {speeds.totalDn.toFixed(3)} GB</div>
            </div>
          </div>
          {chartReady && <SpeedChart upHistory={speeds.upH} dnHistory={speeds.dnH}/>}
          <div style={{display:'grid',gridTemplateColumns:'repeat(4,1fr)',gap:10,marginTop:16}}>
            <div className="speed-stat"><div className="ss-label">PEAK ▲</div><div className="ss-val" style={{color:'var(--accent2)'}}>{speeds.peakUp.toFixed(1)} M</div></div>
            <div className="speed-stat"><div className="ss-label">AVG ▲</div><div className="ss-val" style={{color:'var(--accent2)'}}>{speeds.avgUp.toFixed(1)} M</div></div>
            <div className="speed-stat"><div className="ss-label">PEAK ▼</div><div className="ss-val" style={{color:'var(--accent)'}}>{speeds.peakDn.toFixed(1)} M</div></div>
            <div className="speed-stat"><div className="ss-label">AVG ▼</div><div className="ss-val" style={{color:'var(--accent)'}}>{speeds.avgDn.toFixed(1)} M</div></div>
          </div>
        </div>

        <div className="panel">
          <div className="panel-corner tl"/><div className="panel-corner tr"/>
          <div className="panel-corner bl"/><div className="panel-corner br"/>
          <div style={{display:'flex',alignItems:'center',justifyContent:'space-between',marginBottom:16}}>
            <div className="section-title" style={{marginBottom:0,flex:1}}>ACTIVE TIME SERVER CLIENTS</div>
            <div className="ntp-live-badge"><span className="ntp-blink">●</span> NTP SYNC</div>
          </div>
          <div className="ntp-summary">
            {[
              {label:'TOTAL CLIENTS',val:ntpClients.length,cls:'accent2'},
              {label:'SYNCED',val:ntpClients.filter(c=>c.status==='synced').length,cls:'accent2'},
              {label:'DRIFTING',val:ntpClients.filter(c=>c.status==='drifting').length,cls:'warn'},
              {label:'OFFLINE',val:ntpClients.filter(c=>c.status==='offline').length,cls:'danger'},
            ].map(s => (
              <div key={s.label} className="ntp-sum-cell">
                <div className="ntp-sum-label">{s.label}</div>
                <div className={`ntp-sum-val ${s.cls}`}>{s.val}</div>
              </div>
            ))}
          </div>
          <div className="ntp-header-row">
            <span>CLIENT IP</span><span>HOSTNAME</span><span>STRATUM</span>
            <span>OFFSET (ms)</span><span>LAST SYNC</span><span>STATUS</span>
          </div>
          <div className="ntp-feed">
            {ntpClients.map((c,i) => {
              const offClass = Math.abs(c.offset)<2?'good':Math.abs(c.offset)<8?'warn':'bad';
              const syncStr = c.lastSync<60?c.lastSync+'s ago':Math.floor(c.lastSync/60)+'m ago';
              return (
                <div key={i} className="ntp-row">
                  <span style={{color:'var(--accent)'}}>{c.ip}</span>
                  <span style={{color:'var(--text)'}}>{c.host}</span>
                  <span style={{color:'var(--text-dim)',textAlign:'center'}}>{c.stratum}</span>
                  <span className={`offset-val ${offClass}`}>{c.offset>0?'+':''}{c.offset.toFixed(3)}</span>
                  <span style={{color:'var(--text-dim)'}}>{syncStr}</span>
                  <span className={`ntp-status ${c.status}`}>{c.status.toUpperCase()}</span>
                </div>
              );
            })}
          </div>
          <div style={{marginTop:16}}>
            <div style={{fontFamily:'Share Tech Mono',fontSize:9,letterSpacing:2,color:'var(--text-dim)',marginBottom:8}}>OFFSET DISTRIBUTION</div>
            {chartReady && <OffsetChart ntpClients={ntpClients}/>}
          </div>
        </div>
      </div>

      {/* LOGS */}
      <div className="panel">
        <div className="panel-corner tl"/><div className="panel-corner tr"/>
        <div className="panel-corner bl"/><div className="panel-corner br"/>
        <div style={{display:'flex',alignItems:'center',justifyContent:'space-between',marginBottom:16}}>
          <div className="section-title" style={{marginBottom:0,flex:1}}>LIVE SECURITY EVENT LOG</div>
          <div style={{display:'flex',gap:8,alignItems:'center'}}>
            <span style={{fontFamily:'Share Tech Mono',fontSize:10,letterSpacing:2,color:'var(--text-dim)'}}>FILTER:</span>
            {['ALL','CRITICAL','WARNING','INFO'].map(f => (
              <button key={f} className={`log-filter${logFilter===f?' active':''}`} onClick={()=>setLogFilter(f)}>{f}</button>
            ))}
          </div>
        </div>
        <div className="log-header-row">
          <span>SEVERITY</span><span>TIMESTAMP</span><span>EVENT TYPE</span>
          <span>SOURCE IP</span><span>DESTINATION</span><span>PROTOCOL</span>
          <span>ACTION</span><span>DETAILS</span>
        </div>
        <div className="log-feed">
          {displayLogs.map((l) => {
            const sevClass = l.sev==='CRITICAL'?'crit':l.sev==='WARNING'?'warn':'info';
            const evColor = l.sev==='CRITICAL'?'#b85060':l.sev==='WARNING'?'#a87830':'#7aaec8';
            const ipColor = l.sev==='CRITICAL'?'#a84050':l.sev==='WARNING'?'#9a7228':'#2a7a96';
            const actionCls = l.action==='blocked'?'blocked':l.action==='allowed'?'allowed':'monitor';
            return (
              <div key={l.id} className={`log-row ${sevClass}`}>
                <span className={`sev ${l.sev}`}>{l.sev}</span>
                <span style={{color:'#5a8ab0',letterSpacing:1}}>{l.t}</span>
                <span style={{color:evColor,fontWeight:600}}>{l.ev}</span>
                <span style={{color:ipColor,fontWeight:700}}>{l.ip}</span>
                <span style={{color:'#4a7090'}}>{l.dest}</span>
                <span style={{color:'#00b8d9',letterSpacing:1}}>{l.proto}</span>
                <span className={`action-pill ${actionCls}`}>{l.action.toUpperCase()}</span>
                <span style={{color:'#3a6080'}}>{l.details}</span>
              </div>
            );
          })}
        </div>
      </div>

      {/* STATUS BAR */}
      <div className="status-bar">
        <div className="status-item"><div className="status-dot-sm"/>AEGIS ENGINE ONLINE</div>
        <div className="status-item"><div className="status-dot-sm"/>LOG PROCESSOR ACTIVE</div>
        <div className="status-item"><div className="status-dot-sm warn"/>3 AGENTS ELEVATED</div>
        <div className="status-item"><div className="status-dot-sm"/>SOC DASHBOARD SYNCED</div>
        <div style={{marginLeft:'auto',color:'var(--text-dim)'}}>v3.1.4 — CLASSIFIED</div>
      </div>
    </main>
  );
}

// ─── UNBLOCK PAGE ─────────────────────────────────────────────────────────────
function UnblockPage() {
  const [blockedIPs, setBlockedIPs] = useState(initBlocked.map(e=>({...e})));
  const [ubFilter, setUbFilter] = useState('ALL');
  const [inputVal, setInputVal] = useState('');
  const [ubStatus, setUbStatus] = useState(null);
  const [agents, setAgents] = useState(AGENTS_DATA.map(a=>({...a,status:a.load>80?'busy':a.load<10?'offline':'online'})));
  const [alerts] = useState(() => Array.from({length:18},()=>{const a=ALERT_TYPES[rand(0,ALERT_TYPES.length-1)];return{type:a.type,sev:a.sev,ip:`${rand(1,223)}.${rand(0,255)}.${rand(0,255)}.${rand(1,254)}`,time:new Date().toTimeString().slice(0,8)}}));

  useEffect(() => {
    const t = setInterval(() => {
      setAgents(prev => prev.map(a => {
        const load = Math.max(5,Math.min(98,a.load+rand(-4,4)));
        const tasks = Math.max(0,a.tasks+rand(-1,2));
        const status = load>82?'busy':load<8?'offline':'online';
        return {...a,load,tasks,status};
      }));
    }, 6000);
    return () => clearInterval(t);
  }, []);

  const showStatus = (msg, type) => {
    setUbStatus({msg,type});
    setTimeout(() => setUbStatus(null), 4000);
  };

  const filtered = ubFilter==='ALL'?blockedIPs:blockedIPs.filter(e=>e.reason.includes(ubFilter)||e.reason===ubFilter);
  const ubFilterMap = {'DDoS Flood':'DDoS Flood','Brute Force Login':'Brute Force Login','SQL Injection':'SQL Injection','Port Scan':'Port Scan','Malware Beacon':'Malware Beacon'};

  const unblockIdx = (idx) => {
    const entry = blockedIPs[idx];
    setBlockedIPs(prev => prev.filter((_,i)=>i!==idx));
    showStatus(`✓ ${entry.ip} unblocked — ACL rule removed.`, 'success');
  };

  const unblockAll = (reason) => {
    if (reason==='ALL') {
      const c = blockedIPs.length;
      setBlockedIPs([]);
      showStatus(`✓ All ${c} IPs unblocked.`, 'success');
    } else {
      const before = blockedIPs.length;
      setBlockedIPs(prev => prev.filter(e=>!e.reason.includes(reason)));
      showStatus(`✓ ${before - blockedIPs.filter(e=>!e.reason.includes(reason)).length} IP(s) unblocked.`, 'success');
    }
  };

  const submitUnblock = () => {
    const val = inputVal.trim();
    if (!val) { showStatus('⚠ Enter a valid IP address.','warn'); return; }
    if (!/^(\d{1,3}\.){3}\d{1,3}$/.test(val)||val.split('.').some(n=>+n>255)) { showStatus('✗ Invalid IP format.','error'); return; }
    const idx = blockedIPs.findIndex(e=>e.ip===val);
    if (idx===-1) { showStatus(`✗ ${val} not found in blocklist.`,'error'); }
    else { unblockIdx(idx); }
    setInputVal('');
  };

  const ubStatusStyles = {
    success:{bg:'rgba(0,255,157,.08)',border:'rgba(0,255,157,.3)',color:'#2a9968'},
    error:{bg:'rgba(255,59,92,.08)',border:'rgba(255,59,92,.3)',color:'#904050'},
    warn:{bg:'rgba(255,184,48,.08)',border:'rgba(255,184,48,.3)',color:'#886830'},
  };

  const crits = alerts.filter(a=>a.sev==='CRITICAL').length;
  const warns = alerts.filter(a=>a.sev==='WARNING').length;
  const online = agents.filter(a=>a.status==='online').length;
  const busy   = agents.filter(a=>a.status==='busy').length;
  const offline= agents.filter(a=>a.status==='offline').length;

  return (
    <div className="ubp-wrap">
      {/* LEFT: Alerts */}
      <div className="panel" style={{height:'100%'}}>
        <div className="panel-corner tl"/><div className="panel-corner tr"/>
        <div className="panel-corner bl"/><div className="panel-corner br"/>
        <div className="section-title">ACTIVE ALERTS</div>
        <div style={{display:'grid',gridTemplateColumns:'1fr 1fr',gap:8,marginBottom:16}}>
          <div className="ubp-stat danger"><div className="ubp-stat-val">{crits}</div><div className="ubp-stat-lbl">CRITICAL</div></div>
          <div className="ubp-stat warn"><div className="ubp-stat-val">{warns}</div><div className="ubp-stat-lbl">WARNING</div></div>
        </div>
        <div className="alert-feed">
          {alerts.map((a,i) => (
            <div key={i} className={`alert-item ${a.sev==='CRITICAL'?'crit':'warn'}`} style={{animationDelay:`${i*.03}s`}}>
              <div className="alert-item-hdr">
                <span style={{fontWeight:700,letterSpacing:1,color:a.sev==='CRITICAL'?'#a84050':'#886830'}}>{a.type}</span>
                <span style={{color:'var(--text-dim)',fontSize:9}}>{a.time}</span>
              </div>
              <div style={{color:'var(--text-dim)',fontSize:9,marginTop:2}}>SRC: {a.ip} · {a.sev}</div>
            </div>
          ))}
        </div>
      </div>

      {/* CENTRE: Unblock Manager */}
      <div className="panel">
        <div className="panel-corner tl"/><div className="panel-corner tr"/>
        <div className="panel-corner bl"/><div className="panel-corner br"/>
        <div style={{display:'flex',alignItems:'center',justifyContent:'space-between',marginBottom:20}}>
          <div className="section-title" style={{marginBottom:0,flex:1}}>IP UNBLOCK MANAGER</div>
          <div style={{fontFamily:'Share Tech Mono',fontSize:10,letterSpacing:2,color:'var(--text-dim)'}}>{blockedIPs.length} BLOCKED</div>
        </div>
        <div style={{display:'flex',gap:8,marginBottom:16}}>
          <input className="unblock-input" value={inputVal} onChange={e=>setInputVal(e.target.value)}
            placeholder="Search or enter IP address..."
            onKeyDown={e=>e.key==='Enter'&&submitUnblock()}/>
          <button className="unblock-submit-btn" onClick={submitUnblock}>⊘ UNBLOCK</button>
        </div>
        <div style={{display:'flex',gap:6,marginBottom:12,flexWrap:'wrap'}}>
          {['ALL','DDoS Flood','Brute Force Login','SQL Injection','Port Scan','Malware Beacon'].map(f=>(
            <button key={f} className={`ub-filter${ubFilter===f?' active':''}`} onClick={()=>setUbFilter(f)}>
              {f==='ALL'?'ALL':f==='DDoS Flood'?'DDOS':f==='Brute Force Login'?'BRUTE FORCE':f==='SQL Injection'?'SQL INJECT':f==='Port Scan'?'PORT SCAN':'MALWARE'}
            </button>
          ))}
        </div>
        <div className="ub-header">
          <span>STATUS</span><span>IP ADDRESS</span><span>REASON</span>
          <span>ATTEMPTS</span><span>BLOCKED SINCE</span><span>DURATION</span><span>ACTION</span>
        </div>
        <div className="ub-list">
          {filtered.length===0 ? (
            <div style={{fontFamily:'Share Tech Mono',fontSize:10,color:'var(--text-dim)',padding:16,textAlign:'center',letterSpacing:2}}>NO ENTRIES MATCH FILTER</div>
          ) : filtered.map((entry) => {
            const globalIdx = blockedIPs.indexOf(entry);
            return (
              <div key={entry.ip} className="ub-row">
                <span className="unblock-tag">BLOCKED</span>
                <span style={{color:'#a84050',fontWeight:700,letterSpacing:1}}>{entry.ip}</span>
                <span style={{color:'var(--text)'}}>{entry.reason}</span>
                <span style={{color:'#886830'}}>{entry.attempts.toLocaleString()}</span>
                <span style={{color:'var(--text-dim)'}}>{entry.since}</span>
                <span style={{color:'var(--text-dim)'}}>{entry.duration}</span>
                <button className="unblock-btn" onClick={()=>unblockIdx(globalIdx)}>✓ UNBLOCK</button>
              </div>
            );
          })}
        </div>
        {ubStatus && (
          <div style={{marginTop:12,padding:'9px 14px',borderRadius:3,fontFamily:'Share Tech Mono',fontSize:10,letterSpacing:1,background:ubStatusStyles[ubStatus.type]?.bg||ubStatusStyles.warn.bg,border:`1px solid ${ubStatusStyles[ubStatus.type]?.border||ubStatusStyles.warn.border}`,color:ubStatusStyles[ubStatus.type]?.color||ubStatusStyles.warn.color}}>
            {ubStatus.msg}
          </div>
        )}
        <div style={{marginTop:16,borderTop:'1px solid var(--border)',paddingTop:14,display:'flex',alignItems:'center',gap:10}}>
          <span style={{fontFamily:'Share Tech Mono',fontSize:9,letterSpacing:2,color:'var(--text-dim)'}}>BULK:</span>
          <button className="req-btn warn" style={{width:'auto',padding:'7px 14px'}} onClick={()=>unblockAll('Port Scan')}><span>⊘</span> Clear Port Scans</button>
          <button className="req-btn muted" style={{width:'auto',padding:'7px 14px'}} onClick={()=>unblockAll('ALL')}><span>⊘</span> Unblock All</button>
        </div>
      </div>

      {/* RIGHT: Agents */}
      <div className="panel" style={{height:'100%'}}>
        <div className="panel-corner tl"/><div className="panel-corner tr"/>
        <div className="panel-corner bl"/><div className="panel-corner br"/>
        <div className="section-title">ACTIVE AGENTS</div>
        <div style={{display:'grid',gridTemplateColumns:'1fr 1fr 1fr',gap:8,marginBottom:16}}>
          <div className="ubp-stat green"><div className="ubp-stat-val">{online}</div><div className="ubp-stat-lbl">ONLINE</div></div>
          <div className="ubp-stat warn"><div className="ubp-stat-val">{busy}</div><div className="ubp-stat-lbl">BUSY</div></div>
          <div className="ubp-stat danger"><div className="ubp-stat-val">{offline}</div><div className="ubp-stat-lbl">OFFLINE</div></div>
        </div>
        <div className="agent-feed">
          {agents.map((a,i) => {
            const barColor = a.load>80?'#904050':a.load>60?'#886830':'#2a9968';
            return (
              <div key={a.name} className="agent-card" style={{animationDelay:`${i*.04}s`}}>
                <div className="agent-card-top">
                  <div className="agent-name">{a.name}</div>
                  <span className={`agent-status-badge ${a.status}`}>{a.status.toUpperCase()}</span>
                </div>
                <div className="agent-meta">ROLE: {a.role}<br/>LOAD: {a.load}% · TASKS: {a.tasks}</div>
                <div className="agent-bar-wrap">
                  <div className="agent-bar" style={{width:`${a.load}%`,background:barColor}}/>
                </div>
              </div>
            );
          })}
        </div>
      </div>
    </div>
  );
}

// ─── ROOT APP ─────────────────────────────────────────────────────────────────
export default function AEGISApp() {
  const [page, setPage] = useState('dashboard');
  const [clock, setClock] = useState('');

  useEffect(() => {
    const t = setInterval(() => setClock(new Date().toTimeString().slice(0,8)+' UTC'), 1000);
    setClock(new Date().toTimeString().slice(0,8)+' UTC');
    return () => clearInterval(t);
  }, []);

  return (
    <div className="CipherNest-root">
      <style>{CSS}</style>
      <header className="CipherNest-header">
        <div className="CipherNest-logo">
          <div className="logo-shield"/>
          AEGIS
        </div>
        <div className="header-right">
          <div className="nav-tabs">
            <button className={`nav-tab${page==='dashboard'?' active':''}`} onClick={()=>setPage('dashboard')}>DASHBOARD</button>
            <button className={`nav-tab${page==='unblock'?' active':''}`} onClick={()=>setPage('unblock')}>UNBLOCK MANAGER</button>
          </div>
          <div className="status-pill"><div className="status-dot"/>ALL SYSTEMS NOMINAL</div>
          <div className="clock">{clock}</div>
          <div className="threat-badge">THREAT LEVEL: HIGH</div>
        </div>
      </header>
      {page === 'dashboard'
        ? <DashboardPage onNavigate={setPage}/>
        : <UnblockPage/>
      }
    </div>
  );
}
