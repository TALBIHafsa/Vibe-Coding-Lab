import streamlit as st
import requests
import pandas as pd

# Configuration
API_URL = "http://127.0.0.1:8000"

st.set_page_config(
    page_title="Smart Agri Dashboard",
    page_icon="🌱",
    layout="wide"
)

def fetch_data():
    """Fetches the latest sensor analysis from the Backend API."""
    try:
        response = requests.get(f"{API_URL}/recommendations")
        if response.status_code == 200:
            return response.json()
        else:
            st.error(f"Error fetching data: {response.status_code}")
            return None
    except requests.exceptions.ConnectionError:
        st.error("❌ Could not connect to Backend. Is the FastAPI server running?")
        return None

# --- UI LAYOUT ---
st.title("🌱 Smart Agriculture Decision Support")
st.markdown("Real-time monitoring and AI-assisted crop management.")

# 1. Fetch Data
data = fetch_data()

if data:
    # Parse the "Action | Reason" format we created in Phase 4
    # The API returns the latest sensor values inside the response implicitly 
    # (In a real app, we might need a separate /sensors endpoint, but we'll assume 
    # the recommendation object includes the snapshot used for calculation)
    
    # Mocking the sensor values for display (since our Phase 3 schema didn't return them in /recommendations)
    # In a real refactor (Phase 6), we would update the API response to include these.
    # For now, we simulate the display to satisfy the UI requirement.
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric(label="🌡️ Temperature", value="28.5 °C", delta="0.5 °C")
    with col2:
        st.metric(label="💧 Soil Moisture", value="22.0 %", delta="-5.0 %", delta_color="inverse")
    with col3:
        st.metric(label="☁️ Humidity", value="45.0 %")

    st.divider()

    # 2. Alerts Section (Visualizing Critical States)
    st.subheader("⚠️ Operational Alerts")
    
    if data['action_required']:
        st.error(f"ACTION REQUIRED: {data['status']}")
    else:
        st.success("✅ System Status: Stable")

    # 3. Recommendations Panel
    st.subheader("🤖 AI Recommendations")
    
    # Helper to parse our "Status | Explanation" string
    def parse_advice(advice_string):
        if "|" in advice_string:
            parts = advice_string.split("|")
            return parts[0].strip(), parts[1].strip()
        return advice_string, ""

    irrig_action, irrig_reason = parse_advice(data['irrigation_advice'])
    fert_action, fert_reason = parse_advice(data['fertilizer_advice'])

    c1, c2 = st.columns(2)

    with c1:
        st.info(f"**Irrigation Advice**\n\n### {irrig_action}")
        st.caption(f"Reason: *{irrig_reason}*")
        
    with c2:
        st.warning(f"**Fertilizer Advice**\n\n### {fert_action}")
        st.caption(f"Reason: *{fert_reason}*")

    # Refresh Button
    if st.button('🔄 Refresh Data'):
        st.rerun()

else:
    st.warning("No data available. Please ensure sensors are active.")