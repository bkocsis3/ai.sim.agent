from agents.agent import create_my_agent
import json

def main():
    # Create the AI agent
    agent = create_my_agent()
    print("Agent started. Type 'quit' to exit.")

    # Main loop to interact with the agent
    while True:
        # Get the self state from the user
        self_state = input(
            "Enter the self state (JSON format) of the AI agent: "
        )

        # Check if the user wants to quit
        if self_state.lower() == "quit":
            print("Shutting down agent...")
            break

        # Validate the JSON input
        try:
            json.loads(self_state)
        except json.JSONDecodeError:
            print("Invalid JSON. Try again.")
            continue

        # Invoke the agent with the self state
        response = agent.invoke({
            "messages": [
                {"role": "user", "content": self_state}
            ],
            "tools": agent,
            "tool_choice": "auto"
        })

        # Print the agent's response
        answer = response["messages"][-1].content
        print(answer)

if __name__ == "__main__":
    main()