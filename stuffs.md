
Used streamlit UI to create chatbox interface;

Debugging the return format from ollama

# App starter for streamlit
streamlit run streamlit.py

## how the model is served
- ReST API (HTTP Request):Ollama is ready to serve Inference API requests, on local HTTP port 11434 (default). You can hit the Inference API endpoint with HTTP POST request containing the prompt message payload. 

## Some stuffs to notice
- set the “stream” flag as “false” in the CURL request, to get all responses at once. The default value for “stream” is true, in which case, you will receive multiple HTTP responses with a streaming result of tokens. For the last response of the streaming results, the “done” attribute will be returned as “true”.
### Stage
 the “stage” is represented by a variable (agent_stage in st.session_state) that tracks the progress through the interaction process.
## logic
Overall Logic Flow

	1.	Initialization:
	•	Initialize states for tracking messages, stages, and input.
	2.	UI for the Current Stage:
	•	Display the current agent’s name and conversation history.
	•	Provide the input box for the user to interact with the current agent.
	3.	Input Handling and Processing:
	•	Check if user input has already been processed to prevent duplicates.
	•	Append the input and agent response to the message history.
	•	Clear the input box after processing.
	4.	Stage Control:
	•	Once the stage has been processed, give the user the option to ask another question or move to the next stage.
	5.	Conversation Reset:
	•	Provide the user with an option to reset the conversation and start again.

stage1 - stage2 -stage3

flag: processed
button: shown or not

current agent;
current conversation


### bug

- the msg display duplicates issue.

- the option added for previous agents 