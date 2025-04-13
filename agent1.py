from flask import Flask, jsonify, request
import requests
import uuid

app = Flask(__name__)

# Agent card
agent_card = {
    "name": "Agent 1",
    "description": "A simple agent that says hello",
    "url": "http://localhost:3001",
    "version": "1.0.0",
    "authentication": {
        "schemes": []
    },
    "defaultInputModes": ["text/plain"],
    "defaultOutputModes": ["text/plain"],
    "capabilities": {
        "streaming": False,
        "pushNotifications": False
    },
    "skills": [
        {
            "id": "say-hello",
            "name": "Say Hello",
            "description": "Says hello to Agent 2",
            "tags": ["hello"],
            "examples": ["hello agent 2"]
        }
    ]
}

# Publish agent card
@app.route('/.well-known/agent.json')
def get_agent_card():
    return jsonify(agent_card)

# Function to send hello to Agent 2
def send_hello():
    task_id = str(uuid.uuid4())
    session_id = str(uuid.uuid4())
    
    try:
        # A2A task/send request to Agent 2
        response = requests.post('http://localhost:3002/rpc', json={
            "jsonrpc": "2.0",
            "id": 1,
            "method": "tasks/send",
            "params": {
                "id": task_id,
                "sessionId": session_id,
                "message": {
                    "role": "user",
                    "parts": [{
                        "type": "text",
                        "text": "hello agent 2"
                    }]
                }
            }
        })
        
        response_data = response.json()
        print('Agent 2 response:', response_data)
        
        # Extract response message
        if (response_data.get('result') and 
            response_data['result'].get('artifacts') and 
            len(response_data['result']['artifacts']) > 0 and
            response_data['result']['artifacts'][0].get('parts') and
            len(response_data['result']['artifacts'][0]['parts']) > 0):
            return response_data['result']['artifacts'][0]['parts'][0]['text']
        
        return "No response from Agent 2"
    except Exception as e:
        print('Error sending hello:', e)
        raise e
