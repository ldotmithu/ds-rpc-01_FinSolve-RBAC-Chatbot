import streamlit as st
import requests
import base64
import os
from dotenv import load_dotenv

load_dotenv() 

BACKEND_URL = os.getenv("FASTAPI_BACKEND_URL", "http://localhost:8000")

st.set_page_config(page_title="FinSolve RBAC Chatbot", layout="centered")

if "messages" not in st.session_state or st.session_state.messages is None:
    st.session_state.messages = []
if "authenticated" not in st.session_state:
    st.session_state.authenticated = False
if "username" not in st.session_state:
    st.session_state.username = ""
if "password" not in st.session_state:
    st.session_state.password = ""
if "role" not in st.session_state:
    st.session_state.role = ""
if "selected_department" not in st.session_state:
    st.session_state.selected_department = ""

st.sidebar.title("🔐 Login")

def get_auth_headers(username, password):
    auth_string = f"{username}:{password}"
    encoded_auth = base64.b64encode(auth_string.encode()).decode("utf-8")
    return {"Authorization": f"Basic {encoded_auth}"}

if not st.session_state.authenticated:
    st.session_state.username = st.sidebar.text_input("Username")
    st.session_state.password = st.sidebar.text_input("Password", type="password")

    if st.sidebar.button("Login"):
        headers = get_auth_headers(st.session_state.username, st.session_state.password)
        try:
            response = requests.get(f"{BACKEND_URL}/login", headers=headers)
            if response.status_code == 200:
                user_data = response.json()
                st.session_state.authenticated = True
                st.session_state.role = user_data.get('role') 
                st.success(f"✅ Logged in successfully as: {st.session_state.username} ({st.session_state.role.capitalize()})")
                st.session_state.messages = [] 
            else:
                st.error(f"Login failed: {response.status_code} - {response.json().get('detail', 'Unknown error')}")
        except requests.exceptions.RequestException as e:
            st.error(f"Could not reach backend: {e}")
else:
    st.sidebar.success(f"Logged in as: {st.session_state.username} ({st.session_state.role.capitalize()})")
    if st.sidebar.button("Logout"):
        for key in ["authenticated", "username", "password", "role", "selected_department"]:
            st.session_state[key] = None
        st.session_state.messages = [] 
        st.rerun() 

    st.title("💬 FinSolve Chatbot")

    available_dep_for_role = {
        "finance": ["Finance"],
        "marketing": ["Marketing"],
        "hr": ["HR"],
        "engineering": ["Engineering"],
        "employee": ["General"]
    }
    
    current_user_departments = available_dep_for_role.get(st.session_state.role, [])
    
    if len(current_user_departments) > 1:
        st.session_state.selected_department = st.selectbox(
            "Select Department to Query:",
            options=current_user_departments,
            key="department_select"
        )
    elif len(current_user_departments) == 1:
        st.session_state.selected_department = current_user_departments[0]
        st.info(f"You are querying the **{st.session_state.selected_department}** department.")
    else:
        st.error("No departments available for your role. Please contact support.")
        st.stop() 

    user_input = st.text_input("Ask your question:", key="chat_input")

    if user_input and st.session_state.selected_department:
        st.session_state.messages.append(("user", user_input))

        headers = get_auth_headers(st.session_state.username, st.session_state.password)
        try:
            res = requests.post(
                f"{BACKEND_URL}/chat", 
                headers=headers,
                json={"message": user_input, "role": st.session_state.selected_department}, 
            )
            if res.status_code == 200:
                bot_reply = res.json()["response"]
            else:
                bot_reply = f"Error: {res.status_code} - {res.json().get('detail', 'Unknown error')}"
        except Exception as e:
            bot_reply = f"Failed to reach backend: {str(e)}"

        st.session_state.messages.append(("bot", bot_reply))

    for role, msg in reversed(st.session_state.messages):
        if role == "user":
            st.chat_message("user").write(msg)
        else:
            st.chat_message("assistant").write(msg)