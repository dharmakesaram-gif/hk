import streamlit as st
import pandas as pd
import random
import plotly.graph_objects as go
from datetime import datetime
from streamlit_autorefresh import st_autorefresh

# ------------------------------------------------
# AUTO REFRESH
# ------------------------------------------------

st_autorefresh(interval=3000, key="refresh")

st.set_page_config(
    page_title="AI Cyber Defense System",
    page_icon="🛡️",
    layout="wide"
)

# ------------------------------------------------
# BLACK THEME
# ------------------------------------------------

st.markdown("""
<style>

.stApp {
    background-color: #000000;
    color: white;
}

[data-testid="stSidebar"] {
    background-color: #000000;
}

[data-testid="stMetric"] {
    background-color: #111111;
    padding: 10px;
    border-radius: 8px;
}

</style>
""", unsafe_allow_html=True)

# ------------------------------------------------
# HEADER + SYSTEM HEALTH
# ------------------------------------------------

left, right = st.columns([4,1])

with left:
    st.title("🛡️ Multi-Agent Cybersecurity Defense System")

with right:
    st.metric("System Health", "Healthy", "✔")

st.caption("Real-time Threat Monitoring & Automated Response")

st.markdown("---")

# ------------------------------------------------
# THREAT ANALYSIS BUTTONS
# ------------------------------------------------

st.subheader("Threat Analysis Mode")

b1,b2,b3,b4,b5 = st.columns(5)

if "mode" not in st.session_state:
    st.session_state.mode = "All Traffic"

if b1.button("All Traffic"):
    st.session_state.mode = "All Traffic"

if b2.button("Login Attacks"):
    st.session_state.mode = "Login Attack"

if b3.button("Network Attacks"):
    st.session_state.mode = "Network Attack"

if b4.button("Port Scans"):
    st.session_state.mode = "Port Scan"

if b5.button("Malware"):
    st.session_state.mode = "Malware Activity"

mode = st.session_state.mode

st.markdown("---")

# ------------------------------------------------
# METRICS
# ------------------------------------------------

c1,c2,c3,c4 = st.columns(4)

c1.metric("Threat Level","HIGH","↑12%")
c2.metric("Active Alerts",random.randint(10,30))
c3.metric("Blocked IPs",random.randint(20,70))
c4.metric("Anomalous Events",random.randint(5,20))

st.markdown("---")

# ------------------------------------------------
# AI THREAT ANALYSIS + THREAT DISTRIBUTION
# ------------------------------------------------

col1, col2 = st.columns(2)

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

    threat_ip = f"192.168.1.{random.randint(1,255)}"
    location = "Unknown Location"

    a,b = st.columns(2)

    with a:
        st.metric("Threat IP", threat_ip)

    with b:
        st.metric("Location", location)

with col2:

    st.subheader("⚠️ Threat Distribution")

    threat_types = ["DDoS","Brute Force","Malware","Port Scan","Phishing"]
    counts = [random.randint(5,40) for _ in threat_types]

    fig = go.Figure(data=[go.Pie(
        labels=threat_types,
        values=counts,
        hole=.5
    )])

    fig.update_layout(
        template="plotly_dark",
        height=350,
        paper_bgcolor="#000000",
        plot_bgcolor="#000000"
    )

    st.plotly_chart(fig,use_container_width=True)

st.markdown("---")

# ------------------------------------------------
# NETWORK PERFORMANCE GRAPH
# ------------------------------------------------

st.subheader("🌐 Network Performance Monitoring")

time = list(range(40))

latency = [random.randint(10,80) for _ in time]
error = [random.uniform(0,1) for _ in time]
request = [random.uniform(0,3) for _ in time]
duration = [random.randint(1,15) for _ in time]

fig = go.Figure()

fig.add_trace(go.Scatter(
    x=time,y=latency,
    mode='lines',
    name='Latency',
    line=dict(color='#FFA500',width=3)
))

fig.add_trace(go.Scatter(
    x=time,y=error,
    mode='lines',
    name='Error Ratio',
    line=dict(color='#FF2D55',width=3)
))

fig.add_trace(go.Scatter(
    x=time,y=request,
    mode='lines',
    name='Request Rate',
    line=dict(color='#00FFFF',width=3)
))

fig.add_trace(go.Scatter(
    x=time,y=duration,
    mode='lines',
    name='Connection Duration',
    line=dict(color='#00FF7F',width=3)
))

fig.update_layout(
    template="plotly_dark",
    plot_bgcolor="#000000",
    paper_bgcolor="#000000",
    height=400,
    legend=dict(orientation="h",yanchor="bottom",y=1.02,xanchor="right",x=1)
)

st.plotly_chart(fig,use_container_width=True)

st.markdown("---")

# ------------------------------------------------
# SECURITY ARCHITECTURE MAP
# ------------------------------------------------

st.subheader("🗺️ Security Architecture Map")

nodes = [
    "Internet",
    "Firewall",
    "API Gateway",
    "Web Server",
    "AI Threat Engine",
    "Log Processor",
    "Security Database",
    "SOC Dashboard"
]

x = list(range(len(nodes)))
y = [0]*len(nodes)

fig = go.Figure()

fig.add_trace(go.Scatter(
    x=x,
    y=y,
    mode="markers+text",
    text=nodes,
    textposition="top center",
    marker=dict(size=30,color="#00FFFF"),
    hoverinfo="text"
))

connections = [
    (0,1),(1,2),(2,3),(3,4),(4,5),(5,6),(6,7)
]

for start,end in connections:
    fig.add_trace(go.Scatter(
        x=[x[start],x[end]],
        y=[y[start],y[end]],
        mode="lines",
        line=dict(width=3,color="#888"),
        hoverinfo="none"
    ))

fig.update_layout(
    template="plotly_dark",
    plot_bgcolor="#000000",
    paper_bgcolor="#000000",
    showlegend=False,
    height=300,
    xaxis=dict(showgrid=False,visible=False),
    yaxis=dict(showgrid=False,visible=False)
)

st.plotly_chart(fig,use_container_width=True)

st.markdown("---")

# ------------------------------------------------
# LIVE SECURITY LOGS
# ------------------------------------------------

st.subheader("🖥️ Live Security Log Monitor")

log_rows = 100

logs = pd.DataFrame({
    "Time":[datetime.now().strftime("%H:%M:%S") for _ in range(log_rows)],
    "Event":[random.choice([
        "Login Attack",
        "Network Attack",
        "Port Scan",
        "Malware Activity"
    ]) for _ in range(log_rows)],
    "Source IP":[f"192.168.1.{random.randint(1,255)}" for _ in range(log_rows)],
    "Status":[random.choice(["INFO","WARNING","CRITICAL"]) for _ in range(log_rows)]
})

if mode != "All Traffic":
    logs = logs[logs["Event"].str.contains(mode.split()[0], case=False)]

st.dataframe(
    logs,
    use_container_width=True,
    height=400
)

st.success("System Operational — All Agents Running")
