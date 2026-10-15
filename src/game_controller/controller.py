import asyncio
import json
from pathlib import Path
from playwright.async_api import async_playwright
from ai.agents.agent import create_my_agent
import sys

def safe_print(msg: str):
    # Erase the current input line completely
    sys.stdout.write("\033[2K\r")
    # Print the log on its own line
    print(f"\n\033[33m{msg}\033[0m\n") # space and color yellow
    # Reprint the prompt on the SAME line
    sys.stdout.write(">> game controller: ")
    sys.stdout.flush()

class GameController:
    def __init__(self):
        self.playwright = None
        self.browser = None
        self.context = None
        self.page = None
        self.agent = None
        self.ai_task = None
        self.alive = False
        self.stop_loop = False
        self.max_iterations = 12
        self.remaining_iteration = self.max_iterations
        self.iteration_delay = 15
        self.logs = []

        self.logbox_decor_code = Path("src/game_controller/scripts/logbox_decor.js").read_text()
        self.ai_state_code = Path("src/game_controller/scripts/ai_state.js").read_text()
        self.player_count_code = Path("src/game_controller/scripts/player_count.js").read_text()
        self.resource_count_code = Path("src/game_controller/scripts/resource_count.js").read_text()
        self.injection_code = (
            self.logbox_decor_code + 
            Path("src/game_controller/scripts/ai_injection.js").read_text() +
            self.logbox_decor_code
        )
        self.removal_code = (
            self.logbox_decor_code + 
            Path("src/game_controller/scripts/ai_removal.js").read_text() +
            self.logbox_decor_code 
        )

    async def start_game(self):
        if self.browser:
            print("\tGame already running.")
            return

        print("\tStarting game...")
        self.agent = create_my_agent()

        self.playwright = await async_playwright().start()
        self.browser = await self.playwright.chromium.launch(
            headless=False,
            args=["--start-maximized"]
        )
        self.context = await self.browser.new_context(no_viewport=True)
        self.page = await self.context.new_page()

        await self.page.goto("https://bkocsis3.github.io/ai.sim.game")
        print("\tGame loaded.")

    async def inject_ai(self):
        if not self.page:
            print("\tGame not started.")
            return

        ai_state = await self.page.evaluate(self.ai_state_code)
        if ai_state:
            print("\tAI agent is already alive.")
            return

        print("\tInjecting AI...")
        self.remaining_iterations = self.max_iterations
        await self.page.evaluate(self.injection_code)
        await asyncio.sleep(2)

        ai_state = await self.page.evaluate(self.ai_state_code)
        self.alive = bool(ai_state)

        if self.alive:
            print("\tAI injected. Starting loop...")
            await self.start_ai_loop()
        else:
            print("\tAI injection failed.")

    async def start_ai_loop(self):
        if self.ai_task and not self.ai_task.done():
            print("\tAI loop is already running.")
            return

        self.stop_loop = False
        self.ai_task = asyncio.create_task(self.run_ai_loop())

    async def run_ai_loop(self):
        print("\tAI loop started.")

        fields = [
            "name", "age", "health", "x", "y", "level", "xp",
            "nextLevelXp", "totalXp", "attack", "charm",
            "intelligence", "maxHealth", "speed", "food",
            "kills", "actionState", "lvlUpChoice"
        ]

        while not self.stop_loop:
            if self.remaining_iterations == 0:
                await self.page.evaluate(self.removal_code)
                safe_print("Max iterations reached. Type 'inject ai' to restart or 'quit' to exit.")
                return
            self.remaining_iterations -= 1        

            ai_state = await self.page.evaluate(self.ai_state_code)
            if not ai_state:
                safe_print("AI agent died. Type 'inject ai' to restart or 'quit' to exit.")
                self.alive = False
                return

            filtered_ai_state = {field: ai_state[field] for field in fields}
            player_count = await self.page.evaluate(self.player_count_code)
            resource_count = await self.page.evaluate(self.resource_count_code)

            combined_state = {
                **filtered_ai_state,
                "playerCount": player_count,
                "resourceCount": resource_count
            }

            response = self.agent.invoke({
                "messages": [
                    {"role": "user", "content": json.dumps(combined_state, indent=2)}
                ],
                "tools": self.agent,
                "tool_choice": "auto"
            })

            reasoning = response["messages"][-1].content
            combined_tool_msg_content = "".join(
                msg.content
                for msg in response["messages"]
                if msg.__class__.__name__ == "ToolMessage"
            )

            answer_code = (
                self.logbox_decor_code +
                combined_tool_msg_content +
                reasoning +
                self.logbox_decor_code
            )

            try:
                await self.page.evaluate(answer_code)
                safe_print(reasoning)
                await asyncio.sleep(self.iteration_delay)
            except Exception as e:
                safe_print(f"Error evaluating answer: {e}")
                safe_print("AI agent likely died mid iteration. Type 'inject ai' to restart or 'quit' to exit.")
                return

        print("\tAI loop stopped.")

    async def quit(self):
        print("\tClosing...")
        self.stop_loop = True

        if self.ai_task:
            await asyncio.sleep(1)

        if self.browser:
            await self.browser.close()

        if self.playwright:
            await self.playwright.stop()

        print("\tClosed.")