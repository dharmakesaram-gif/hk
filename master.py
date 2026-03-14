
import streamlit as st
import pandas as pd
import random
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime

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

# -------------------------
# NETWORK TRAFFIC MONITOR
# -------------------------

col1, col2 = st.columns(2)

with col1:

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

    st.subheader("👤 User Behavior Risk Scores")

    users = pd.DataFrame({
        "User":[
            "admin",
            "john",
            "guest",
            "developer",
            "finance"
        ],
        "Risk Score":[
            random.randint(10,90),
            random.randint(10,90),
            random.randint(10,90),
            random.randint(10,90),
            random.randint(10,90)
        ]
    })

    fig3 = px.bar(
        users,
        x="User",
        y="Risk Score",
        color="Risk Score",
        color_continuous_scale="reds"
    )

    fig3.update_layout(height=350)

    st.plotly_chart(fig3, use_container_width=True)

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
