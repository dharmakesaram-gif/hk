import streamlit as st
import pandas as pd
import random
import plotly.graph_objects as go
from datetime import datetime
from streamlit_autorefresh import st_autorefresh

# ------------------------------------
# AUTO REFRESH
# ------------------------------------

st_autorefresh(interval=3000, key="refresh")

st.set_page_config(
    page_title="AI Cyber Defense System",
    page_icon="🛡️",
    layout="wide"
)

# ------------------------------------
# DARK DASHBOARD STYLE
# ------------------------------------

st.markdown("""
<style>

.stApp {
    background-color:#000000;
    color:white;
}

[data-testid="stSidebar"]{
    background-color:#000000;
}

[data-testid="stMetric"]{
    background-color:#111111;
    padding:25px;
    border-radius:12px;
    border:1px solid #222;
    font-size:20px;
}

div.stButton > button{
    background:#0d1117;
    border:1px solid #333;
    color:white;
    padding:10px 25px;
    border-radius:8px;
}

</style>
""", unsafe_allow_html=True)

# ------------------------------------
# HEADER + SYSTEM STATUS
# ------------------------------------

left, right = st.columns([3,1])

with left:
    st.title("🛡️ Multi-Agent Cybersecurity Defense System")
    st.caption("Real-time Threat Monitoring & Automated Response")

with right:

    r1,r2 = st.columns(2)

    with r1:
        st.metric("System Health","Healthy")

    with r2:
        st.metric("Threat Level","HIGH","↑12%")

st.markdown("---")

# ------------------------------------
# THREAT MODE BUTTONS
# ------------------------------------

st.subheader("Threat Analysis Mode")

b1,b2,b3,b4,b5 = st.columns(5)

if "mode" not in st.session_state:
    st.session_state.mode="All Traffic"

if b1.button("All Traffic"):
    st.session_state.mode="All Traffic"

if b2.button("Login Attacks"):
    st.session_state.mode="Login Attack"

if b3.button("Network Attacks"):
    st.session_state.mode="Network Attack"

if b4.button("Port Scans"):
    st.session_state.mode="Port Scan"

if b5.button("Malware"):
    st.session_state.mode="Malware Activity"

mode=st.session_state.mode

st.markdown("---")

# ------------------------------------
# METRIC PANELS
# ------------------------------------

c1,c2,c3,c4 = st.columns(4)

c1.metric("Active Alerts",random.randint(10,30))
c2.metric("Blocked IPs",random.randint(20,70))
c3.metric("Anomalous Events",random.randint(5,20))
c4.metric("Network Load",f"{random.randint(30,80)}%")

st.markdown("---")

# ------------------------------------
# AI THREAT ANALYSIS
# ------------------------------------

col1,col2=st.columns(2)

with col1:

    st.subheader("🧠 AI Threat Analysis")

    st.info(f"""
Threat detected  
Attack type: {mode}  
Confidence: {random.randint(80,95)}%
""")

    st.warning("""
System Response  
IP automatically blocked  
Admin alerted
""")

    st.success("""
AI Explanation  
Detected abnormal pattern matching attack behaviour.
""")

    threat_ip=f"192.168.1.{random.randint(1,255)}"

    a,b=st.columns(2)

    with a:
        st.metric("Threat IP",threat_ip)

    with b:
        st.metric("Location","Unknown")

# ------------------------------------
# THREAT DISTRIBUTION
# ------------------------------------

with col2:

    st.subheader("⚠️ Threat Distribution")

    labels=["DDoS","Brute Force","Malware","Port Scan","Phishing"]
    values=[random.randint(5,40) for _ in labels]

    fig=go.Figure(data=[go.Pie(labels=labels,values=values,hole=.5)])

    fig.update_layout(
        template="plotly_dark",
        paper_bgcolor="#000000",
        plot_bgcolor="#000000",
        height=350
    )

    st.plotly_chart(fig,use_container_width=True)

st.markdown("---")

# ------------------------------------
# NETWORK PERFORMANCE GRAPH
# ------------------------------------

st.subheader("🌐 Network Performance Monitoring")

time=list(range(40))

latency=[random.randint(10,80) for _ in time]
error=[random.uniform(0,1) for _ in time]
request=[random.uniform(0,3) for _ in time]
duration=[random.randint(1,15) for _ in time]

