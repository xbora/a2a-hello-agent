# A2A Hello World

A minimal implementation of the Agent-to-Agent (A2A) protocol, demonstrating basic agent communication.

## What is A2A?

The Agent-to-Agent (A2A) protocol is an open standard that enables different AI agents to communicate with each other in a structured, predictable way. This project provides a simple "hello world" example of two agents exchanging messages using A2A.

## How It Works

In this demo:
- Agent 1 sends the message "hello agent 2"
- Agent 2 responds with "hello back agent 1"

## Key A2A Concepts Demonstrated

### Agent Cards

Each agent has an "agent card" that serves as its identity document. The card describes:
- Who the agent is (name, description)
- What skills it has
- What input/output formats it supports
- Authentication requirements (none in this demo)

Agent cards are published at the `/.well-known/agent.json` endpoint.

### Tasks

Communication in A2A happens within the context of "tasks." A task:
- Has a unique ID
- Contains a session ID (for related tasks)
- Tracks the state of the work (submitted, working, completed, etc.)
- Contains messages and artifacts

### Messages and Artifacts

- **Messages**: Content exchanged between agents (like "hello agent 2")
- **Artifacts**: Results produced by agents (like the response "hello back agent 1")

### JSON-RPC 2.0

All A2A communication uses the JSON-RPC 2.0 format for requests and responses, providing a standardized way to make requests and handle responses.

## How to Run This Demo

1. Clone this repository
2. Install dependencies: `pip install -r requirements.txt`
3. Run the application: `python simplified_app.py`
4. Open your browser to the URL shown in the console (typically http://localhost:8080)
5. Click the "Start Conversation" button to see the agents communicate

## Code Structure

This implementation is simplified to run within a single Flask application:

- Agent 1 and Agent 2 are implemented as different routes within the same app
- Both agents expose their agent cards at `/.well-known/agent.json`
- Agent 2 handles RPC requests at `/agent2/rpc`
- Communication between agents is simulated using Flask's test client

## Real-World A2A

In a production environment:
- Agents would typically run as separate services
- They would communicate over HTTP/HTTPS
- Authentication would be implemented
- They could handle more complex data types (images, structured data)
- Multiple agents could work together on complex tasks

## Further Reading

For more information on the A2A protocol, see the [official documentation](https://a2a.org).

## License

[MIT License](LICENSE)
