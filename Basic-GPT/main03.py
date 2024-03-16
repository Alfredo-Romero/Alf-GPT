import requests
import json
import gradio as gr

url = "http://localhost:11434/api/generate"

headers = {
    'Content-Type': 'application/json',
}

# This function now includes a state parameter and a reset parameter
def generate_response(prompt, model_name, state, reset=False):
    if reset or state is None:
        state = []  # Reset or initialize the conversation history

    state.append(prompt)
    full_prompt = "\n".join(state)

    data = {
        "model": model_name,
        "stream": False,
        "prompt": full_prompt,
    }

    response = requests.post(url, headers=headers, data=json.dumps(data))

    if response.status_code == 200:
        response_text = response.text
        data = json.loads(response_text)
        actual_response = data["response"]
        state.append(actual_response)  # Update the conversation history stored in state
        return actual_response, state  # Return the updated state along with the response
    else:
        error_message = f"Error: {response.status_code} {response.text}"
        print(error_message)
        return error_message, state

# Define the interface with state and a reset button
iface = gr.Interface(
    fn=generate_response,
    inputs=[
        gr.Textbox(lines=2, placeholder="Enter your prompt here..."),
        gr.Dropdown(choices=['llama2', 'mistral', 'falcon'], label="Model Selection"),
        gr.State(),  # This will hold the conversation history as state
        gr.Checkbox(label="Reset Conversation")  # A checkbox to control whether to reset
    ],
    outputs=[
        "text",
        gr.State()  # Output the state back to the interface
    ],
)

iface.launch()
