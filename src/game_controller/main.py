from playwright.sync_api import sync_playwright
from pathlib import Path
import json
import time
from ai.agents.agent import create_my_agent

def main():
    # Start the ai agent
    agent = create_my_agent()

    # Start playwright
    with sync_playwright() as p:
        # Launch the browser
        browser = p.chromium.launch(
            headless=False,
            args=["--start-maximized"]
        )

        # Maximize the browser window
        context = browser.new_context(no_viewport=True)
        page = context.new_page()

        # Open game page
        page.goto("https://bkocsis3.github.io/ai.sim.game")

        # Create ai agent game object
        injection_code = Path("src/game_controller/scripts/ai_injection.js").read_text(encoding="utf-8")
        page.evaluate(injection_code)

        # Set pre-loop variables
        fields = [
            "name", 
            "age", 
            "health", 
            "x", 
            "y", 
            "level", 
            "xp",
            "nextLevelXp",
            "totalXp",
            "attack",
            "charm",
            "intelligence",
            "maxHealth",
            "speed",
            "food",
            "kills",
            "actionState",
            "lvlUpChoice"
        ]
        state_code = Path("src/game_controller/scripts/ai_state.js").read_text(encoding="utf-8")

        loop_count = 0

        # Main loop to interact with the agent and the game
        while True:
            # Get self state
            full_state = page.evaluate(state_code)
            filtered_state = json.dumps({field: full_state[field] for field in fields}, indent=2)
            print(f"Current state: {filtered_state}")

            # Break the loop if the agent is dead
            if full_state["health"] <= 0 or loop_count >= 10: 
                break

            # Invoke the agent with the self state
            response = agent.invoke({
                "messages": [
                    {"role": "user", "content": filtered_state}
                ],
                "tools": agent,
                "tool_choice": "auto"
            })
            
            # Get the agent's response
            answer = response["messages"][-1].content
            print(f"Agent's response: {answer}")

            # Send the agent's response to the game
            try:
                page.evaluate(answer)
                time.sleep(30) # Wait for 30 seconds before the next iteration
            except Exception as e:
                print(f"Error occurred while evaluating answer: {e}")

            # Increment the loop count
            loop_count += 1

if __name__ == "__main__":
    main()

