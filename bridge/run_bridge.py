"""
Simple Bridge Server for Cascade/Windsurf Integration
This allows CrewAI agents to communicate with humans through the Windsurf IDE
"""
import os
import json
from flask import Flask, request, jsonify, Response
import logging

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

logger = logging.getLogger('CascadeBridge')

# Initialize Flask app
app = Flask(__name__)

@app.route('/health', methods=['GET'])
def health_check():
    """Simple health check endpoint"""
    return jsonify({"status": "ok"})

@app.route('/generate', methods=['POST'])
def generate():
    """
    Handle generation request from agents
    
    This endpoint receives prompts from CrewAI agents and
    relays them to the human user via the console. The human's
    response is then sent back to the agent.
    """
    try:
        data = request.json
        prompt = data.get('prompt', '')
        role = data.get('role', 'Agent')
        
        # Display agent's message to human
        print(f"\n\n{'=' * 40}")
        print(f"Message from {role}:")
        print(f"{'=' * 40}")
        print(prompt)
        print(f"{'=' * 40}")
        
        # Get human's response
        print("\nYour response (type your answer and press Enter):")
        human_response = input("> ")
        
        # Return human's response to the agent
        return jsonify({
            "response": human_response,
            "role": "Human"
        })
        
    except Exception as e:
        logger.error(f"Error in generate: {str(e)}")
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    print("=" * 50)
    print("🌉 CrewSurf Bridge Server")
    print("=" * 50)
    print("Starting bridge server for Windsurf/Cascade integration...")
    print("This allows CrewAI agents to communicate with humans")
    print("\nServer running at http://localhost:8089")
    print("Use another terminal to run the CrewAI agents")
    print("=" * 50)
    
    # Run the Flask app
    app.run(host='0.0.0.0', port=8089, debug=False)
