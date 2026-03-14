import streamlit as st
import pandas as pd
import random
import plotly.express as px
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
# FORCE BLACK THEME
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

[data-testid="stHeader"] {
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
# HEADER
# ------------------------------------------------

st.title("🛡️ Multi-Agent Cybersecurity Defense System")
st.caption("Real-time Threat Monitoring & Automated Response")

st.markdown("---")

# ------------------------------------------------
# THREAT MODE SELECTOR
# ------------------------------------------------

mode = st.radio(
    "Threat Analysis Mode",
    ["All Traffic","Login Attacks","Network Attacks","Port Scans","Malware Activity"],
    horizontal=True
)

st.markdown("---")

# ------------------------------------------------
# SIDEBAR
# ------------------------------------------------

st.sidebar.title("System Control")

st.sidebar.success("Network Agent Active")
st.sidebar.success("Log Agent Active")
st.sidebar.success("Behavior Agent Active")
st.sidebar.success("Response Agent Active")

st.sidebar.info(datetime.now().strftime("%Y-%m-%d %H:%M:%S"))

# ------------------------------------------------
# METRICS
# ------------------------------------------------

col1, col2, col3, col4 = st.columns(4)

col1.metric("Threat Level","HIGH","↑ 12%")
col2.metric("Active Alerts",random.randint(10,30))
col3.metric("Blocked IPs",random.randint(20,70))
col4.metric("Anomalous Events",random.randint(5,20))

st.markdown("---")

# ------------------------------------------------
# AI THREAT ANALYSIS + THREAT DISTRIBUTION
# ------------------------------------------------

col1, col2 = st.columns(2)

with col1:

    st.subheader("🧠 AI Threat Analysis")

    logs = [
        "login failed",
        "login failed",
        "login failed",
        "login success"
    ]

    if logs.count("login failed") >= 3:

        st.info("""
Threat detected  
Attack type: Brute Force Login  
Confidence: 91%
""")

        st.warning("""
System Response  
IP automatically blocked  
Admin alerted
""")

        st.success("""
AI Explanation  
Multiple failed login attempts from same IP indicate brute force behaviour.
""")

        threat_ip = "185.23.44.21"
        location = "Moscow, Russia"

        a,b = st.columns(2)

        with a:
            st.metric("Threat IP", threat_ip)

        with b:
            st.metric("Location", location)

    else:
        st.success("No threat detected")

with col2:

    st.subheader("⚠️ Threat Type Distribution")

    threats = pd.DataFrame({
        "Attack Type":["DDoS","Brute Force","Malware","Port Scan","Phishing"],
        "Count":[random.randint(5,40) for _ in range(5)]
    })

    fig = px.pie(threats,names="Attack Type",values="Count",hole=0.5)

    fig.update_layout(
        template="plotly_dark",
        plot_bgcolor="#000000",
        paper_bgcolor="#000000"
    )

    st.plotly_chart(fig,use_container_width=True)

st.markdown("---")

# ------------------------------------------------
# NETWORK PERFORMANCE GRAPH
# ------------------------------------------------

st.subheader("🌐 Network Performance Monitoring")

metric = st.selectbox(
    "Select Network Metric",
    ["Latency","Error Ratio","Request Rate"]
)

if metric == "Latency":

    data = pd.DataFrame({
        "time": range(40),
        "latency":[random.randint(10,80) for _ in range(40)]
    })

    fig = px.line(data,x="time",y="latency")

    fig.update_traces(line=dict(color="#FF8C42",width=3),fill="tozeroy")

    fig.update_layout(
        title="Latency (P95)",
        template="plotly_dark",
        plot_bgcolor="#000000",
        paper_bgcolor="#000000",
        height=300
    )

    st.plotly_chart(fig,use_container_width=True)


elif metric == "Error Ratio":

    data = pd.DataFrame({
        "time": range(40),
        "error":[random.uniform(0,1) for _ in range(40)]
    })

    fig = px.line(data,x="time",y="error")

    fig.update_traces(line=dict(color="#E02F44",width=3),fill="tozeroy")

    fig.update_layout(
        title="Error Ratio",
        template="plotly_dark",
        plot_bgcolor="#000000",
        paper_bgcolor="#000000",
        height=300
    )

    st.plotly_chart(fig,use_container_width=True)


elif metric == "Request Rate":

    data = pd.DataFrame({
        "time": range(40),
        "req":[random.uniform(0,3) for _ in range(40)]
    })

    fig = px.line(data,x="time",y="req")

    fig.update_traces(line=dict(color="#1FC7D4",width=3),fill="tozeroy")

    fig.update_layout(
        title="Request Rate",
        template="plotly_dark",
        plot_bgcolor="#000000",
        paper_bgcolor="#000000",
        height=300
    )

    st.plotly_chart(fig,use_container_width=True)

st.markdown("---")

# ------------------------------------------------
# SERVER INFRASTRUCTURE PANEL
# ------------------------------------------------

st.subheader("🗺️ Server Infrastructure Map")

servers = pd.DataFrame({
    "Server":[
        "Web Server",
        "API Gateway",
        "Authentication Server",
        "Database Server",
        "Firewall",
        "Threat Detection Engine"
    ],
    "Status":[
        "Active",
        "Active",
        "Active",
        "Active",
        "Active",
        "Monitoring"
    ],
    "Load":[random.randint(20,70) for _ in range(6)]
})

st.dataframe(servers,use_container_width=True)

st.markdown("---")

# ------------------------------------------------
# LIVE SECURITY LOGS
# ------------------------------------------------

st.subheader("🖥️ Live Security Log Monitor")

log_rows = 100

logs = pd.DataFrame({
    "Time":[datetime.now().strftime("%H:%M:%S") for _ in range(log_rows)],
    "Event":[
        random.choice([
            "Login Attack",
            "Network Attack",
            "Port Scan",
            "Malware Activity"
        ]) for _ in range(log_rows)
    ],
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
