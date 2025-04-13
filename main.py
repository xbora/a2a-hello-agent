from flask import Flask, jsonify, request, render_template_string
import uuid

app = Flask(__name__)

# Agent 1 card
agent1_card = {
    "name": "Agent 1",
    "description": "A simple agent that says hello",
    "url": "/agent1",
    "version": "1.0.0",
    "authentication": {
        "schemes": []
    },
    "defaultInputModes": ["text/plain"],
    "defaultOutputModes": ["text/plain"],
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

# Agent 2 card
agent2_card = {
    "name": "Agent 2",
    "description": "A simple agent that responds to hello",
    "url": "/agent2",
    "version": "1.0.0",
    "authentication": {
        "schemes": []
    },
    "defaultInputModes": ["text/plain"],
    "defaultOutputModes": ["text/plain"],
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

# Main interface
@app.route('/.well-known/agent.json')
def root_agent_card():
    # Return a combined card that represents the system
    return jsonify({
        "name": "A2A Demo System",
        "description": "A demo system with two agents that can talk to each other",
        "url": "/",
        "version": "1.0.0",
        "agents": [agent1_card, agent2_card]
    })

@app.route('/')
def index():
    return render_template_string("""
        <h1>A2A Hello World</h1>
        <p>Agent 1 and Agent 2 are ready to talk!</p>
        <button onclick="startConversation()">Start Conversation</button>
        <div id="results"></div>
        <script>
            async function startConversation() {
                document.getElementById('results').innerHTML = 'Starting conversation...';
                const response = await fetch('/start-conversation');
                const result = await response.text();
                document.getElementById('results').innerHTML = result;
            }
        </script>
    """)

# Agent 1 card endpoint
@app.route('/agent1/.well-known/agent.json')
def agent1_card_endpoint():
    return jsonify(agent1_card)

# Agent 2 card endpoint
@app.route('/agent2/.well-known/agent.json')
def agent2_card_endpoint():
    return jsonify(agent2_card)

# Agent 2 RPC endpoint
@app.route('/agent2/rpc', methods=['POST'])
def agent2_rpc():
    request_data = request.json
    print('Agent 2 received RPC request:', request_data)

    if request_data.get('method') == 'tasks/send':
        params = request_data.get('params', {})
        task_id = params.get('id')
        session_id = params.get('sessionId')
        message = params.get('message', {})

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
        return jsonify({
            "jsonrpc": "2.0",
            "id": request_data.get('id'),
            "error": {
                "code": -32601,
                "message": "Method not found"
            }
        })

# Trigger the conversation
@app.route('/start-conversation')
def start_conversation():
    try:
        # Generate IDs
        task_id = str(uuid.uuid4())
        session_id = str(uuid.uuid4())

        # This would normally be an HTTP request, but since we're in the same app,
        # we'll simulate the request and response
        request_data = {
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
        }

        # Log the simulated request
        print("Agent 1 sending request to Agent 2:", request_data)

        # Get the response directly from Agent 2's RPC endpoint
        with app.test_client() as client:
            response = client.post('/agent2/rpc', json=request_data)
            response_data = response.get_json()

        print("Agent 2 response:", response_data)

        # Extract response message
        if (response_data.get('result') and 
            response_data['result'].get('artifacts') and 
            len(response_data['result']['artifacts']) > 0 and
            response_data['result']['artifacts'][0].get('parts') and
            len(response_data['result']['artifacts'][0]['parts']) > 0):
            result = response_data['result']['artifacts'][0]['parts'][0]['text']
        else:
            result = "No response from Agent 2"

        return f'Conversation complete!<br>Agent 1: "hello agent 2"<br>Agent 2: "{result}"'
    except Exception as e:
        print("Error:", str(e))
        return f"Error: {str(e)}", 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)