# AI.Sim.Agent

AI.Sim.Agent is a Python agent that plays [AI.Sim.Game](https://bkocsis3.github.io/ai.sim.game). It uses a LangChain agent backed by OpenAI's `gpt-5.4-mini` model to choose an in-game action and a character upgrade. Playwright opens the game in Chromium, adds the AI player, reads the game state, and executes the JavaScript returned by the agent.

## Requirements

- Python 3.10 or newer
- An OpenAI API key with access to `gpt-5.4-mini`
- A working internet connection

## Setup

Run these commands from the repository root.

### Windows Command Prompt

```powershell
py -m venv venv
venv\Scripts\activate.bat
python -m pip install --upgrade pip
python -m pip install -e ".[dev]"
python -m playwright install chromium
```

If PowerShell prevents activation, either allow script activation for the current terminal or run the environment's Python directly as `venv\Scripts\python.exe`.

### macOS or Linux

```bash
python3 -m venv venv
source venv/bin/activate
python -m pip install --upgrade pip
python -m pip install -e ".[dev]"
python -m playwright install chromium
```

Create `src/ai/config/.env` and add your API key:

```dotenv
OPENAI_API_KEY=your_openai_api_key
```

Keep this file private and do not commit your API key. The application loads this path when run from the repository root.

## Run the Game Agent

From the repository root, with the virtual environment active:

```bash
python -m game_controller.main
```

The controller opens a visible Chromium window and navigates to the hosted game. It injects a player named `AI_Agent`, reads that player's state plus the player and resource counts, and asks the model to choose one action and one level-up option. The returned JavaScript is evaluated in the game page.

The current controller runs for at most five iterations and waits 30 seconds after each action. It prints the state and the agent's response to the terminal. Close the browser or interrupt the Python process to stop early.

## Interactive Agent Input

`src/ai/main.py` provides a text-based way to send a JSON state to the agent without opening the game:

```bash
python src/ai/main.py
```

Enter a JSON object representing the agent state at the prompt, or enter `quit` to exit. This mode prints the agent response; it does not execute the response in the game.

## Project Layout

```text
src/
	ai/
		agents/       Agent construction and tool registration
		config/       Environment-variable loading
		models/       OpenAI chat model configuration
		prompts/      Agent behavior instructions
		tools/        Game actions and level-up choices
		workflows/    Placeholder for future graph workflows
	game_controller/
		main.py       Playwright game loop
		scripts/      JavaScript for injection and game-state queries
tests/            Python tests
```

The system prompt in `src/ai/prompts/survive.md` asks the agent to choose exactly one action (`gather`, `hunt`, or `wander`) and one upgrade (`attack`, `charm`, `intelligence`, `maxHealth`, or `speed`). The tools in `src/ai/tools/` return JavaScript snippets that update the injected player's state in the game.

## Notes

- Run commands from the repository root: the controller reads its JavaScript files using paths relative to that directory.
- The game is hosted externally; this project does not include or start the game server.
- The `ai.workflows.graph` module is currently a placeholder and is not used by the game controller.
