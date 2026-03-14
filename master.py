
import streamlit as st
import pandas as pd
import random
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime
from streamlit_autorefresh import st_autorefresh
st_autorefresh(interval=3000, key="log_refresh")
st.set_page_config(
    page_title="AI Cyber Defense System",
    page_icon="🛡️",
    layout="wide"
)


# -------------------------
# HEADER
# -------------------------

st.title("🛡️ Multi-Agent Cybersecurity Defense System")
st.caption("Real-time Threat Monitoring & Automated Response")

st.markdown("---")

# -------------------------
# SIDEBAR
# -------------------------

st.sidebar.title("System Control")

st.sidebar.write("Agent Status")

st.sidebar.success("Network Agent: Active")
st.sidebar.success("Log Agent: Active")
st.sidebar.success("Behavior Agent: Active")
st.sidebar.success("Response Agent: Active")

st.sidebar.markdown("---")

st.sidebar.write("System Time")
st.sidebar.info(datetime.now().strftime("%Y-%m-%d %H:%M:%S"))

# -------------------------
# METRICS PANEL
# -------------------------

col1, col2, col3, col4 = st.columns(4)

col1.metric(
    "Threat Level",
    "HIGH",
    "↑ 12%"
)

col2.metric(
    "Active Alerts",
    random.randint(10,30)
)

col3.metric(
    "Blocked IPs",
    random.randint(30,80)
)

col4.metric(
    "Anomalous Users",
    random.randint(2,10)
)

st.markdown("---")
mode = st.radio(
    "Select Threat Type",
    ["Login Attacks", "Network Attacks", "Malware Activity", "Port Scans"],
    horizontal=True
)
st.markdown("---")

# -------------------------
# NETWORK TRAFFIC MONITOR
# -------------------------

col1, col2 = st.columns(2)

# -------------------------
# NETWORK TRAFFIC + AI ANALYSIS
# -------------------------

col1, col2 = st.columns(2)
with col1:

    st.subheader("🧠 AI Threat Analysis")

    if mode == "Login Attacks":

        st.info("Threat detected: Brute Force Login")
        st.write("Confidence: 91%")

        st.warning("System Response: IP blocked automatically")

        st.success("AI Explanation: Multiple failed login attempts detected.")

        threat_ip = "185.23.44.21"
        location = "Moscow, Russia"


    elif mode == "Network Attacks":

        st.info("Threat detected: DDoS Attack")
        st.write("Confidence: 88%")

        st.warning("System Response: Traffic rate limiting enabled")

        st.success("AI Explanation: Abnormal traffic spike detected.")

        threat_ip = "91.210.33.19"
        location = "Beijing, China"


    elif mode == "Malware Activity":

        st.info("Threat detected: Malware Communication")
        st.write("Confidence: 86%")

        st.warning("System Response: Host isolated")

        st.success("AI Explanation: Suspicious outbound connection detected.")

        threat_ip = "103.44.22.88"
        location = "Seoul, South Korea"


    elif mode == "Port Scans":

        st.info("Threat detected: Port Scanning Activity")
        st.write("Confidence: 84%")

        st.warning("System Response: Firewall rule applied")

        st.success("AI Explanation: Sequential port probing detected.")

        threat_ip = "172.16.10.4"
        location = "Berlin, Germany"


    st.markdown("### 🌐 Threat Source")

    colA, colB = st.columns(2)

    with colA:
        st.metric("Threat IP Address", threat_ip)

    with colB:
        st.metric("Location", location)
with col2:

    st.subheader("📡 Network Traffic Monitor")

    traffic = pd.DataFrame({
        "time": list(range(1,60)),
        "traffic": [random.randint(100,800) for _ in range(59)]
    })

    fig = px.line(
        traffic,
        x="time",
        y="traffic",
        title="Incoming Network Traffic"
    )

    fig.update_layout(height=350)

    st.plotly_chart(fig, use_container_width=True)

# -------------------------
# ATTACK TYPE DISTRIBUTION
# -------------------------

with col2:

    st.subheader("⚠️ Threat Type Distribution")

    threats = pd.DataFrame({
        "Attack Type":[
            "DDoS",
            "Brute Force",
            "Phishing",
            "Malware",
            "Port Scan"
        ],
        "Count":[
            random.randint(5,30),
            random.randint(5,30),
            random.randint(5,30),
            random.randint(5,30),
            random.randint(5,30)
        ]
    })

    fig2 = px.pie(
        threats,
        names="Attack Type",
        values="Count",
        hole=0.5
    )

    fig2.update_layout(height=350)

    st.plotly_chart(fig2, use_container_width=True)

st.markdown("---")

# -------------------------
# USER BEHAVIOR ANOMALY
# -------------------------

col1, col2 = st.columns(2)

with col1:
     st.subheader("🌐 Network Performance Monitoring")
    col1, col2 = st.columns(2)
 # Latency
     latency_data = pd.DataFrame({
      "time": range(50),
      "latency":[random.randint(10,120) for _ in range(50)]
   })

    fig_latency = px.line(latency_data,x="time",y="latency",title="Network Latency (ms)")
    col1.plotly_chart(fig_latency,use_container_width=True)

# Request Rate
    req_data = pd.DataFrame({
       "time": range(50),
       "requests":[random.randint(100,800) for _ in range(50)]
    })

   fig_req = px.line(req_data,x="time",y="requests",title="Request Rate")
    col2.plotly_chart(fig_req,use_container_width=True)

# -------------------------
# BLOCKED IP LIST
# -------------------------

with col2:

    st.subheader("🚫 Recently Blocked IPs")

    blocked = pd.DataFrame({
        "IP Address":[
            "185.23.44.21",
            "91.210.33.19",
            "103.44.22.88",
            "172.16.10.4"
        ],
        "Reason":[
            "DDoS Traffic",
            "Brute Force",
            "Port Scanning",
            "Malware Communication"
        ]
    })

    st.dataframe(blocked, use_container_width=True)

st.markdown("---")

# -------------------------
# LIVE SECURITY ALERTS
# -------------------------

st.subheader("🚨 Live Security Alerts")

alerts = pd.DataFrame({
    "Time":[
        "12:01:03",
        "12:03:12",
        "12:04:55",
        "12:06:41"
    ],
    "IP Address":[
        "45.12.44.90",
        "201.33.11.77",
        "33.91.55.21",
        "77.44.22.18"
    ],
    "Threat":[
        "DDoS Attack",
        "Brute Force Login",
        "Suspicious Login",
        "Malware Activity"
    ],
    "Severity":[
        "Critical",
        "High",
        "Medium",
        "High"
    ],
    "Action":[
        "IP Blocked",
        "Account Locked",
        "User Flagged",
        "Connection Terminated"
    ]
})

st.dataframe(alerts, use_container_width=True)

st.markdown("---")

st.success("System Operational — All Agents Running")
st.markdown("---")
st.subheader("🖥️ Live Security Log Monitor")

import pandas as pd
import random
from datetime import datetime

# Simulated logs (later you will read from file)
log_data = pd.DataFrame({
    "Time":[
        datetime.now().strftime("%H:%M:%S") for _ in range(6)
    ],
    "Event":[
        random.choice([
            "Failed login attempt",
            "Suspicious IP detected",
            "Port scan detected",
            "User login success",
            "Malware signature detected",
            "Firewall blocked IP"
        ]) for _ in range(6)
    ],
    "Source IP":[
        f"192.168.1.{random.randint(1,255)}" for _ in range(6)
    ],
    "Status":[
        random.choice(["INFO","WARNING","CRITICAL"]) for _ in range(6)
    ]
})

st.dataframe(log_data, use_container_width=True)