fig=go.Figure()

fig.add_trace(go.Scatter(x=time,y=latency,mode="lines",name="Latency",line=dict(color="#FFA500",width=3)))
fig.add_trace(go.Scatter(x=time,y=error,mode="lines",name="Error Ratio",line=dict(color="#FF2D55",width=3)))
fig.add_trace(go.Scatter(x=time,y=request,mode="lines",name="Request Rate",line=dict(color="#00FFFF",width=3)))
fig.add_trace(go.Scatter(x=time,y=duration,mode="lines",name="Connection Duration",line=dict(color="#00FF7F",width=3)))

fig.update_layout(
    template="plotly_dark",
    paper_bgcolor="#000000",
    plot_bgcolor="#000000",
    height=400
)

st.plotly_chart(fig,use_container_width=True)

st.markdown("---")

# ------------------------------------
# SECURITY ARCHITECTURE MAP
# ------------------------------------

st.subheader("🗺️ Security Infrastructure Architecture")

nodes=[
"🌐 Internet",
"🛡️ Firewall",
"🔀 API Gateway",
"🖥️ Web Server",
"🤖 AI Threat Engine",
"📜 Log Processor",
"🗄️ Security DB",
"📊 SOC Dashboard"
]

positions={
"🌐 Internet":(0,4),
"🛡️ Firewall":(1,3),
"🔀 API Gateway":(2,3),
"🖥️ Web Server":(3,3),
"🤖 AI Threat Engine":(3,2),
"📜 Log Processor":(2,1),
"🗄️ Security DB":(3,1),
"📊 SOC Dashboard":(4,2)
}

colors={
"🌐 Internet":"#888",
"🛡️ Firewall":"#FF4B4B",
"🔀 API Gateway":"#1F77B4",
"🖥️ Web Server":"#1F77B4",
"🤖 AI Threat Engine":"#00FFAA",
"📜 Log Processor":"#FFB347",
"🗄️ Security DB":"#B19CD9",
"📊 SOC Dashboard":"#00FFFF"
}

fig=go.Figure()

for node,(x,y) in positions.items():

    fig.add_trace(go.Scatter(
        x=[x],y=[y],
        mode="markers+text",
        text=[node],
        textposition="bottom center",
        marker=dict(size=45,color=colors[node],line=dict(width=2,color="white")),
        hoverinfo="text"
    ))

connections=[
("🌐 Internet","🛡️ Firewall"),
("🛡️ Firewall","🔀 API Gateway"),
("🔀 API Gateway","🖥️ Web Server"),
("🖥️ Web Server","🤖 AI Threat Engine"),
("🤖 AI Threat Engine","📜 Log Processor"),
("📜 Log Processor","🗄️ Security DB"),
("🗄️ Security DB","📊 SOC Dashboard")
]

for a,b in connections:

    x0,y0=positions[a]
    x1,y1=positions[b]

    fig.add_trace(go.Scatter(
        x=[x0,x1],y=[y0,y1],
        mode="lines",
        line=dict(width=3,color="#AAAAAA"),
        hoverinfo="none"
    ))

fig.update_layout(
    template="plotly_dark",
    paper_bgcolor="#000000",
    plot_bgcolor="#000000",
    showlegend=False,
    height=500,
    xaxis=dict(visible=False),
    yaxis=dict(visible=False)
)

st.plotly_chart(fig,use_container_width=True)

st.markdown("---")

# ------------------------------------
# SECURITY LOGS
# ------------------------------------

st.subheader("🖥️ Live Security Log Monitor")

log_rows=100

logs=pd.DataFrame({
"Time":[datetime.now().strftime("%H:%M:%S") for _ in range(log_rows)],
"Event":[random.choice(["Login Attack","Network Attack","Port Scan","Malware Activity"]) for _ in range(log_rows)],
"Source IP":[f"192.168.1.{random.randint(1,255)}" for _ in range(log_rows)],
"Status":[random.choice(["INFO","WARNING","CRITICAL"]) for _ in range(log_rows)]
})

if mode!="All Traffic":
    logs=logs[logs["Event"].str.contains(mode.split()[0],case=False)]

st.dataframe(logs,use_container_width=True,height=400)

st.success("System Operational — All Agents Running")
