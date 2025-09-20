import streamlit as st
import requests

st.title("Test Deployed FastAPI Chat Endpoint")

# Input box for user query
query = st.text_input("Enter your query:", "Finalize AI MVP")

# Number of top results
top_k = st.number_input("Top K results:", min_value=1, max_value=10, value=3)

if st.button("Send Request"):
    url = "http://139.185.33.139/chat"  # Your public endpoint
    payload = {"query": query, "top_k": top_k}

    try:
        response = requests.post(url, json=payload)
        if response.status_code == 200:
            st.success("Request successful!")
            st.json(response.json())
        else:
            st.error(f"Error {response.status_code}: {response.text}")
    except Exception as e:
        st.error(f"Request failed: {e}")
