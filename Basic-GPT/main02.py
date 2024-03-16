import requests
import json
import gradio as gr

url = "http://localhost:11434/api/generate"

headers = {
    'Content-Type': 'application/json',
}

conversation_history = []

def generate_response(prompt, model_name):  # Updated to accept model_name
    conversation_history.append(prompt)

    full_prompt = "\n".join(conversation_history)

    data = {
        "model": model_name,  # Use the selected model
        "stream": False,
        "prompt": full_prompt,
    }

    response = requests.post(url, headers=headers, data=json.dumps(data))

    if response.status_code == 200:
        response_text = response.text
        data = json.loads(response_text)
        actual_response = data["response"]
        conversation_history.append(actual_response)
        return actual_response
    else:
        error_message = f"Error: {response.status_code} {response.text}"
        print(error_message)
        return error_message  # So the error shows in the Gradio interface instead of just the console

iface = gr.Interface(
    fn=generate_response,
    inputs=[gr.Textbox(lines=2, placeholder="Enter your prompt here..."),  # Keep the existing Textbox input
            gr.Dropdown(choices=['llama2', 'mistral', 'falcon'], label="Model Selection")],  # Add a Dropdown for model selection
    outputs="text"
)

iface.launch()
