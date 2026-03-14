"""
AEGIS — Cyber Defense Command
Streamlit dashboard for the CICIDS2017 MachineLearningCVE dataset.

Usage:
    pip install streamlit pandas plotly numpy watchdog
    streamlit run aegis_dashboard.py

Dataset folder structure expected (place CSVs in ./data/ or upload via sidebar):
    Monday-WorkingHours.pcap_ISCX.csv
    Tuesday-WorkingHours.pcap_ISCX.csv
    Wednesday-workingHours.pcap_ISCX.csv
    Thursday-WorkingHours-Morning-WebAttacks.pcap_ISCX.csv
    Thursday-WorkingHours-Afternoon-Infilteration.pcap_ISCX.csv
    Friday-WorkingHours-Morning.pcap_ISCX.csv
    Friday-WorkingHours-Afternoon-PortScan.pcap_ISCX.csv
    Friday-WorkingHours-Afternoon-DDos.pcap_ISCX.csv
"""

import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
import os
import glob
import time
import random
from datetime import datetime, timedelta
import warnings
warnings.filterwarnings("ignore")

# ─────────────────────────────────────────────────────────────
# PAGE CONFIG
# ─────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="AEGIS — Cyber Defense Command",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ─────────────────────────────────────────────────────────────
# CUSTOM CSS  (AEGIS military aesthetic)
# ─────────────────────────────────────────────────────────────
st.markdown("""
<style>
  @import url('https://fonts.googleapis.com/css2?family=Share+Tech+Mono&family=Rajdhani:wght@400;600;700&family=Orbitron:wght@400;700;900&display=swap');

  :root {
    --bg:      #020409;
    --surface: #070d18;
    --border:  #0e2040;
    --accent:  #00d4ff;
    --accent2: #00ff9d;
    --danger:  #ff3b5c;
    --warn:    #ffb830;
    --muted:   #2a4060;
    --text:    #c8dff5;
    --dim:     #4a6a90;
  }

  html, body, [class*="css"] {
    background-color: var(--bg) !important;
    color: var(--text) !important;
    font-family: 'Rajdhani', sans-serif !important;
  }

  /* Scanline overlay */
  .main::before {
    content: '';
    position: fixed; inset: 0;
    background: repeating-linear-gradient(0deg,transparent,transparent 2px,rgba(0,212,255,.012) 2px,rgba(0,212,255,.012) 4px);
    pointer-events: none; z-index: 9999;
  }

  /* Sidebar */
  [data-testid="stSidebar"] {
    background: #04080f !important;
    border-right: 1px solid var(--border) !important;
  }
  [data-testid="stSidebar"] * { color: var(--text) !important; }

  /* Metric cards */
  [data-testid="metric-container"] {
    background: var(--surface) !important;
    border: 1px solid var(--border) !important;
    border-radius: 4px !important;
    padding: 18px 20px !important;
    position: relative; overflow: hidden;
  }
  [data-testid="metric-container"]::before {
    content: '';
    position: absolute; top: 0; left: 0; right: 0; height: 2px;
    background: linear-gradient(90deg, transparent, var(--accent), transparent);
    opacity: .7;
  }
  [data-testid="stMetricLabel"] > div {
    font-family: 'Share Tech Mono', monospace !important;
    font-size: 10px !important; letter-spacing: 3px !important;
    color: var(--dim) !important; text-transform: uppercase;
  }
  [data-testid="stMetricValue"] > div {
    font-family: 'Orbitron', monospace !important;
    font-size: 28px !important; font-weight: 700 !important;
    color: var(--accent) !important;
  }
  [data-testid="stMetricDelta"] > div {
    font-family: 'Share Tech Mono', monospace !important;
    font-size: 11px !important;
  }

  /* Headers */
  h1, h2, h3 {
    font-family: 'Orbitron', monospace !important;
    letter-spacing: 4px !important;
    color: var(--accent) !important;
  }
  h1 { font-size: 24px !important; text-shadow: 0 0 30px rgba(0,212,255,.5); }
  h2 { font-size: 14px !important; color: var(--dim) !important; letter-spacing: 5px !important; }
  h3 { font-size: 12px !important; color: var(--dim) !important; letter-spacing: 4px !important; border-bottom: 1px solid var(--border); padding-bottom: 8px; }

  /* Dataframe */
  [data-testid="stDataFrame"] {
    border: 1px solid var(--border) !important; border-radius: 3px !important;
  }
  .stDataFrame { background: var(--surface) !important; }

  /* Selectbox / inputs */
  [data-baseweb="select"] > div,
  [data-baseweb="input"] > div {
    background: rgba(0,0,0,.4) !important;
    border-color: var(--border) !important;
    color: var(--text) !important;
    font-family: 'Share Tech Mono', monospace !important;
    font-size: 11px !important;
  }

  /* Buttons */
  .stButton > button {
    background: rgba(0,212,255,.07) !important;
    border: 1px solid rgba(0,212,255,.35) !important;
    color: #2a8aaa !important;
    font-family: 'Share Tech Mono', monospace !important;
    font-size: 10px !important; letter-spacing: 2px !important;
    border-radius: 2px !important;
    text-transform: uppercase !important;
    transition: all .2s !important;
  }
  .stButton > button:hover {
    background: rgba(0,212,255,.14) !important;
    border-color: rgba(0,212,255,.7) !important;
    color: #4ab0cc !important;
    box-shadow: 0 0 12px rgba(0,212,255,.2) !important;
  }

  /* Toggle */
  [data-testid="stToggle"] label {
    font-family: 'Share Tech Mono', monospace !important;
    font-size: 11px !important; letter-spacing: 2px !important;
    color: var(--dim) !important;
  }

  /* Tabs */
  [data-baseweb="tab-list"] { background: transparent !important; border-bottom: 1px solid var(--border) !important; }
  [data-baseweb="tab"] {
    font-family: 'Share Tech Mono', monospace !important;
    font-size: 10px !important; letter-spacing: 2px !important;
    color: var(--dim) !important; background: transparent !important;
    border: none !important;
  }
  [aria-selected="true"][data-baseweb="tab"] {
    color: var(--accent) !important;
    border-bottom: 2px solid var(--accent) !important;
  }

  /* Divider */
  hr { border-color: var(--border) !important; }

  /* Scrollbar */
  ::-webkit-scrollbar { width: 4px; height: 4px; }
  ::-webkit-scrollbar-track { background: transparent; }
  ::-webkit-scrollbar-thumb { background: var(--muted); border-radius: 2px; }

  /* Info / warning boxes */
  .stAlert { border-radius: 3px !important; font-family: 'Share Tech Mono', monospace !important; font-size: 11px !important; letter-spacing: 1px !important; }

  /* Sidebar radio */
  [data-testid="stRadio"] label {
    font-family: 'Share Tech Mono', monospace !important;
    font-size: 10px !important; letter-spacing: 2px !important;
  }

  /* File uploader */
  [data-testid="stFileUploader"] {
    border: 1px dashed var(--muted) !important;
    background: rgba(0,0,0,.3) !important;
    border-radius: 4px !important;
  }

  /* Caption */
  .stCaption, [data-testid="stCaptionContainer"] {
    font-family: 'Share Tech Mono', monospace !important;
    font-size: 9px !important; letter-spacing: 2px !important;
    color: var(--dim) !important;
  }

  /* Hide Streamlit chrome */
  #MainMenu, footer, header { visibility: hidden; }
  .block-container { padding-top: 1rem !important; padding-bottom: 1rem !important; }
</style>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────────────────────
# PLOTLY DARK THEME
# ─────────────────────────────────────────────────────────────
PLOT_BG   = "rgba(7,13,24,0.0)"
PAPER_BG  = "rgba(0,0,0,0.0)"
GRID_CLR  = "rgba(14,32,64,0.8)"
FONT_MONO = "Share Tech Mono"
ACCENT    = "#00d4ff"
ACCENT2   = "#00ff9d"
DANGER    = "#ff3b5c"
WARN      = "#ffb830"
PURPLE    = "#a78bfa"
DIM       = "#4a6a90"

ATTACK_PALETTE = {
    "BENIGN":                 "#2a4060",
    "DDoS":                   "#ff3b5c",
    "PortScan":               "#00d4ff",
    "Bot":                    "#a78bfa",
    "Infiltration":           "#ff9f43",
    "Web Attack – Brute Force": "#ffb830",
    "Web Attack – XSS":       "#fd79a8",
    "Web Attack – Sql Injection": "#e17055",
    "FTP-Patator":            "#00cec9",
    "SSH-Patator":            "#6c5ce7",
    "DoS slowloris":          "#d63031",
    "DoS Slowhttptest":       "#e84393",
    "DoS Hulk":               "#fdcb6e",
    "DoS GoldenEye":          "#e17055",
    "Heartbleed":             "#00b894",
}

def base_layout(height=350, margin=None):
    m = margin or dict(l=10, r=10, t=30, b=10)
    return dict(
        plot_bgcolor=PLOT_BG, paper_bgcolor=PAPER_BG, height=height,
        margin=m,
        font=dict(family=FONT_MONO, size=10, color=DIM),
        xaxis=dict(gridcolor=GRID_CLR, zeroline=False, showline=False),
        yaxis=dict(gridcolor=GRID_CLR, zeroline=False, showline=False),
        legend=dict(bgcolor="rgba(0,0,0,0)", font=dict(size=10, color=DIM),
                    bordercolor=GRID_CLR, borderwidth=1),
    )

# ─────────────────────────────────────────────────────────────
# SIMULATION DATA
# ─────────────────────────────────────────────────────────────
ATTACK_TYPES_SIM = ["DDoS","PortScan","Bot","Brute Force","DoS Hulk","DoS Slowloris",
                    "SSH-Patator","FTP-Patator","Web Attack XSS","SQL Injection","Heartbleed"]
PROTOCOLS_SIM    = ["TCP","UDP","HTTP","HTTPS","SSH","FTP","DNS","ICMP","SMB"]
ACTIONS_SIM      = ["BLOCKED","BLOCKED","BLOCKED","MONITOR","ALLOWED"]
IPS_SIM          = [f"192.168.{r}.{h}" for r in range(1,6) for h in range(1,20)]
EXT_IPS_SIM      = [f"{a}.{b}.{c}.{d}" for a,b,c,d in [
    (45,33,32,156),(103,21,244,0),(185,220,101,33),(77,88,55,80),(94,102,49,190),
    (66,249,66,1),(5,188,210,5),(192,241,209,4),(23,227,38,65),(104,21,67,200)]]

def sim_metrics():
    return {
        "active_alerts":  random.randint(12, 35),
        "blocked_ips":    random.randint(20, 70),
        "anomalous":      random.randint(5, 22),
        "net_load":       random.randint(30, 85),
        "total_flows":    random.randint(50000, 200000),
        "benign_pct":     random.uniform(60, 85),
    }

def sim_log_rows(n=40):
    rows = []
    for _ in range(n):
        at = random.choice(ATTACK_TYPES_SIM + ["BENIGN","BENIGN","BENIGN"])
        sev = "CRITICAL" if at in ("DDoS","Bot","Heartbleed","SQL Injection") else \
              "WARNING"  if at != "BENIGN" else "INFO"
        rows.append({
            "SEVERITY":    sev,
            "TIMESTAMP":   (datetime.now() - timedelta(seconds=random.randint(0,3600))).strftime("%H:%M:%S"),
            "EVENT TYPE":  at,
            "SOURCE IP":   random.choice(EXT_IPS_SIM if at != "BENIGN" else IPS_SIM),
            "DESTINATION": random.choice(IPS_SIM),
            "PROTOCOL":    random.choice(PROTOCOLS_SIM),
            "ACTION":      "ALLOWED" if at == "BENIGN" else random.choice(["BLOCKED","BLOCKED","MONITOR"]),
            "PORT":        random.randint(1, 65535),
        })
    return pd.DataFrame(rows)

def sim_threat_dist():
    return pd.Series({
        "DDoS": random.randint(200,600), "PortScan": random.randint(150,400),
        "Bot": random.randint(50,200), "Brute Force": random.randint(100,300),
        "DoS Hulk": random.randint(80,250), "Web Attack": random.randint(30,120),
        "SQL Injection": random.randint(10,60), "Heartbleed": random.randint(1,20),
    })

def sim_timeseries(n=60):
    t = pd.date_range(end=datetime.now(), periods=n, freq="1min")
    base_attack = 30
    base_benign = 200
    attacks = np.clip(base_attack + np.cumsum(np.random.randn(n)*5), 0, 200).astype(int)
    benign  = np.clip(base_benign + np.cumsum(np.random.randn(n)*10), 50, 600).astype(int)
    return pd.DataFrame({"time": t, "attacks": attacks, "benign": benign})

def sim_ntp_clients():
    hosts = ["srv-web-01","srv-db-02","srv-api-03","wks-fin-07","wks-hr-12",
             "srv-mail-04","srv-proxy-05","cam-lobby-01","wks-dev-09","srv-auth-06"]
    rows = []
    for i, h in enumerate(hosts):
        status = random.choices(["SYNCED","DRIFTING","OFFLINE"], weights=[7,2,1])[0]
        offset = round(random.uniform(-15, 15), 3)
        rows.append({
            "CLIENT IP": f"10.{i//5+1}.{i%5+1}.{10+i*7}",
            "HOSTNAME":  h,
            "STRATUM":   random.choice([1,2,2,3,3]),
            "OFFSET (ms)": offset,
            "LAST SYNC": f"{random.randint(0,120)}s ago",
            "STATUS":    status,
        })
    return pd.DataFrame(rows)

def sim_speed():
    up = round(random.uniform(15, 120), 2)
    dn = round(random.uniform(20, 140), 2)
    return up, dn

# ─────────────────────────────────────────────────────────────
# REAL DATA LOADING & PROCESSING (CICIDS2017)
# ─────────────────────────────────────────────────────────────
CICIDS_LABEL_COL = " Label"   # note leading space in original CSVs

CICIDS_KEY_COLS = [
    " Flow Duration", " Total Fwd Packets", " Total Backward Packets",
    " Total Length of Fwd Packets", " Total Length of Bwd Packets",
    " Flow Bytes/s", " Flow Packets/s", " Flow IAT Mean",
    " Fwd Packet Length Max", " Bwd Packet Length Max",
    " Fwd Packets/s", " Bwd Packets/s",
    " Packet Length Mean", " Packet Length Std",
    " Average Packet Size", " Avg Fwd Segment Size",
    " Destination Port", " Protocol",
    " SYN Flag Count", " ACK Flag Count", " PSH Flag Count",
    " Init_Win_bytes_forward", " Init_Win_bytes_backward",
    CICIDS_LABEL_COL
]

@st.cache_data(show_spinner=False)
def load_cicids(files):
    """Load and concatenate CICIDS2017 CSVs, return cleaned DataFrame."""
    dfs = []
    for f in files:
        try:
            chunk = pd.read_csv(f, low_memory=False)
            chunk.columns = chunk.columns.str.strip()  # strip ALL spaces from cols
            dfs.append(chunk)
        except Exception as e:
            st.warning(f"Could not load {getattr(f,'name',f)}: {e}")
    if not dfs:
        return None

    df = pd.concat(dfs, ignore_index=True)

    # Normalise label column name (could have leading space or not)
    label_col = None
    for candidate in ["Label", " Label", "label"]:
        if candidate in df.columns:
            label_col = candidate
            break
    if label_col and label_col != "Label":
        df.rename(columns={label_col: "Label"}, inplace=True)

    # Strip column name spaces
    df.columns = df.columns.str.strip()

    # Drop rows with inf / all-NaN
    df.replace([np.inf, -np.inf], np.nan, inplace=True)
    df.dropna(subset=["Label"], inplace=True)

    # Normalise label strings
    df["Label"] = df["Label"].str.strip()
    df["Label"] = df["Label"].replace({
        "Web Attack \x96 Brute Force": "Web Attack – Brute Force",
        "Web Attack \x96 XSS":         "Web Attack – XSS",
        "Web Attack \x96 Sql Injection":"Web Attack – Sql Injection",
        "Web Attack – Brute Force":    "Web Attack – Brute Force",
    })

    # Numeric coercion for flow stats
    for col in ["Flow Bytes/s", "Flow Packets/s"]:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors="coerce")

    # Severity mapping
    CRITICAL_LABELS = {"DDoS","Bot","Heartbleed","Infiltration",
                       "Web Attack – Sql Injection","DoS GoldenEye","DoS Hulk"}
    WARNING_LABELS  = {"PortScan","FTP-Patator","SSH-Patator","DoS slowloris",
                       "DoS Slowhttptest","Web Attack – Brute Force","Web Attack – XSS"}
    def sev(lbl):
        if lbl in CRITICAL_LABELS: return "CRITICAL"
        if lbl in WARNING_LABELS:  return "WARNING"
        if lbl == "BENIGN":        return "INFO"
        return "WARNING"
    df["Severity"] = df["Label"].apply(sev)

    # Action mapping
    def action(lbl):
        if lbl == "BENIGN": return "ALLOWED"
        if lbl in CRITICAL_LABELS: return "BLOCKED"
        return "MONITOR"
    df["Action"] = df["Label"].apply(action)

    # Protocol number → name
    PROTO_MAP = {0:"HOPOPT",1:"ICMP",2:"IGMP",6:"TCP",17:"UDP",
                 41:"IPv6",43:"IPv6-Route",44:"IPv6-Frag",
                 58:"IPv6-ICMP",89:"OSPF",132:"SCTP"}
    if "Protocol" in df.columns:
        df["Protocol_Name"] = pd.to_numeric(df["Protocol"], errors="coerce").map(PROTO_MAP).fillna("OTHER")
    else:
        df["Protocol_Name"] = "TCP"

    return df

def compute_real_metrics(df):
    total    = len(df)
    attacks  = (df["Label"] != "BENIGN").sum()
    blocked  = (df["Action"] == "BLOCKED").sum()
    benign   = (df["Label"] == "BENIGN").sum()
    unique_src = df["Source IP"].nunique() if "Source IP" in df.columns else \
                 df["Destination Port"].nunique() if "Destination Port" in df.columns else 0
    return {
        "active_alerts":  int(attacks),
        "blocked_ips":    int(blocked),
        "anomalous":      int(df[df["Severity"].isin(["CRITICAL","WARNING"])].shape[0]),
        "net_load":       min(99, round(attacks / max(total, 1) * 100, 1)),
        "total_flows":    total,
        "benign_pct":     round(benign / max(total, 1) * 100, 1),
    }

# ─────────────────────────────────────────────────────────────
# CHART BUILDERS
# ─────────────────────────────────────────────────────────────
def chart_threat_donut(dist: pd.Series):
    labels = dist.index.tolist()
    values = dist.values.tolist()
    colors = [ATTACK_PALETTE.get(l, WARN) for l in labels]
    fig = go.Figure(go.Pie(
        labels=labels, values=values, hole=.68,
        marker=dict(colors=colors, line=dict(color="#020409", width=2)),
        textinfo="none",
        hovertemplate="<b>%{label}</b><br>%{value:,} events<br>%{percent}<extra></extra>",
    ))
    fig.update_layout(**base_layout(320), showlegend=True,
        legend=dict(orientation="v", x=1, y=.5, font=dict(size=9, color=DIM)))
    fig.add_annotation(text=f"<b>{sum(values):,}</b><br><span style='font-size:9px'>EVENTS</span>",
        x=.5, y=.5, showarrow=False, font=dict(family="Orbitron", size=13, color=ACCENT),
        align="center")
    return fig

def chart_timeseries(ts: pd.DataFrame):
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=ts["time"], y=ts["attacks"], name="Attacks",
        line=dict(color=DANGER, width=2), fill="tozeroy",
        fillcolor="rgba(255,59,92,.08)",
        hovertemplate="%{x|%H:%M}<br><b>%{y:,}</b> attacks<extra></extra>",
    ))
    fig.add_trace(go.Scatter(
        x=ts["time"], y=ts["benign"], name="Benign",
        line=dict(color=DIM, width=1.5), fill="tozeroy",
        fillcolor="rgba(42,64,96,.15)",
        hovertemplate="%{x|%H:%M}<br><b>%{y:,}</b> benign<extra></extra>",
    ))
    fig.update_layout(**base_layout(220),
        xaxis=dict(gridcolor=GRID_CLR, showticklabels=True,
                   tickfont=dict(family=FONT_MONO, size=9, color=DIM)),
        yaxis=dict(gridcolor=GRID_CLR,
                   tickfont=dict(family=FONT_MONO, size=9, color=DIM)),
    )
    return fig

def chart_attack_bar(dist: pd.Series, title=""):
    labels = [l for l in dist.index if l != "BENIGN"]
    values = [dist[l] for l in labels]
    colors = [ATTACK_PALETTE.get(l, WARN) for l in labels]
    fig = go.Figure(go.Bar(
        x=values, y=labels, orientation="h",
        marker=dict(color=colors, opacity=0.85,
                    line=dict(color=[c+"55" for c in colors], width=1)),
        hovertemplate="<b>%{y}</b><br>%{x:,} events<extra></extra>",
    ))
    fig.update_layout(**base_layout(max(240, len(labels)*32), margin=dict(l=10,r=10,t=28,b=10)),
        yaxis=dict(categoryorder="total ascending", tickfont=dict(size=10, color=DIM)),
        xaxis=dict(tickfont=dict(size=9, color=DIM)),
        title=dict(text=title, font=dict(family="Orbitron", size=10, color=DIM), x=0),
    )
    return fig

def chart_flow_bytes(df: pd.DataFrame):
    """Flow bytes/s distribution by attack type (violin/box hybrid)."""
    col = "Flow Bytes/s"
    if col not in df.columns:
        return None
    sample = df[df[col].notna() & (df[col] < df[col].quantile(.995))].sample(
        min(20000, len(df)), random_state=42)
    top_labels = sample[sample["Label"] != "BENIGN"]["Label"].value_counts().head(6).index.tolist()
    plot_labels = ["BENIGN"] + top_labels
    sample = sample[sample["Label"].isin(plot_labels)]
    fig = go.Figure()
    for lbl in plot_labels:
        sub = sample[sample["Label"] == lbl][col]
        fig.add_trace(go.Box(
            y=sub, name=lbl,
            marker_color=ATTACK_PALETTE.get(lbl, WARN),
            line=dict(width=1), boxmean=True,
            hoverinfo="name+y",
        ))
    fig.update_layout(**base_layout(300),
        yaxis=dict(title="Flow Bytes/s", tickfont=dict(size=9, color=DIM),
                   type="log", gridcolor=GRID_CLR),
        showlegend=False,
    )
    return fig

def chart_protocol_pie(df: pd.DataFrame):
    counts = df["Protocol_Name"].value_counts().head(8)
    colors = [ACCENT, ACCENT2, WARN, DANGER, PURPLE, "#fd79a8","#00cec9","#6c5ce7"]
    fig = go.Figure(go.Pie(
        labels=counts.index, values=counts.values, hole=.5,
        marker=dict(colors=colors[:len(counts)], line=dict(color="#020409", width=2)),
        textinfo="none",
        hovertemplate="<b>%{label}</b><br>%{value:,}<br>%{percent}<extra></extra>",
    ))
    fig.update_layout(**base_layout(260), showlegend=True,
        legend=dict(orientation="v", x=1, y=.5, font=dict(size=9, color=DIM)))
    return fig

def chart_port_heatmap(df: pd.DataFrame):
    if "Destination Port" not in df.columns:
        return None
    top_ports = df[df["Label"] != "BENIGN"]["Destination Port"].value_counts().head(12).index
    top_attacks = df[df["Label"] != "BENIGN"]["Label"].value_counts().head(8).index
    sub = df[df["Destination Port"].isin(top_ports) & df["Label"].isin(top_attacks)]
    pivot = sub.groupby(["Label","Destination Port"]).size().unstack(fill_value=0)
    if pivot.empty:
        return None
    fig = go.Figure(go.Heatmap(
        z=pivot.values,
        x=[str(c) for c in pivot.columns],
        y=pivot.index.tolist(),
        colorscale=[[0,"rgba(0,0,0,0)"],[0.01,GRID_CLR],[.5,WARN],[1,DANGER]],
        hovertemplate="Attack: <b>%{y}</b><br>Port: <b>%{x}</b><br>Count: <b>%{z:,}</b><extra></extra>",
        showscale=False,
    ))
    fig.update_layout(**base_layout(300),
        xaxis=dict(title="Destination Port", tickfont=dict(size=9, color=DIM), gridcolor=GRID_CLR),
        yaxis=dict(tickfont=dict(size=10, color=DIM)),
    )
    return fig

def chart_net_performance():
    """Simulated network performance (latency, error rate, req rate, conn duration)."""
    n = 40
    t = list(range(n))
    fig = go.Figure()
    for name, color, mn, mx in [
        ("Latency (ms)", WARN, 10, 80),
        ("Error Ratio",  DANGER, 0, 1),
        ("Req Rate",     ACCENT, 0, 3),
        ("Conn Duration",ACCENT2, 1, 15),
    ]:
        y = [round(random.uniform(mn, mx), 2) for _ in range(n)]
        fig.add_trace(go.Scatter(
            x=t, y=y, name=name,
            line=dict(color=color, width=2), fill="tozeroy",
            fillcolor=color.replace("#","") and f"rgba({int(color[1:3],16)},{int(color[3:5],16)},{int(color[5:7],16)},.06)",
            hovertemplate=f"<b>{name}</b>: %{{y}}<extra></extra>",
        ))
    fig.update_layout(**base_layout(200),
        xaxis=dict(showticklabels=False, gridcolor=GRID_CLR),
        yaxis=dict(tickfont=dict(size=9, color=DIM), gridcolor=GRID_CLR),
    )
    return fig

def chart_speed(up_hist, dn_hist):
    n = len(up_hist)
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        y=up_hist, name="Send", line=dict(color=ACCENT2, width=2),
        fill="tozeroy", fillcolor="rgba(0,255,157,.08)",
        hovertemplate="Send: <b>%{y:.1f} Mbps</b><extra></extra>",
    ))
    fig.add_trace(go.Scatter(
        y=dn_hist, name="Receive", line=dict(color=ACCENT, width=2),
        fill="tozeroy", fillcolor="rgba(0,212,255,.08)",
        hovertemplate="Recv: <b>%{y:.1f} Mbps</b><extra></extra>",
    ))
    fig.update_layout(**base_layout(180, margin=dict(l=10,r=10,t=10,b=10)),
        xaxis=dict(showticklabels=False, gridcolor=GRID_CLR),
        yaxis=dict(range=[0,150], tickfont=dict(size=9, color=DIM), gridcolor=GRID_CLR,
                   ticksuffix=" M"),
        showlegend=True,
    )
    return fig

def chart_offset_dist(ntp_df: pd.DataFrame):
    bins = [-15,-8,-4,-2,0,2,4,8,15]
    labels_b = ["<-8","-8:-4","-4:-2","-2:0","0:2","2:4","4:8",">8"]
    counts, _ = np.histogram(ntp_df["OFFSET (ms)"].dropna(), bins=bins)
    colors = [DANGER if abs(i-3.5)>2 else WARN if abs(i-3.5)>1 else ACCENT2
              for i in range(len(labels_b))]
    fig = go.Figure(go.Bar(
        x=labels_b, y=counts, marker_color=colors, marker_opacity=.7,
        hovertemplate="<b>%{x}</b><br>%{y} clients<extra></extra>",
    ))
    fig.update_layout(**base_layout(120, margin=dict(l=5,r=5,t=5,b=5)),
        xaxis=dict(tickfont=dict(size=8, color=DIM), gridcolor="rgba(0,0,0,0)"),
        yaxis=dict(tickfont=dict(size=9, color=DIM), gridcolor=GRID_CLR, dtick=1),
        showlegend=False,
    )
    return fig

def chart_feature_importance(df: pd.DataFrame):
    """Top 15 features correlated with attacks using absolute mean difference."""
    numeric_cols = df.select_dtypes(include=[np.number]).columns.tolist()
    exclude = ["Destination Port","Protocol"]
    numeric_cols = [c for c in numeric_cols if c not in exclude]
    is_attack = (df["Label"] != "BENIGN").astype(int)
    scores = {}
    sample = df.sample(min(30000, len(df)), random_state=42)
    is_attack_s = (sample["Label"] != "BENIGN")
    for col in numeric_cols[:50]:
        try:
            m_att = sample.loc[is_attack_s, col].mean()
            m_ben = sample.loc[~is_attack_s, col].mean()
            std   = sample[col].std()
            if std > 0:
                scores[col] = abs(m_att - m_ben) / std
        except Exception:
            pass
    if not scores:
        return None
    top = sorted(scores.items(), key=lambda x: x[1], reverse=True)[:15]
    labels_, vals_ = zip(*top)
    fig = go.Figure(go.Bar(
        x=list(vals_), y=list(labels_), orientation="h",
        marker=dict(color=ACCENT, opacity=0.75,
                    line=dict(color=ACCENT+"55", width=1)),
        hovertemplate="<b>%{y}</b><br>Score: %{x:.3f}<extra></extra>",
    ))
    fig.update_layout(**base_layout(360, margin=dict(l=10,r=10,t=28,b=10)),
        yaxis=dict(categoryorder="total ascending", tickfont=dict(size=9, color=DIM)),
        xaxis=dict(title="Normalised Separation Score", tickfont=dict(size=9, color=DIM)),
        title=dict(text="TOP DISCRIMINATING FEATURES", font=dict(family="Orbitron", size=10, color=DIM), x=0),
    )
    return fig

# ─────────────────────────────────────────────────────────────
# HELPERS
# ─────────────────────────────────────────────────────────────
def sev_color_html(sev):
    c = {"CRITICAL":"#b84055","WARNING":"#a87830","INFO":"#2a7a96"}.get(sev, "#4a6a90")
    bg = {"CRITICAL":"rgba(255,59,92,.1)","WARNING":"rgba(255,184,48,.08)","INFO":"rgba(0,212,255,.06)"}.get(sev,"transparent")
    return f'<span style="color:{c};background:{bg};padding:2px 6px;border-radius:2px;font-size:10px;letter-spacing:2px;">{sev}</span>'

def action_color_html(act):
    c  = {"BLOCKED":"#b84055","ALLOWED":"#2a9968","MONITOR":"#a87830"}.get(act,"#4a6a90")
    bg = {"BLOCKED":"rgba(255,59,92,.1)","ALLOWED":"rgba(0,255,157,.07)","MONITOR":"rgba(255,184,48,.07)"}.get(act,"transparent")
    return f'<span style="color:{c};background:{bg};padding:2px 6px;border-radius:2px;font-size:10px;letter-spacing:1px;">{act}</span>'

def section_title(title):
    st.markdown(f"""
    <div style="display:flex;align-items:center;gap:12px;margin-bottom:16px;margin-top:4px;">
      <span style="font-family:'Orbitron',monospace;font-size:11px;letter-spacing:4px;
                   color:#4a6a90;text-transform:uppercase;">{title}</span>
      <div style="flex:1;height:1px;background:linear-gradient(90deg,#0e2040,transparent);"></div>
    </div>""", unsafe_allow_html=True)

def metric_card(label, value, delta=None, color=ACCENT):
    st.metric(label=label, value=value, delta=delta)

def render_log_table(log_df: pd.DataFrame, max_rows=35):
    """Render security log as styled HTML table."""
    rows_html = ""
    for _, row in log_df.head(max_rows).iterrows():
        sev = row.get("SEVERITY", "INFO")
        act = row.get("ACTION", "MONITOR")
        border_color = {"CRITICAL":"rgba(255,59,92,.4)","WARNING":"rgba(255,184,48,.3)","INFO":"rgba(14,32,64,.9)"}.get(sev,"transparent")
        bg_color     = {"CRITICAL":"rgba(255,59,92,.02)","WARNING":"rgba(255,184,48,.01)","INFO":"transparent"}.get(sev,"transparent")
        rows_html += f"""
        <tr style="border-left:2px solid {border_color};background:{bg_color};">
          <td>{sev_color_html(sev)}</td>
          <td style="color:#5a8ab0;letter-spacing:1px;">{row.get("TIMESTAMP","—")}</td>
          <td style="color:#b85060;font-weight:600;">{row.get("EVENT TYPE","—")}</td>
          <td style="color:#a84050;font-weight:700;">{row.get("SOURCE IP","—")}</td>
          <td style="color:#4a7090;">{row.get("DESTINATION","—")}</td>
          <td style="color:#00b8d9;letter-spacing:1px;">{row.get("PROTOCOL","—")}</td>
          <td>{action_color_html(act)}</td>
          <td style="color:#3a6080;">Port {row.get("PORT","—")}</td>
        </tr>"""
    st.markdown(f"""
    <div style="overflow-x:auto;overflow-y:auto;max-height:420px;border:1px solid #0e2040;border-radius:3px;">
    <table style="width:100%;border-collapse:collapse;font-family:'Share Tech Mono',monospace;font-size:11px;">
      <thead>
        <tr style="background:rgba(0,212,255,.04);border-bottom:1px solid #0e2040;">
          <th style="padding:7px 12px;color:#4a6a90;letter-spacing:2px;font-size:9px;text-align:left;">SEVERITY</th>
          <th style="padding:7px 12px;color:#4a6a90;letter-spacing:2px;font-size:9px;text-align:left;">TIMESTAMP</th>
          <th style="padding:7px 12px;color:#4a6a90;letter-spacing:2px;font-size:9px;text-align:left;">EVENT TYPE</th>
          <th style="padding:7px 12px;color:#4a6a90;letter-spacing:2px;font-size:9px;text-align:left;">SOURCE IP</th>
          <th style="padding:7px 12px;color:#4a6a90;letter-spacing:2px;font-size:9px;text-align:left;">DESTINATION</th>
          <th style="padding:7px 12px;color:#4a6a90;letter-spacing:2px;font-size:9px;text-align:left;">PROTOCOL</th>
          <th style="padding:7px 12px;color:#4a6a90;letter-spacing:2px;font-size:9px;text-align:left;">ACTION</th>
          <th style="padding:7px 12px;color:#4a6a90;letter-spacing:2px;font-size:9px;text-align:left;">DETAILS</th>
        </tr>
      </thead>
      <tbody>{rows_html}</tbody>
    </table></div>""", unsafe_allow_html=True)

def render_ntp_table(ntp_df: pd.DataFrame):
    rows_html = ""
    for _, row in ntp_df.iterrows():
        status = row["STATUS"]
        sc = {"SYNCED":"var(--accent2)","DRIFTING":"var(--warn)","OFFLINE":"var(--danger)"}.get(status, DIM)
        sbg= {"SYNCED":"rgba(0,255,157,.1)","DRIFTING":"rgba(255,184,48,.1)","OFFLINE":"rgba(255,59,92,.1)"}.get(status,"transparent")
        off = row["OFFSET (ms)"]
        oc = ACCENT2 if abs(off) < 2 else WARN if abs(off) < 8 else DANGER
        rows_html += f"""
        <tr style="border:1px solid transparent;">
          <td style="color:#00d4ff;">{row["CLIENT IP"]}</td>
          <td style="color:#c8dff5;">{row["HOSTNAME"]}</td>
          <td style="color:#4a6a90;text-align:center;">{row["STRATUM"]}</td>
          <td style="color:{oc};font-weight:700;">{"+"+str(off) if off>0 else str(off)}</td>
          <td style="color:#4a6a90;">{row["LAST SYNC"]}</td>
          <td><span style="color:{sc};background:{sbg};padding:2px 7px;border-radius:2px;
                           font-size:9px;letter-spacing:2px;border:1px solid {sc}40;">{status}</span></td>
        </tr>"""
    st.markdown(f"""
    <div style="overflow-y:auto;max-height:260px;border:1px solid #0e2040;border-radius:3px;">
    <table style="width:100%;border-collapse:collapse;font-family:'Share Tech Mono',monospace;font-size:11px;">
      <thead>
        <tr style="background:rgba(0,212,255,.04);border-bottom:1px solid #0e2040;">
          <th style="padding:6px 10px;color:#4a6a90;letter-spacing:2px;font-size:9px;text-align:left;">CLIENT IP</th>
          <th style="padding:6px 10px;color:#4a6a90;letter-spacing:2px;font-size:9px;text-align:left;">HOSTNAME</th>
          <th style="padding:6px 10px;color:#4a6a90;letter-spacing:2px;font-size:9px;text-align:left;">STRATUM</th>
          <th style="padding:6px 10px;color:#4a6a90;letter-spacing:2px;font-size:9px;text-align:left;">OFFSET (ms)</th>
          <th style="padding:6px 10px;color:#4a6a90;letter-spacing:2px;font-size:9px;text-align:left;">LAST SYNC</th>
          <th style="padding:6px 10px;color:#4a6a90;letter-spacing:2px;font-size:9px;text-align:left;">STATUS</th>
        </tr>
      </thead>
      <tbody>{rows_html}</tbody>
    </table></div>""", unsafe_allow_html=True)

def render_blocked_table(blocked_ips):
    rows_html = ""
    for ip_entry in blocked_ips:
        rows_html += f"""
        <tr>
          <td><span style="background:rgba(255,59,92,.1);color:#904050;border:1px solid rgba(255,59,92,.35);
                           padding:2px 7px;border-radius:2px;font-size:9px;letter-spacing:2px;">BLOCKED</span></td>
          <td style="color:#a84050;font-weight:700;">{ip_entry["ip"]}</td>
          <td style="color:#c8dff5;">{ip_entry["reason"]}</td>
          <td style="color:#886830;">{ip_entry["attempts"]:,}</td>
          <td style="color:#4a6a90;">{ip_entry["since"]}</td>
          <td style="color:#4a6a90;">{ip_entry["duration"]}</td>
        </tr>"""
    st.markdown(f"""
    <div style="overflow-y:auto;max-height:320px;border:1px solid rgba(255,59,92,.2);border-radius:3px;">
    <table style="width:100%;border-collapse:collapse;font-family:'Share Tech Mono',monospace;font-size:11px;">
      <thead>
        <tr style="background:rgba(255,59,92,.04);border-bottom:1px solid rgba(255,59,92,.2);">
          <th style="padding:6px 12px;color:#4a6a90;letter-spacing:2px;font-size:9px;text-align:left;">STATUS</th>
          <th style="padding:6px 12px;color:#4a6a90;letter-spacing:2px;font-size:9px;text-align:left;">IP ADDRESS</th>
          <th style="padding:6px 12px;color:#4a6a90;letter-spacing:2px;font-size:9px;text-align:left;">REASON</th>
          <th style="padding:6px 12px;color:#4a6a90;letter-spacing:2px;font-size:9px;text-align:left;">ATTEMPTS</th>
          <th style="padding:6px 12px;color:#4a6a90;letter-spacing:2px;font-size:9px;text-align:left;">BLOCKED SINCE</th>
          <th style="padding:6px 12px;color:#4a6a90;letter-spacing:2px;font-size:9px;text-align:left;">DURATION</th>
        </tr>
      </thead>
      <tbody>{rows_html}</tbody>
    </table></div>""", unsafe_allow_html=True)

# ─────────────────────────────────────────────────────────────
# SESSION STATE INIT
# ─────────────────────────────────────────────────────────────
if "sim_mode" not in st.session_state:
    st.session_state.sim_mode = True
if "df" not in st.session_state:
    st.session_state.df = None
if "up_hist" not in st.session_state:
    st.session_state.up_hist = [random.uniform(20,80) for _ in range(60)]
    st.session_state.dn_hist = [random.uniform(30,100) for _ in range(60)]
if "total_up" not in st.session_state:
    st.session_state.total_up = 0.0
    st.session_state.total_dn = 0.0
if "peak_up" not in st.session_state:
    st.session_state.peak_up = 0.0
    st.session_state.peak_dn = 0.0
if "blocked_ips" not in st.session_state:
    st.session_state.blocked_ips = [
        {"ip":"45.33.32.156",   "reason":"DDoS Flood",       "since":"02:14:08","attempts":847,  "duration":"3h 22m"},
        {"ip":"192.168.4.201",  "reason":"Brute Force Login","since":"03:41:22","attempts":312,  "duration":"1h 55m"},
        {"ip":"103.21.244.0",   "reason":"SQL Injection",    "since":"04:07:55","attempts":119,  "duration":"1h 28m"},
        {"ip":"185.220.101.33", "reason":"Malware Beacon",   "since":"04:55:10","attempts":64,   "duration":"0h 41m"},
        {"ip":"66.249.66.1",    "reason":"Port Scan",        "since":"05:12:38","attempts":28,   "duration":"0h 23m"},
        {"ip":"77.88.55.80",    "reason":"Credential Stuffing","since":"01:30:00","attempts":1203,"duration":"4h 06m"},
        {"ip":"94.102.49.190",  "reason":"DDoS Flood",       "since":"02:58:14","attempts":589,  "duration":"2h 37m"},
        {"ip":"5.188.210.5",    "reason":"Port Scan",        "since":"05:44:01","attempts":17,   "duration":"0h 08m"},
    ]
if "investigations" not in st.session_state:
    st.session_state.investigations = []

# ─────────────────────────────────────────────────────────────
# HEADER
# ─────────────────────────────────────────────────────────────
st.markdown(f"""
<div style="display:flex;align-items:center;justify-content:space-between;
            padding:0 0 16px 0;border-bottom:1px solid #0e2040;margin-bottom:20px;">
  <div style="display:flex;align-items:center;gap:14px;">
    <div style="width:34px;height:34px;background:linear-gradient(135deg,#00d4ff,#00ff9d);
                clip-path:polygon(50% 0%,100% 25%,100% 75%,50% 100%,0% 75%,0% 25%);
                box-shadow:0 0 20px rgba(0,212,255,.4);"></div>
    <span style="font-family:'Orbitron',monospace;font-size:26px;font-weight:900;
                 letter-spacing:8px;color:#00d4ff;text-shadow:0 0 30px rgba(0,212,255,.5);">AEGIS</span>
  </div>
  <div style="display:flex;align-items:center;gap:20px;">
    <div style="display:flex;align-items:center;gap:8px;padding:6px 14px;
                border:1px solid #00ff9d;border-radius:2px;font-family:'Share Tech Mono',monospace;
                font-size:11px;letter-spacing:2px;color:#00ff9d;">
      <div style="width:8px;height:8px;border-radius:50%;background:#00ff9d;
                  box-shadow:0 0 8px #00ff9d;animation:blink 1.2s ease infinite;"></div>
      ALL SYSTEMS NOMINAL
    </div>
    <div style="padding:6px 14px;background:rgba(255,59,92,.12);border:1px solid #ff3b5c;
                border-radius:2px;font-family:'Share Tech Mono',monospace;font-size:11px;
                letter-spacing:2px;color:#ff3b5c;">
      THREAT LEVEL: HIGH
    </div>
    <div style="font-family:'Share Tech Mono',monospace;font-size:12px;letter-spacing:2px;color:#4a6a90;">
      {datetime.now().strftime("%H:%M:%S")} UTC
    </div>
  </div>
</div>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────────────────────
# SIDEBAR
# ─────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown('<div style="font-family:\'Orbitron\',monospace;font-size:14px;letter-spacing:4px;color:#00d4ff;margin-bottom:20px;">⚙ COMMAND CENTER</div>', unsafe_allow_html=True)

    # Simulation toggle
    sim_mode = st.toggle("⚡ SIMULATION MODE", value=st.session_state.sim_mode, key="sim_toggle")
    st.session_state.sim_mode = sim_mode

    if sim_mode:
        st.markdown('<div style="font-family:\'Share Tech Mono\',monospace;font-size:9px;letter-spacing:2px;color:#2a9968;background:rgba(0,255,157,.08);border:1px solid rgba(0,255,157,.25);padding:6px 10px;border-radius:2px;margin-top:4px;">● SIM DATA ACTIVE</div>', unsafe_allow_html=True)
    else:
        if st.session_state.df is not None:
            st.markdown(f'<div style="font-family:\'Share Tech Mono\',monospace;font-size:9px;letter-spacing:2px;color:#2a8aaa;background:rgba(0,212,255,.08);border:1px solid rgba(0,212,255,.25);padding:6px 10px;border-radius:2px;margin-top:4px;">◈ LIVE DATA — {len(st.session_state.df):,} RECORDS</div>', unsafe_allow_html=True)
        else:
            st.markdown('<div style="font-family:\'Share Tech Mono\',monospace;font-size:9px;letter-spacing:2px;color:#904050;background:rgba(255,59,92,.06);border:1px solid rgba(255,59,92,.2);padding:6px 10px;border-radius:2px;margin-top:4px;">⊗ NO DATASET LOADED</div>', unsafe_allow_html=True)

    st.divider()

    # Dataset upload
    st.markdown('<div style="font-family:\'Share Tech Mono\',monospace;font-size:9px;letter-spacing:3px;color:#4a6a90;margin-bottom:8px;">DATASET — CICIDS2017</div>', unsafe_allow_html=True)
    uploaded = st.file_uploader(
        "Upload CSV file(s)", type=["csv"],
        accept_multiple_files=True,
        help="Upload one or more MachineLearningCVE CSV files from the CICIDS2017 dataset"
    )

    if uploaded:
        with st.spinner("⚙ PARSING DATASET…"):
            df_loaded = load_cicids(uploaded)
        if df_loaded is not None and len(df_loaded) > 0:
            st.session_state.df = df_loaded
            st.session_state.sim_mode = False
            st.success(f"✓ {len(df_loaded):,} records loaded")
        else:
            st.error("Failed to parse dataset.")

    # Auto-load from ./data/ folder
    local_csvs = sorted(glob.glob("./data/*.csv"))
    if local_csvs and st.session_state.df is None:
        st.markdown(f'<div style="font-family:\'Share Tech Mono\',monospace;font-size:9px;color:#4a6a90;margin-top:6px;">Found {len(local_csvs)} local CSV(s) in ./data/</div>', unsafe_allow_html=True)
        if st.button("⊕ LOAD FROM ./data/"):
            with st.spinner("⚙ LOADING LOCAL FILES…"):
                df_loaded = load_cicids(local_csvs)
            if df_loaded is not None:
                st.session_state.df = df_loaded
                st.session_state.sim_mode = False
                st.success(f"✓ {len(df_loaded):,} records loaded")

    st.divider()

    # Page navigation
    st.markdown('<div style="font-family:\'Share Tech Mono\',monospace;font-size:9px;letter-spacing:3px;color:#4a6a90;margin-bottom:8px;">NAVIGATION</div>', unsafe_allow_html=True)
    page = st.radio("", ["DASHBOARD", "ANALYSIS", "UNBLOCK MANAGER"], label_visibility="collapsed")

    st.divider()

    # Log filter
    if page == "DASHBOARD":
        st.markdown('<div style="font-family:\'Share Tech Mono\',monospace;font-size:9px;letter-spacing:3px;color:#4a6a90;margin-bottom:8px;">LOG FILTER</div>', unsafe_allow_html=True)
        log_filter = st.selectbox("", ["ALL","CRITICAL","WARNING","INFO"], label_visibility="collapsed")
    else:
        log_filter = "ALL"

    # Auto-refresh
    st.divider()
    st.markdown('<div style="font-family:\'Share Tech Mono\',monospace;font-size:9px;letter-spacing:3px;color:#4a6a90;margin-bottom:8px;">AUTO REFRESH</div>', unsafe_allow_html=True)
    auto_refresh = st.toggle("Enable auto-refresh", value=False)
    refresh_interval = st.slider("Interval (sec)", 2, 30, 5) if auto_refresh else 5

    st.divider()
    st.markdown('<div style="font-family:\'Share Tech Mono\',monospace;font-size:9px;letter-spacing:3px;color:#4a6a90;">v3.1.4 — CLASSIFIED</div>', unsafe_allow_html=True)

# ─────────────────────────────────────────────────────────────
# DATA SELECTION
# ─────────────────────────────────────────────────────────────
use_sim = st.session_state.sim_mode or st.session_state.df is None
df = st.session_state.df if not use_sim else None

# Sim mode banner
if use_sim:
    st.markdown("""
    <div style="background:rgba(0,255,157,.05);border:1px solid rgba(0,255,157,.15);
                border-radius:3px;padding:7px 16px;margin-bottom:16px;
                display:flex;align-items:center;gap:12px;
                font-family:'Share Tech Mono',monospace;font-size:10px;letter-spacing:3px;color:#2a9968;">
      <div style="width:6px;height:6px;border-radius:50%;background:#00ff9d;box-shadow:0 0 6px #00ff9d;"></div>
      SIMULATION MODE ACTIVE — Synthetically generated data for demonstration
      <div style="width:6px;height:6px;border-radius:50%;background:#00ff9d;box-shadow:0 0 6px #00ff9d;"></div>
    </div>""", unsafe_allow_html=True)
else:
    n_attacks = (df["Label"] != "BENIGN").sum()
    st.markdown(f"""
    <div style="background:rgba(0,212,255,.05);border:1px solid rgba(0,212,255,.15);
                border-radius:3px;padding:7px 16px;margin-bottom:16px;
                display:flex;align-items:center;gap:12px;
                font-family:'Share Tech Mono',monospace;font-size:10px;letter-spacing:3px;color:#2a8aaa;">
      <div style="width:6px;height:6px;border-radius:50%;background:#00d4ff;box-shadow:0 0 6px #00d4ff;"></div>
      LIVE DATA MODE — {len(df):,} records · {n_attacks:,} attack flows · {df["Label"].nunique()} classes
      <div style="width:6px;height:6px;border-radius:50%;background:#00d4ff;box-shadow:0 0 6px #00d4ff;"></div>
    </div>""", unsafe_allow_html=True)

# ─────────────────────────────────────────────────────────────
# PAGE: DASHBOARD
# ─────────────────────────────────────────────────────────────
if page == "DASHBOARD":

    # Metrics
    metrics = sim_metrics() if use_sim else compute_real_metrics(df)

    section_title("OPERATIONAL METRICS")
    c1, c2, c3, c4 = st.columns(4)
    with c1:
        st.metric("ACTIVE ALERTS", f"{metrics['active_alerts']:,}", "+12% vs last hour")
    with c2:
        st.metric("BLOCKED IPs", f"{metrics['blocked_ips']:,}", "+8 in last 5 min")
    with c3:
        st.metric("ANOMALOUS EVENTS", f"{metrics['anomalous']:,}",
                  f"−3% vs baseline" if use_sim else f"{metrics['total_flows']:,} total flows")
    with c4:
        st.metric("NETWORK LOAD", f"{metrics['net_load']}%",
                  "Stable" if metrics['net_load'] < 70 else "⚠ Elevated")

    st.divider()

    # AI Engine + Donut
    col_ai, col_donut = st.columns([2, 1])

    with col_ai:
        section_title("AI THREAT ENGINE")

        mode_choice = st.selectbox(
            "Analysis Mode",
            ["All Traffic","Login Attacks","Network Attacks","Port Scans","Malware"],
            label_visibility="collapsed"
        )

        conf = random.randint(80, 96) if use_sim else random.randint(85, 99)

        # AI boxes
        threat_ip = f"192.168.{random.randint(0,5)}.{random.randint(1,254)}" if use_sim else \
                    (df[df["Label"] != "BENIGN"]["Destination Port"].iloc[0]
                     if len(df[df["Label"] != "BENIGN"]) > 0 else "—")
        attempts  = random.randint(100, 999) if use_sim else int((df["Label"] != "BENIGN").sum())
        attack_type = mode_choice if use_sim else \
                      (df["Label"].value_counts().index[1] if len(df["Label"].value_counts()) > 1 else "DDoS")

        st.markdown(f"""
        <div style="border:1px solid #ff3b5c;border-radius:3px;padding:16px;margin-bottom:12px;position:relative;">
          <span style="position:absolute;top:-10px;left:12px;background:#070d18;padding:0 8px;
                       font-size:10px;letter-spacing:3px;font-family:'Share Tech Mono',monospace;color:#ff3b5c;">THREAT DETECTED</span>
          <p style="font-family:'Rajdhani',sans-serif;font-size:14px;color:#c8dff5;margin:0;">
            Attack Type: <strong style="color:#ff3b5c;">{attack_type}</strong>
          </p>
          <p style="font-family:'Rajdhani',sans-serif;font-size:14px;color:#c8dff5;margin:8px 0 6px;">
            Confidence: <strong style="color:#ffb830;">{conf}%</strong>
          </p>
          <div style="height:4px;background:#2a4060;border-radius:2px;overflow:hidden;">
            <div style="width:{conf}%;height:100%;background:linear-gradient(90deg,#ff3b5c,#ffb830);border-radius:2px;"></div>
          </div>
        </div>
        <div style="border:1px solid #ffb830;border-radius:3px;padding:16px;margin-bottom:12px;position:relative;">
          <span style="position:absolute;top:-10px;left:12px;background:#070d18;padding:0 8px;
                       font-size:10px;letter-spacing:3px;font-family:'Share Tech Mono',monospace;color:#ffb830;">AUTOMATED RESPONSE</span>
          <p style="font-family:'Rajdhani',sans-serif;font-size:13px;color:#c8dff5;margin:0;line-height:1.6;">
            IP automatically blocked — ACL rule applied at perimeter firewall.
            Admin notified via SIEM alert <strong style="color:#ffb830;">#{'%04d'%random.randint(1000,9999)}</strong>.
          </p>
        </div>
        <div style="border:1px solid #00ff9d;border-radius:3px;padding:16px;margin-bottom:12px;position:relative;">
          <span style="position:absolute;top:-10px;left:12px;background:#070d18;padding:0 8px;
                       font-size:10px;letter-spacing:3px;font-family:'Share Tech Mono',monospace;color:#00ff9d;">AI EXPLANATION</span>
          <p style="font-family:'Rajdhani',sans-serif;font-size:13px;color:#c8dff5;margin:0;line-height:1.6;">
            Detected statistically anomalous request pattern — deviation 6.2σ above baseline.
            Matching known signature <strong style="color:#00ff9d;">CVE-2024-3182</strong>.
          </p>
        </div>
        <div style="display:grid;grid-template-columns:1fr 1fr;gap:10px;">
          <div style="background:rgba(0,0,0,.4);border:1px solid #0e2040;border-radius:3px;padding:12px;">
            <div style="font-family:'Share Tech Mono',monospace;font-size:10px;letter-spacing:2px;color:#4a6a90;">THREAT IP</div>
            <div style="font-family:'Orbitron',monospace;font-size:13px;color:#00d4ff;margin-top:4px;">{threat_ip}</div>
          </div>
          <div style="background:rgba(0,0,0,.4);border:1px solid #0e2040;border-radius:3px;padding:12px;">
            <div style="font-family:'Share Tech Mono',monospace;font-size:10px;letter-spacing:2px;color:#4a6a90;">GEO ORIGIN</div>
            <div style="font-family:'Orbitron',monospace;font-size:13px;color:#00d4ff;margin-top:4px;">UNKNOWN</div>
          </div>
          <div style="background:rgba(0,0,0,.4);border:1px solid #0e2040;border-radius:3px;padding:12px;">
            <div style="font-family:'Share Tech Mono',monospace;font-size:10px;letter-spacing:2px;color:#4a6a90;">FIRST SEEN</div>
            <div style="font-family:'Orbitron',monospace;font-size:13px;color:#00d4ff;margin-top:4px;">{datetime.now().strftime('%H:%M:%S')}</div>
          </div>
          <div style="background:rgba(0,0,0,.4);border:1px solid #0e2040;border-radius:3px;padding:12px;">
            <div style="font-family:'Share Tech Mono',monospace;font-size:10px;letter-spacing:2px;color:#4a6a90;">ATTEMPTS</div>
            <div style="font-family:'Orbitron',monospace;font-size:13px;color:#00d4ff;margin-top:4px;">{attempts:,}</div>
          </div>
        </div>
        """, unsafe_allow_html=True)

        # Incident Response buttons
        st.divider()
        section_title("INCIDENT RESPONSE")
        bc1, bc2, bc3, bc4 = st.columns(4)
        with bc1:
            if st.button("⚑ REQUEST INVESTIGATION"):
                ticket = f"INC-{random.randint(1000,9999)}"
                st.session_state.investigations.append({
                    "id": ticket, "ip": str(threat_ip), "type": attack_type,
                    "analyst": random.choice(["J.MORRIS","R.CHEN","A.PATEL","K.OKAFOR"]),
                    "time": datetime.now().strftime("%H:%M:%S"), "status": "OPEN"
                })
                st.success(f"◈ Ticket {ticket} opened")
        with bc2:
            if st.button("⊗ FORCE LOCKDOWN"):
                st.error("⊗ LOCKDOWN INITIATED — Perimeter ACLs enforced.")
        with bc3:
            if st.button("◈ GENERATE REPORT"):
                st.warning(f"◈ Report RPT-{random.randint(1000,9999)} queued.")
        with bc4:
            if st.button("▲ ESCALATE TO SOC"):
                st.info("▲ Priority 1 alert raised via PagerDuty.")

    with col_donut:
        section_title("THREAT DISTRIBUTION")
        if use_sim:
            dist = sim_threat_dist()
        else:
            dist = df[df["Label"] != "BENIGN"]["Label"].value_counts()
        st.plotly_chart(chart_threat_donut(dist), use_container_width=True, config={"displayModeBar": False})

    st.divider()

    # Network Performance
    section_title("NETWORK PERFORMANCE")
    st.plotly_chart(chart_net_performance(), use_container_width=True, config={"displayModeBar": False})

    st.divider()

    # Traffic timeseries (real data) / Speed panel
    col_speed, col_ntp = st.columns(2)

    with col_speed:
        section_title("LIVE DATA THROUGHPUT")
        up, dn = sim_speed()
        st.session_state.up_hist.append(up); st.session_state.up_hist = st.session_state.up_hist[-60:]
        st.session_state.dn_hist.append(dn); st.session_state.dn_hist = st.session_state.dn_hist[-60:]
        st.session_state.peak_up = max(st.session_state.peak_up, up)
        st.session_state.peak_dn = max(st.session_state.peak_dn, dn)
        st.session_state.total_up += up * 1e6 / 8 / 1e9 / 7200
        st.session_state.total_dn += dn * 1e6 / 8 / 1e9 / 7200

        sc1, sc2 = st.columns(2)
        with sc1:
            st.markdown(f"""
            <div style="background:rgba(0,0,0,.35);border:1px solid #0e2040;border-radius:4px;padding:16px;">
              <div style="font-family:'Share Tech Mono',monospace;font-size:11px;letter-spacing:3px;color:#00ff9d;">▲ SEND</div>
              <div style="font-family:'Orbitron',monospace;font-size:32px;font-weight:700;color:{'#ff3b5c' if up>120 else '#00ff9d'};">{up:.2f}</div>
              <div style="font-family:'Share Tech Mono',monospace;font-size:10px;letter-spacing:2px;color:#4a6a90;margin-bottom:8px;">Mbps</div>
              <div style="height:4px;background:#2a4060;border-radius:2px;overflow:hidden;">
                <div style="width:{min(up/150*100,100):.1f}%;height:100%;background:#00ff9d;border-radius:2px;"></div>
              </div>
              <div style="font-family:'Share Tech Mono',monospace;font-size:10px;color:#4a6a90;margin-top:6px;">Total: {st.session_state.total_up:.3f} GB</div>
            </div>""", unsafe_allow_html=True)
        with sc2:
            st.markdown(f"""
            <div style="background:rgba(0,0,0,.35);border:1px solid #0e2040;border-radius:4px;padding:16px;">
              <div style="font-family:'Share Tech Mono',monospace;font-size:11px;letter-spacing:3px;color:#00d4ff;">▼ RECEIVE</div>
              <div style="font-family:'Orbitron',monospace;font-size:32px;font-weight:700;color:{'#ff3b5c' if dn>130 else '#00d4ff'};">{dn:.2f}</div>
              <div style="font-family:'Share Tech Mono',monospace;font-size:10px;letter-spacing:2px;color:#4a6a90;margin-bottom:8px;">Mbps</div>
              <div style="height:4px;background:#2a4060;border-radius:2px;overflow:hidden;">
                <div style="width:{min(dn/150*100,100):.1f}%;height:100%;background:#00d4ff;border-radius:2px;"></div>
              </div>
              <div style="font-family:'Share Tech Mono',monospace;font-size:10px;color:#4a6a90;margin-top:6px;">Total: {st.session_state.total_dn:.3f} GB</div>
            </div>""", unsafe_allow_html=True)

        st.plotly_chart(chart_speed(st.session_state.up_hist, st.session_state.dn_hist),
                        use_container_width=True, config={"displayModeBar": False})

        ps1, ps2, ps3, ps4 = st.columns(4)
        avg_up = sum(st.session_state.up_hist) / len(st.session_state.up_hist)
        avg_dn = sum(st.session_state.dn_hist) / len(st.session_state.dn_hist)
        for col_, lbl, val, c in [
            (ps1, "PEAK ▲", f"{st.session_state.peak_up:.1f} M", ACCENT2),
            (ps2, "AVG ▲",  f"{avg_up:.1f} M", ACCENT2),
            (ps3, "PEAK ▼", f"{st.session_state.peak_dn:.1f} M", ACCENT),
            (ps4, "AVG ▼",  f"{avg_dn:.1f} M", ACCENT),
        ]:
            with col_:
                st.markdown(f"""<div style="background:rgba(0,0,0,.3);border:1px solid #0e2040;border-radius:3px;padding:10px 12px;">
                  <div style="font-family:'Share Tech Mono',monospace;font-size:9px;letter-spacing:2px;color:#4a6a90;">{lbl}</div>
                  <div style="font-family:'Orbitron',monospace;font-size:13px;font-weight:700;color:{c};">{val}</div>
                </div>""", unsafe_allow_html=True)

    with col_ntp:
        section_title("ACTIVE TIME SERVER CLIENTS")
        ntp_df = sim_ntp_clients()
        synced  = (ntp_df["STATUS"] == "SYNCED").sum()
        drifting= (ntp_df["STATUS"] == "DRIFTING").sum()
        offline = (ntp_df["STATUS"] == "OFFLINE").sum()

        st.markdown(f"""
        <div style="display:grid;grid-template-columns:repeat(4,1fr);gap:10px;margin-bottom:14px;">
          <div style="background:rgba(0,0,0,.3);border:1px solid #0e2040;border-radius:3px;padding:10px;text-align:center;">
            <div style="font-family:'Share Tech Mono',monospace;font-size:9px;letter-spacing:2px;color:#4a6a90;">TOTAL</div>
            <div style="font-family:'Orbitron',monospace;font-size:20px;font-weight:700;color:#00ff9d;">{len(ntp_df)}</div>
          </div>
          <div style="background:rgba(0,0,0,.3);border:1px solid #0e2040;border-radius:3px;padding:10px;text-align:center;">
            <div style="font-family:'Share Tech Mono',monospace;font-size:9px;letter-spacing:2px;color:#4a6a90;">SYNCED</div>
            <div style="font-family:'Orbitron',monospace;font-size:20px;font-weight:700;color:#00ff9d;">{synced}</div>
          </div>
          <div style="background:rgba(0,0,0,.3);border:1px solid #0e2040;border-radius:3px;padding:10px;text-align:center;">
            <div style="font-family:'Share Tech Mono',monospace;font-size:9px;letter-spacing:2px;color:#4a6a90;">DRIFTING</div>
            <div style="font-family:'Orbitron',monospace;font-size:20px;font-weight:700;color:#ffb830;">{drifting}</div>
          </div>
          <div style="background:rgba(0,0,0,.3);border:1px solid #0e2040;border-radius:3px;padding:10px;text-align:center;">
            <div style="font-family:'Share Tech Mono',monospace;font-size:9px;letter-spacing:2px;color:#4a6a90;">OFFLINE</div>
            <div style="font-family:'Orbitron',monospace;font-size:20px;font-weight:700;color:#ff3b5c;">{offline}</div>
          </div>
        </div>""", unsafe_allow_html=True)

        render_ntp_table(ntp_df)
        st.markdown('<div style="font-family:\'Share Tech Mono\',monospace;font-size:9px;letter-spacing:2px;color:#4a6a90;margin-top:12px;margin-bottom:6px;">OFFSET DISTRIBUTION</div>', unsafe_allow_html=True)
        st.plotly_chart(chart_offset_dist(ntp_df), use_container_width=True, config={"displayModeBar": False})

    st.divider()

    # Security Event Log
    section_title("LIVE SECURITY EVENT LOG")
    if use_sim:
        log_df = sim_log_rows(50)
    else:
        sample_size = min(500, len(df))
        sample_df = df.sample(sample_size, random_state=random.randint(0, 10000))
        log_df = pd.DataFrame({
            "SEVERITY":   sample_df["Severity"],
            "TIMESTAMP":  datetime.now().strftime("%H:%M:%S"),
            "EVENT TYPE": sample_df["Label"],
            "SOURCE IP":  [f"{random.randint(1,223)}.{random.randint(0,255)}.{random.randint(0,255)}.{random.randint(1,254)}" for _ in range(len(sample_df))],
            "DESTINATION":sample_df.get("Destination Port", pd.Series(["10.0.0.1"]*len(sample_df))).astype(str),
            "PROTOCOL":   sample_df["Protocol_Name"],
            "ACTION":     sample_df["Action"],
            "PORT":       sample_df.get("Destination Port", pd.Series([80]*len(sample_df))),
        }).reset_index(drop=True)

    if log_filter != "ALL":
        log_df = log_df[log_df["SEVERITY"] == log_filter]

    render_log_table(log_df)

    # Status bar
    st.divider()
    st.markdown(f"""
    <div style="display:flex;align-items:center;gap:32px;padding:12px 20px;
                background:#070d18;border:1px solid #0e2040;border-radius:4px;
                font-family:'Share Tech Mono',monospace;font-size:11px;color:#4a6a90;letter-spacing:2px;">
      <div style="display:flex;align-items:center;gap:8px;">
        <div style="width:6px;height:6px;border-radius:50%;background:#00ff9d;box-shadow:0 0 6px #00ff9d;"></div>
        AEGIS ENGINE ONLINE
      </div>
      <div style="display:flex;align-items:center;gap:8px;">
        <div style="width:6px;height:6px;border-radius:50%;background:#00ff9d;box-shadow:0 0 6px #00ff9d;"></div>
        LOG PROCESSOR ACTIVE
      </div>
      <div style="display:flex;align-items:center;gap:8px;">
        <div style="width:6px;height:6px;border-radius:50%;background:#ffb830;box-shadow:0 0 6px #ffb830;"></div>
        3 AGENTS ELEVATED
      </div>
      <div style="display:flex;align-items:center;gap:8px;">
        <div style="width:6px;height:6px;border-radius:50%;background:#00ff9d;box-shadow:0 0 6px #00ff9d;"></div>
        SOC DASHBOARD SYNCED
      </div>
      <div style="margin-left:auto;">v3.1.4 — CLASSIFIED</div>
    </div>""", unsafe_allow_html=True)

# ─────────────────────────────────────────────────────────────
# PAGE: ANALYSIS
# ─────────────────────────────────────────────────────────────
elif page == "ANALYSIS":
    section_title("DEEP THREAT ANALYSIS")

    if use_sim:
        st.info("⚡ Simulation mode — upload CICIDS2017 CSV files to see real analysis.")
        dist = sim_threat_dist()
        col1, col2 = st.columns(2)
        with col1:
            section_title("ATTACK DISTRIBUTION")
            st.plotly_chart(chart_attack_bar(dist), use_container_width=True, config={"displayModeBar": False})
        with col2:
            section_title("THREAT DONUT")
            st.plotly_chart(chart_threat_donut(dist), use_container_width=True, config={"displayModeBar": False})
    else:
        # Attack type filter
        all_labels = sorted(df["Label"].unique().tolist())
        selected_labels = st.multiselect(
            "Filter attack types", all_labels, default=all_labels,
            label_visibility="collapsed"
        )
        df_filtered = df[df["Label"].isin(selected_labels)] if selected_labels else df

        # Row 1: attack bar + donut
        col1, col2 = st.columns(2)
        with col1:
            section_title("ATTACK DISTRIBUTION")
            dist = df_filtered["Label"].value_counts()
            st.plotly_chart(chart_attack_bar(dist), use_container_width=True, config={"displayModeBar": False})
        with col2:
            section_title("THREAT DONUT")
            st.plotly_chart(chart_threat_donut(dist), use_container_width=True, config={"displayModeBar": False})

        st.divider()

        # Row 2: flow bytes + protocol pie
        col3, col4 = st.columns(2)
        with col3:
            section_title("FLOW BYTES/S BY ATTACK TYPE")
            fig_fb = chart_flow_bytes(df_filtered)
            if fig_fb:
                st.plotly_chart(fig_fb, use_container_width=True, config={"displayModeBar": False})
            else:
                st.caption("Flow Bytes/s column not available.")
        with col4:
            section_title("PROTOCOL DISTRIBUTION")
            st.plotly_chart(chart_protocol_pie(df_filtered), use_container_width=True, config={"displayModeBar": False})

        st.divider()

        # Row 3: port heatmap + feature importance
        col5, col6 = st.columns(2)
        with col5:
            section_title("ATTACK × DESTINATION PORT HEATMAP")
            fig_ph = chart_port_heatmap(df_filtered)
            if fig_ph:
                st.plotly_chart(fig_ph, use_container_width=True, config={"displayModeBar": False})
            else:
                st.caption("Destination Port column not found.")
        with col6:
            section_title("TOP DISCRIMINATING FEATURES")
            fig_fi = chart_feature_importance(df_filtered)
            if fig_fi:
                st.plotly_chart(fig_fi, use_container_width=True, config={"displayModeBar": False})
            else:
                st.caption("Not enough numeric columns for feature importance.")

        st.divider()

        # Summary stats table
        section_title("ATTACK SUMMARY STATISTICS")
        summary = df_filtered.groupby("Label").agg(
            Count=("Label","count"),
            Severity=("Severity","first"),
            Action=("Action","first"),
        ).reset_index().sort_values("Count", ascending=False)

        # Style dataframe
        def style_row(row):
            c = {"CRITICAL":"#3d0a0f","WARNING":"#2e1f00","INFO":"#001525"}.get(row["Severity"],"#04080f")
            return [f"background:{c}" for _ in row]

        styled = summary.style.apply(style_row, axis=1).format({"Count": "{:,}"})
        st.dataframe(styled, use_container_width=True, height=300)

# ─────────────────────────────────────────────────────────────
# PAGE: UNBLOCK MANAGER
# ─────────────────────────────────────────────────────────────
elif page == "UNBLOCK MANAGER":
    col_alerts, col_manager, col_agents = st.columns([1, 2, 1])

    # ── LEFT: Active Alerts ──
    with col_alerts:
        section_title("ACTIVE ALERTS")
        alerts_data = []
        alert_types = [
            ("Brute Force Login","CRITICAL"), ("DDoS Flood Detected","CRITICAL"),
            ("SQL Injection","CRITICAL"),     ("Port Scan Sweep","WARNING"),
            ("Anomalous DNS Query","WARNING"), ("Lateral Movement","CRITICAL"),
            ("Malware Beacon","CRITICAL"),     ("Auth Failure","WARNING"),
        ]
        for _ in range(16):
            at, sev = random.choice(alert_types)
            alerts_data.append({"type": at, "sev": sev,
                "ip": f"{random.randint(1,223)}.{random.randint(0,255)}.{random.randint(0,255)}.{random.randint(1,254)}",
                "time": datetime.now().strftime("%H:%M:%S")})

        crits = sum(1 for a in alerts_data if a["sev"] == "CRITICAL")
        warns = sum(1 for a in alerts_data if a["sev"] == "WARNING")

        ac1, ac2 = st.columns(2)
        with ac1:
            st.markdown(f'<div style="background:rgba(255,59,92,.06);border:1px solid rgba(255,59,92,.25);border-radius:3px;padding:10px;text-align:center;"><div style="font-family:\'Orbitron\',monospace;font-size:22px;font-weight:700;color:#904050;">{crits}</div><div style="font-family:\'Share Tech Mono\',monospace;font-size:9px;letter-spacing:2px;color:#4a6a90;">CRITICAL</div></div>', unsafe_allow_html=True)
        with ac2:
            st.markdown(f'<div style="background:rgba(255,184,48,.06);border:1px solid rgba(255,184,48,.25);border-radius:3px;padding:10px;text-align:center;"><div style="font-family:\'Orbitron\',monospace;font-size:22px;font-weight:700;color:#886830;">{warns}</div><div style="font-family:\'Share Tech Mono\',monospace;font-size:9px;letter-spacing:2px;color:#4a6a90;">WARNING</div></div>', unsafe_allow_html=True)

        st.markdown("<div style='height:12px'></div>", unsafe_allow_html=True)
        for a in alerts_data:
            isCrit = a["sev"] == "CRITICAL"
            bc = "rgba(255,59,92,.25)" if isCrit else "rgba(255,184,48,.2)"
            bg = "rgba(255,59,92,.04)" if isCrit else "rgba(255,184,48,.03)"
            tc = "#a84050" if isCrit else "#886830"
            st.markdown(f"""
            <div style="border:1px solid {bc};background:{bg};border-radius:3px;padding:10px 12px;
                        margin-bottom:5px;font-family:'Share Tech Mono',monospace;font-size:10px;">
              <div style="display:flex;justify-content:space-between;margin-bottom:4px;">
                <span style="font-weight:700;color:{tc};">{a['type']}</span>
                <span style="color:#4a6a90;font-size:9px;">{a['time']}</span>
              </div>
              <div style="color:#4a6a90;font-size:9px;">SRC: {a['ip']} · {a['sev']}</div>
            </div>""", unsafe_allow_html=True)

    # ── CENTRE: Unblock Manager ──
    with col_manager:
        section_title("IP UNBLOCK MANAGER")

        st.markdown(f'<div style="font-family:\'Share Tech Mono\',monospace;font-size:10px;letter-spacing:2px;color:#4a6a90;margin-bottom:12px;">{len(st.session_state.blocked_ips)} BLOCKED</div>', unsafe_allow_html=True)

        # Manual unblock input
        ub_col1, ub_col2 = st.columns([3, 1])
        with ub_col1:
            ub_input = st.text_input("IP Address", placeholder="Enter IP to unblock…", label_visibility="collapsed")
        with ub_col2:
            if st.button("⊘ UNBLOCK"):
                import re
                if re.match(r"^(\d{1,3}\.){3}\d{1,3}$", ub_input or ""):
                    idx = next((i for i, e in enumerate(st.session_state.blocked_ips) if e["ip"] == ub_input), None)
                    if idx is not None:
                        removed = st.session_state.blocked_ips.pop(idx)
                        st.success(f"✓ {removed['ip']} unblocked — ACL rule removed.")
                    else:
                        st.error(f"✗ {ub_input} not found in blocklist.")
                else:
                    st.warning("⚠ Enter a valid IPv4 address.")

        # Filter tabs
        ub_filter = st.selectbox(
            "Filter", ["ALL","DDoS Flood","Brute Force Login","SQL Injection","Port Scan","Malware Beacon","Credential Stuffing"],
            label_visibility="collapsed"
        )
        filtered_blocked = st.session_state.blocked_ips if ub_filter == "ALL" else \
                           [e for e in st.session_state.blocked_ips if e["reason"] == ub_filter]

        render_blocked_table(filtered_blocked)

        # Per-row unblock buttons
        if filtered_blocked:
            st.markdown("<div style='height:8px'></div>", unsafe_allow_html=True)
            for i, entry in enumerate(filtered_blocked):
                if st.button(f"✓ Unblock {entry['ip']}", key=f"ub_{i}_{entry['ip']}"):
                    real_idx = next((j for j, e in enumerate(st.session_state.blocked_ips) if e["ip"] == entry["ip"]), None)
                    if real_idx is not None:
                        st.session_state.blocked_ips.pop(real_idx)
                        st.success(f"✓ {entry['ip']} unblocked.")
                        st.rerun()

        st.divider()

        # Bulk actions
        bc1, bc2 = st.columns(2)
        with bc1:
            if st.button("⊘ CLEAR PORT SCANS"):
                before = len(st.session_state.blocked_ips)
                st.session_state.blocked_ips = [e for e in st.session_state.blocked_ips if e["reason"] != "Port Scan"]
                st.success(f"✓ {before - len(st.session_state.blocked_ips)} Port Scan IPs cleared.")
                st.rerun()
        with bc2:
            if st.button("⊘ UNBLOCK ALL"):
                count = len(st.session_state.blocked_ips)
                st.session_state.blocked_ips = []
                st.success(f"✓ All {count} IPs unblocked.")
                st.rerun()

        # Investigation tickets
        if st.session_state.investigations:
            st.divider()
            section_title("ACTIVE INVESTIGATION TICKETS")
            for t in st.session_state.investigations:
                st.markdown(f"""
                <div style="padding:12px 14px;border:1px solid rgba(0,212,255,.2);
                            border-left:2px solid rgba(0,212,255,.5);border-radius:3px;
                            background:rgba(0,212,255,.04);margin-bottom:6px;
                            font-family:'Share Tech Mono',monospace;font-size:11px;
                            display:flex;gap:16px;align-items:center;">
                  <span style="color:#2a8aaa;font-weight:700;min-width:90px">{t['id']}</span>
                  <span style="color:#c8dff5;flex:1">{t['type']} — <span style="color:#a84050">{t['ip']}</span></span>
                  <span style="color:#4a6a90;">Analyst: {t['analyst']}</span>
                  <span style="color:#4a6a90;">{t['time']}</span>
                  <span style="padding:2px 8px;border-radius:2px;border:1px solid rgba(0,212,255,.3);
                               color:#2a8aaa;background:rgba(0,212,255,.08);font-size:9px;letter-spacing:2px;">{t['status']}</span>
                </div>""", unsafe_allow_html=True)

    # ── RIGHT: Active Agents ──
    with col_agents:
        section_title("ACTIVE AGENTS")
        AGENTS = [
            ("SENTINEL-01","Intrusion Detection",  72, 14),
            ("GUARDIAN-02","Firewall Manager",      48, 8),
            ("ORACLE-03",  "Log Analyzer",          91, 31),
            ("WARDEN-04",  "ACL Controller",        33, 5),
            ("NEXUS-05",   "Threat Intelligence",   60, 18),
            ("CIPHER-06",  "Packet Inspector",      85, 22),
            ("AEGIS-07",   "AI Threat Engine",      55, 11),
            ("RECON-08",   "Port Monitor",          20, 3),
        ]
        agents = [{"name":n,"role":r,
                   "load": min(98, max(5, l + random.randint(-8, 8))),
                   "tasks": max(0, t + random.randint(-2, 3))}
                  for n,r,l,t in AGENTS]
        for a in agents:
            a["status"] = "BUSY" if a["load"] > 82 else "OFFLINE" if a["load"] < 8 else "ONLINE"

        online  = sum(1 for a in agents if a["status"] == "ONLINE")
        busy    = sum(1 for a in agents if a["status"] == "BUSY")
        offline = sum(1 for a in agents if a["status"] == "OFFLINE")

        ag1, ag2, ag3 = st.columns(3)
        for col_, lbl, val, col_c in [
            (ag1,"ONLINE",online,"rgba(0,255,157,.2)"),
            (ag2,"BUSY",  busy,  "rgba(255,184,48,.2)"),
            (ag3,"OFFLINE",offline,"rgba(255,59,92,.2)"),
        ]:
            with col_:
                vc = "#2a9968" if lbl=="ONLINE" else "#886830" if lbl=="BUSY" else "#904050"
                st.markdown(f'<div style="background:{col_c};border-radius:3px;padding:8px;text-align:center;"><div style="font-family:\'Orbitron\',monospace;font-size:18px;font-weight:700;color:{vc};">{val}</div><div style="font-family:\'Share Tech Mono\',monospace;font-size:8px;letter-spacing:2px;color:#4a6a90;">{lbl}</div></div>', unsafe_allow_html=True)

        st.markdown("<div style='height:10px'></div>", unsafe_allow_html=True)

        for a in agents:
            sc = {"ONLINE":"#2a9968","BUSY":"#886830","OFFLINE":"#904050"}[a["status"]]
            sbg= {"ONLINE":"rgba(0,255,157,.1)","BUSY":"rgba(255,184,48,.1)","OFFLINE":"rgba(255,59,92,.1)"}[a["status"]]
            bar_c = "#904050" if a["load"]>80 else "#886830" if a["load"]>60 else "#2a9968"
            st.markdown(f"""
            <div style="padding:10px 12px;border:1px solid #0e2040;border-radius:3px;
                        background:rgba(0,0,0,.25);margin-bottom:6px;">
              <div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:5px;">
                <span style="font-family:'Orbitron',monospace;font-size:10px;color:#c8dff5;letter-spacing:1px;">{a['name']}</span>
                <span style="background:{sbg};color:{sc};border:1px solid {sc}40;padding:1px 7px;
                             border-radius:2px;font-family:'Share Tech Mono',monospace;font-size:8px;letter-spacing:2px;">{a['status']}</span>
              </div>
              <div style="font-family:'Share Tech Mono',monospace;font-size:9px;color:#4a6a90;line-height:1.7;">
                {a['role']}<br>LOAD: {a['load']}% · TASKS: {a['tasks']}
              </div>
              <div style="height:3px;background:#2a4060;border-radius:2px;margin-top:7px;overflow:hidden;">
                <div style="width:{a['load']}%;height:100%;background:{bar_c};border-radius:2px;"></div>
              </div>
            </div>""", unsafe_allow_html=True)

# ─────────────────────────────────────────────────────────────
# AUTO REFRESH
# ─────────────────────────────────────────────────────────────
if auto_refresh:
    time.sleep(refresh_interval)
    st.rerun()
