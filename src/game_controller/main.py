from playwright.sync_api import sync_playwright
from pathlib import Path
import json

def main():
    with sync_playwright() as p:
        browser = p.chromium.launch(
            headless=False,
            args=["--start-maximized"]
        )

        # Maximize the browser window
        context = browser.new_context(no_viewport=True)
        page = context.new_page()

        # Open game page
        page.goto("https://bkocsis3.github.io/ai.sim.game")

        # Inject ai agent
        injection_code = Path("src/game_controller/ai_injection.js").read_text(encoding="utf-8")
        page.evaluate(injection_code)

        # Play the game
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
            "kills"
        ]
        state_code = Path("src/game_controller/ai_state.js").read_text(encoding="utf-8")
        while True:
            # get self state
            full_state = page.evaluate(state_code)
            filtered_state = {field: full_state[field] for field in fields}
            print("Self State:", json.dumps(filtered_state, indent=2))

            # get the next action from the AI agent
            # perform action

        #browser.close()

if __name__ == "__main__":
    main()

