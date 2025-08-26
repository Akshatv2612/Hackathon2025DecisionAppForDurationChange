import streamlit as st
import requests

BASE_URL = "https://9ssz6ekjqa.execute-api.ap-south-1.amazonaws.com"

query_params = st.query_params
project_id = query_params.get("projectId", None)
requested_duration = query_params.get("requestedDuration", None)

st.title("Duration Change Request Review")

if project_id and requested_duration:
    st.write(f"📌 Project ID: `{project_id}`")
    st.write(f"🕒 Requested Duration: **{requested_duration} days**")
    st.write("Please choose an action:")

    # Checkbox for human verification
    verified = st.checkbox("✅ I am not a robot")

    if "action_taken" not in st.session_state:
        st.session_state.action_taken = None

    col1, col2 = st.columns(2)

    with col1:
        if st.button("✅ Approve", disabled=not verified):
            st.session_state.action_taken = "approve-duration"

    with col2:
        if st.button("❌ Reject", disabled=not verified):
            st.session_state.action_taken = "reject-duration"

    if st.session_state.action_taken in ["approve-duration", "reject-duration"]:
        url = f"{BASE_URL}/{st.session_state.action_taken}"
        payload = {
            "projectId": project_id,
            "requestedDuration": int(requested_duration)
        }

        try:
            response = requests.post(url, json=payload, verify=False)
            print("Response", response.text)

            past_tense = {
                "approve-duration": "Approved",
                "reject-duration": "Rejected"
            }

            if response.ok:
                st.success(f"✅ Duration Change {past_tense[st.session_state.action_taken]} successfully!")
            else:
                st.error(f"❌ Duration Change {st.session_state.action_taken} failed.")

        except Exception as e:
            st.error(f"🚨 Request error: {e}")

        st.session_state.action_taken = None

else:
    st.error("Missing `projectId` or `requestedDuration` in the URL. Please open this app with a valid request link.")
