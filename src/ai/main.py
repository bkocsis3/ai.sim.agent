from agents.agent import create_my_agent

def main():
    agent = create_my_agent()
    self_state = input(
        "Enter the self state (JSON format) of the AI agent: "
    )

    response = agent.invoke({
        "messages": [
            {"role": "user", "content": self_state}
        ],
        "tools": agent,
        "tool_choice": "auto"
    })

    answer = response["messages"][-1].content
    print("\nAnswer:\n", answer)

if __name__ == "__main__":
    main()