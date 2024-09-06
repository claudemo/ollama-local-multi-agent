import streamlit as st
import requests

# Define the Ollama API endpoint (replace with the actual one)
OLLAMA_API_URL = "http://localhost:11434/api/generate"

# Function to query an agent with a specific prompt
def query_ollama(prompt):
    headers = {"Content-Type": "application/json"}
    data = {"model": "llama3", "prompt": prompt, "stream": False}
    
    response = requests.post(OLLAMA_API_URL, headers=headers, json=data)
    
    if response.status_code == 200:
        try:
            return response.json()["response"]  # Adjust key as needed
        except KeyError:
            return "Error: Expected key 'response' not found in API response."
    else:
        return f"Error: {response.status_code}, {response.text}"

# Define the role-based agents with their specific prompts
agents_prompts = {
    1: "Agent 1 (Reporter): List the patient's general information in bullet points, only the necessary information and would not give long reports, avoid introducing yourself.",
    2: "Agent 2 (Patient): What is your current blood pressure and any other relevant health details?",
    3: "Agent 3 (Doctor): The nurse needs the doctor's response based on the information from reporter and patient."
}

agents_names = {
    1: "Agent 1 (Reporter)",
    2: "Agent 2 (Patient)",
    3: "Agent 3 (Doctor)"
}

# ------------------------Initialize  
# Initialize Streamlit app
st.title("Multi-Stage Agent Interaction (Nurse, Patient, Doctor)")

# Initialize chat history and progression state
if 'messages' not in st.session_state:
    st.session_state['messages'] = []
if 'agent_stage' not in st.session_state:
    st.session_state['agent_stage'] = 1  # Start with Agent 1 (Reporter)
if 'stage_processed' not in st.session_state:
    st.session_state['stage_processed'] = False  # Track if the current stage has been processed

# Initialize the last input to avoid duplicate entries
if 'last_input' not in st.session_state:
    st.session_state['last_input'] = ""

# User input field, restricted to the current agent stage
user_input = st.text_input("You (Nurse):", value="", key="input_box")
# ---------------------------User input 
# If user input is provided and the stage has not been processed
if user_input and not st.session_state['stage_processed']:
    # Check if the message has already been processed for this stage to avoid duplicates
    if st.session_state['last_input'] != user_input:
        # Append user message to chat history with current agent tag
        st.session_state['messages'].append({
            'agent': st.session_state['agent_stage'],  # Associate the message with the current agent
            'sender': 'Nurse',
            'text': user_input  # Store the user input
        })

        # Interact with the current agent based on the stage
        response = query_ollama(agents_prompts[current_stage])
        st.session_state['messages'].append({
            'agent': current_stage,  # Associate the agent response with the current agent
            'sender': agents_names[current_stage],
            'text': response
        })
        
        # Store the last input to avoid appending it again
        st.session_state['last_input'] = user_input

        # Mark the current stage as processed
        st.session_state['stage_processed'] = True
        # Clear the input box by resetting the value in session state
        st.session_state['last_input'] = ""

    
    # Interact with the current agent based on the stage
    response = query_ollama(agents_prompts[current_stage])
    st.session_state['messages'].append({
        'agent': current_stage,  # Associate the agent response with the current agent
        'sender': agents_names[current_stage],
        'text': response
    })
    
    # Mark the current stage as processed
    st.session_state['stage_processed'] = True
    



#======================= Display chat history for the current agent only==================
st.write(f"Conversation with {agents_names[current_stage]}:")
for message in st.session_state['messages']:
    if message['agent'] == current_stage:
        st.write(f"{message['sender']}: {message['text']}")


#  ----------------------------Stage Progression with Button
# Options after processing the current stage
if st.session_state['stage_processed'] and current_stage <= 3:
    st.write(f"(You are currently interacting with {agents_names[current_stage]}.)")
    
    # Option to ask another question in the current stage
    if st.button(f"Ask another question to {agents_names[current_stage]}"):
        st.session_state['stage_processed'] = False  # Allow another question
    
    # Option to proceed to the next stage
    if current_stage < 3 and st.button(f"Proceed to {agents_names[current_stage + 1]}"):
        st.session_state['agent_stage'] += 1
        st.session_state['stage_processed'] = False  # Reset processing flag for the next stage

# Indicate when the conversation is complete
if current_stage == 4:
    st.success("Interaction complete! You have finished all stages.")

#   --------------------------------------Reset
if st.button("Start New Interaction"):
    st.session_state['messages'] = []
    st.session_state['agent_stage'] = 1  # Reset to Agent 1
    st.session_state['stage_processed'] = False  # Reset the stage processed state
    st.session_state['last_input'] = ""  # Reset the last input