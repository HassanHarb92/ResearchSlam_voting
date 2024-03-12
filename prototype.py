import streamlit as st
import csv
import os

# Function to append vote to CSV
def append_vote_to_csv(vote_data, filename="votes.csv"):
    file_exists = os.path.isfile(filename)
    with open(filename, mode='a', newline='') as file:
        writer = csv.DictWriter(file, fieldnames=vote_data.keys())
        if not file_exists:
            writer.writeheader()
        writer.writerow(vote_data)

if 'judge_id' not in st.session_state:
    st.session_state.judge_id = None

if 'submission_status' not in st.session_state:
    st.session_state.submission_status = False

if 'selected_participant' not in st.session_state:
    st.session_state.selected_participant = None

judges_codes = {"judge1": "1111", "judge2": "2222", "judge3": "3333", "judge4": "4444", "judge5": "5555"}

if not st.session_state.judge_id:
    code = st.text_input("Enter your judge code")
    if code:
        if code in judges_codes.values():
            st.session_state.judge_id = [key for key, value in judges_codes.items() if value == code][0]
            st.success(f"Authenticated as {st.session_state.judge_id}")
        else:
            st.error("Invalid code. Please enter a valid judge code.")

if st.session_state.submission_status:
    st.info(f"Thank you {st.session_state.judge_id}, you have submitted your vote for {st.session_state.selected_participant}.")
    if st.button("Submit another vote"):
        st.session_state.submission_status = False
        # Do not clear st.session_state.judge_id here to remember the judge
        # Reset selected participant for a new selection
        st.session_state.selected_participant = None

if st.session_state.judge_id and not st.session_state.submission_status:
    participants = ["Choose a participant", "Participant 1", "Participant 2", "Participant 3"]
    selected_participant = st.selectbox("Select the participant", participants, index=0)

    if selected_participant and selected_participant != "Choose a participant":
        st.session_state.selected_participant = selected_participant
        q1 = st.slider("Question 1", 1, 10, key="q1")
        q2 = st.slider("Question 2", 1, 10, key="q2")
        q3 = st.slider("Question 3", 1, 10, key="q3")
        q4 = st.slider("Question 4", 1, 10, key="q4")
        q5 = st.slider("Question 5", 1, 10, key="q5")

        if st.button("Submit Vote"):
            vote_data = {
                "judge_id": st.session_state.judge_id,
                "participant": st.session_state.selected_participant,
                "q1": q1,
                "q2": q2,
                "q3": q3,
                "q4": q4,
                "q5": q5,
            }
            append_vote_to_csv(vote_data)
            st.session_state.submission_status = True

