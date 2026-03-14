import streamlit as st
import pandas as pd
import random
import plotly.express as px
from datetime import datetime
from streamlit_autorefresh import st_autorefresh

# auto refresh
st_autorefresh(interval=3000, key="refresh")

st.set_page_config(
    page_title="AI Cyber Defense System",
    page_icon="🛡️",
    layout="wide"
)

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

st.sidebar.markdown("---")

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

    failed = logs.count("login failed")

    if failed >= 3:

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
Multiple failed login attempts from the same IP indicate brute force behaviour.
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
        "Attack Type":[
            "DDoS",
            "Brute Force",
            "Malware",
            "Port Scan",
            "Phishing"
        ],
        "Count":[random.randint(5,40) for _ in range(5)]
    })

    fig = px.pie(threats,names="Attack Type",values="Count",hole=0.5)

    st.plotly_chart(fig,use_container_width=True)

st.markdown("---")

# ------------------------------------------------
# NETWORK PERFORMANCE SELECTOR
# ------------------------------------------------

st.subheader("🌐 Network Performance Monitoring")

metric = st.selectbox(
    "Select Network Metric",
    ["Latency","Request Rate","Error Ratio","Connection Duration"]
)

if metric == "Latency":

    data = pd.DataFrame({
        "time":range(50),
        "latency":[random.randint(10,120) for _ in range(50)]
    })

    fig = px.line(data,x="time",y="latency",title="Network Latency (ms)")
    st.plotly_chart(fig,use_container_width=True)


elif metric == "Request Rate":

    data = pd.DataFrame({
        "time":range(50),
        "requests":[random.randint(100,900) for _ in range(50)]
    })

    fig = px.line(data,x="time",y="requests",title="Request Rate")
    st.plotly_chart(fig,use_container_width=True)


elif metric == "Error Ratio":

    data = pd.DataFrame({
        "time":range(50),
        "error_ratio":[random.uniform(0,0.2) for _ in range(50)]
    })

    fig = px.line(data,x="time",y="error_ratio",title="Error Ratio")
    st.plotly_chart(fig,use_container_width=True)


elif metric == "Connection Duration":

    data = pd.DataFrame({
        "time":range(50),
        "duration":[random.randint(1,15) for _ in range(50)]
    })

    fig = px.line(data,x="time",y="duration",title="Connection Duration")
    st.plotly_chart(fig,use_container_width=True)

st.markdown("---")

# ------------------------------------------------
# LIVE NETWORK MAP
# ------------------------------------------------

st.subheader("🌍 Live Network Data Transfer Map")

map_data = pd.DataFrame({
    "lat":[37.77,55.75,28.61,35.68],
    "lon":[-122.41,37.61,77.20,139.69],
    "traffic":[random.randint(100,800) for _ in range(4)]
})

st.map(map_data)

st.markdown("---")

# ------------------------------------------------
# LIVE SECURITY LOGS
# ------------------------------------------------

st.subheader("🖥️ Live Security Log Monitor")

logs = pd.DataFrame({
    "Time":[datetime.now().strftime("%H:%M:%S") for _ in range(12)],
    "Event":[
        random.choice([
            "Login Attack",
            "Network Attack",
            "Port Scan",
            "Malware Activity"
        ]) for _ in range(12)
    ],
    "Source IP":[f"192.168.1.{random.randint(1,255)}" for _ in range(12)],
    "Status":[random.choice(["INFO","WARNING","CRITICAL"]) for _ in range(12)]
})

# filter logs based on selected mode

if mode != "All Traffic":
    logs = logs[logs["Event"].str.contains(mode.split()[0], case=False)]

st.dataframe(
    logs,
    use_container_width=True,
    height=300
)

st.success("System Operational — All Agents Running")
