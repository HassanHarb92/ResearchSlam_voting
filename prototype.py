import streamlit as st
import csv
import os

# Function to append vote to CSV
def append_vote_to_csv(vote_data, filename="votes.csv"):
    # Check if file exists to write headers
    file_exists = os.path.isfile(filename)
    
    with open(filename, mode='a', newline='') as file:
        writer = csv.DictWriter(file, fieldnames=vote_data.keys())
        
        if not file_exists:
            writer.writeheader()  # Write header only once
        
        writer.writerow(vote_data)

# Initialize session state for sliders
if 'slider_values' not in st.session_state:
    st.session_state.slider_values = [1, 1, 1, 1, 1]

# Example list of participants with a null option at the beginning
participants = ["Choose a participant", "Participant 1", "Participant 2", "Participant 3"]

# Example judges' codes
judges_codes = {"judge1": "1111", "judge2": "2222", "judge3": "3333", "judge4": "4444", "judge5": "5555"}

# Authentication
code = st.text_input("Enter your judge code")

if code in judges_codes.values():
    judge_id = [key for key, value in judges_codes.items() if value == code][0]
    st.success(f"Welcome, {judge_id}")
    
    # Voting Part
    selected_participant = st.selectbox("Choose the participant", participants, index=0, key="participant_selector")
    
    if selected_participant != "Choose a participant":
        # Reset sliders if the selected participant changes
        if 'last_participant' not in st.session_state or st.session_state.last_participant != selected_participant:
            st.session_state.slider_values = [1, 1, 1, 1, 1]
            st.session_state.last_participant = selected_participant
        
        # Questions and Votes
        q1 = st.slider("Question 1", 1, 10, st.session_state.slider_values[0], key="q1")
        q2 = st.slider("Question 2", 1, 10, st.session_state.slider_values[1], key="q2")
        q3 = st.slider("Question 3", 1, 10, st.session_state.slider_values[2], key="q3")
        q4 = st.slider("Question 4", 1, 10, st.session_state.slider_values[3], key="q4")
        q5 = st.slider("Question 5", 1, 10, st.session_state.slider_values[4], key="q5")
        
        # Update slider values in session state
        st.session_state.slider_values = [q1, q2, q3, q4, q5]

        submit = st.button("Submit Vote")
        
        if submit:
            # Prepare vote data
            vote_data = {
                "judge_id": judge_id,
                "participant": selected_participant,
                "q1": q1,
                "q2": q2,
                "q3": q3,
                "q4": q4,
                "q5": q5,
            }
            
            # Append vote to CSV
            append_vote_to_csv(vote_data)
            
            st.success(f"Thanks for voting, {judge_id}!")
    else:
        st.info("Please select a participant to vote for.")
else:
    st.write("Please enter a valid code.")

