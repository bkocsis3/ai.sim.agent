from playwright.sync_api import sync_playwright
from pathlib import Path
import json
import time
from ai.agents.agent import create_my_agent

def main():
    ### Start the ai agent
    agent = create_my_agent()

    ### Start playwright
    with sync_playwright() as p:
        ### Launch the browser
        browser = p.chromium.launch(
            headless=False,
            args=["--start-maximized"]
        )

        ### Maximize the browser window
        context = browser.new_context(no_viewport=True)
        page = context.new_page()

        ### Open game page
        page.goto("https://bkocsis3.github.io/ai.sim.game")

        ### Create ai agent game object
        injection_code = Path("src/game_controller/scripts/ai_injection.js").read_text(encoding="utf-8")
        page.evaluate(injection_code)

        ### Set pre-loop variables
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

        ai_state_code = Path("src/game_controller/scripts/ai_state.js").read_text(encoding="utf-8")
        player_count_code = Path("src/game_controller/scripts/player_count.js").read_text(encoding="utf-8")
        resource_count_code = Path("src/game_controller/scripts/resource_count.js").read_text(encoding="utf-8")
        logbox_decor_code = Path("src/game_controller/scripts/logbox_decor.js").read_text(encoding="utf-8")

        loop_count = 0

        ### Main loop to interact with the agent and the game
        while True:
            ### Break the loop if the agent is dead or if the loop count exceeds a certain threshold
            if loop_count >= 4: 
                print(f"Maximum iteration has been reached. Stopping AI agent...\n")
                break

            ### Get ai state
            ai_state = page.evaluate(ai_state_code)
            if not ai_state:
                print(f"Failed to retrieve AI agent state. Agent may have died.\n")
                break
            filtered_ai_state = {field: ai_state[field] for field in fields}

            ### Get player and resource counts
            player_count = page.evaluate(player_count_code)
            resource_count = page.evaluate(resource_count_code)

            ### Combine ai state with player and resource counts into json format
            combined_state = {
                **filtered_ai_state,
                "playerCount": player_count,
                "resourceCount": resource_count
            }
            print(f"Current state:\n {combined_state}\n" )

            ### Invoke the agent
            response = agent.invoke({
                "messages": [
                    {"role": "user", "content": json.dumps(combined_state, indent=2)}
                ],
                "tools": agent,
                "tool_choice": "auto"
            })

            ### Get reasoning
            reasoning = response["messages"][-1].content
            
            ### Get tool returns
            combined_tool_msg_content = "".join(
                msg.content
                for msg in response["messages"]
                if msg.__class__.__name__ == "ToolMessage"
            )

            ### Craft answer code
            answer_code = logbox_decor_code + combined_tool_msg_content + reasoning + logbox_decor_code
            print(f"Answer code:\n {answer_code}\n")

            ### Send answer code to the game
            try:
                page.evaluate(answer_code)
                time.sleep(15) # Wait for 15 seconds before the next iteration
            except Exception as e:
                print(f"Error occurred while evaluating answer: {e}\n")

            ### Increment the loop count
            loop_count += 1
            print(f"Iteration: {loop_count} complete\n")

if __name__ == "__main__":
    main()

