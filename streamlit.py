import streamlit as st
import requests

# ----------------------------
# FastAPI backend base URL
# ----------------------------
BASE_URL = "https://selamnew-ai.ienetworks.co/"

st.set_page_config(page_title="AI OKR Assistant", page_icon="🤖")
st.title("🤖 AI OKR Assistant")
st.write("Test your OKR AI endpoints: Chat, Weekly Plan, Daily Plan.")

# ----------------------------
# Choose endpoint
# ----------------------------
endpoint = st.selectbox(
    "Select Endpoint",
    ["Chat (Key Results)", "Weekly Plan", "Daily Plan"]
)

top_k = st.number_input("Top K", min_value=1, max_value=20, value=5)

# ----------------------------
# Chat Endpoint
# ----------------------------
if endpoint == "Chat (Key Results)":
    query = st.text_input("Enter Objective:", "")
    if st.button("Generate Key Results"):
        if query.strip():
            try:
                response = requests.post(
                    f"{BASE_URL}/chat",
                    json={"query": query, "top_k": top_k},
                    headers={"Content-Type": "application/json"}
                )
                if response.status_code == 200:
                    st.success("✅ Key Results Generated!")
                    st.json(response.json())
                else:
                    st.error(f"❌ Error {response.status_code}: {response.text}")
            except Exception as e:
                st.error(f"⚠️ Request failed: {e}")
        else:
            st.warning("⚠️ Please enter an Objective first.")

# ----------------------------
# Weekly Plan Endpoint
# ----------------------------
elif endpoint == "Weekly Plan":
    key_result = st.text_input("Enter Key Result:", "")
    if st.button("Generate Weekly Plan"):
        if key_result.strip():
            try:
                response = requests.post(
                    f"{BASE_URL}/weekly-plan",
                    json={"key_result": key_result, "top_k": top_k},
                    headers={"Content-Type": "application/json"}
                )
                if response.status_code == 200:
                    st.success("✅ Weekly Plan Generated!")
                    st.json(response.json())
                else:
                    st.error(f"❌ Error {response.status_code}: {response.text}")
            except Exception as e:
                st.error(f"⚠️ Request failed: {e}")
        else:
            st.warning("⚠️ Please enter a Key Result first.")

# ----------------------------
# Daily Plan Endpoint
# ----------------------------
elif endpoint == "Daily Plan":
    annual_key_result = st.text_input("Enter Annual Key Result:", "")
    if st.button("Generate Daily Plan"):
        if annual_key_result.strip():
            try:
                response = requests.post(
                    f"{BASE_URL}/daily-plan",
                    json={"annual_key_result": annual_key_result, "top_k": top_k},
                    headers={"Content-Type": "application/json"}
                )
                if response.status_code == 200:
                    st.success("✅ Daily Plan Generated!")
                    st.json(response.json())
                else:
                    st.error(f"❌ Error {response.status_code}: {response.text}")
            except Exception as e:
                st.error(f"⚠️ Request failed: {e}")
        else:
            st.warning("⚠️ Please enter an Annual Key Result first.")
