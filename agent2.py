from flask import Flask, jsonify, request

app = Flask(__name__)

# Agent card
agent_card = {
    "name": "Agent 2",
    "description": "A simple agent that responds to hello",
    "url": "http://localhost:3002",
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
            "id": "respond-hello",
            "name": "Respond Hello",
            "description": "Responds to hello from Agent 1",
            "tags": ["hello"],
            "examples": ["hello back agent 1"]
        }
    ]
}

# Publish agent card
@app.route('/.well-known/agent.json')
def get_agent_card():
    return jsonify(agent_card)

# Handle A2A RPC requests
@app.route('/rpc', methods=['POST'])
def handle_rpc():
    request_data = request.json
    print('Received RPC request:', request_data)
    
    # Check if it's a task/send method
    if request_data.get('method') == 'tasks/send':
        params = request_data.get('params', {})
        task_id = params.get('id')
        session_id = params.get('sessionId')
        message = params.get('message', {})
        
        # Check if it's a hello message
        if message.get('parts') and message['parts'][0].get('text') == 'hello agent 2':
            # Respond with a hello back
            return jsonify({
                "jsonrpc": "2.0",
                "id": request_data.get('id'),
                "result": {
                    "id": task_id,
                    "sessionId": session_id,
                    "status": {
                        "state": "completed"
                    },
                    "artifacts": [{
                        "parts": [{
                            "type": "text",
                            "text": "hello back agent 1"
                        }]
                    }]
                }
            })
        else:
            # Handle unknown message
            return jsonify({
                "jsonrpc": "2.0",
                "id": request_data.get('id'),
                "result": {
                    "id": task_id,
                    "sessionId": session_id,
                    "status": {
                        "state": "completed"
                    },
                    "artifacts": [{
                        "parts": [{
                            "type": "text",
                            "text": "I don't understand that message"
                        }]
                    }]
                }
            })
    else:
        # Handle unsupported method
        return jsonify({
            "jsonrpc": "2.0",
            "id": request_data.get('id'),
            "error": {
                "code": -32601,
                "message": "Method not found"
            }
        })
