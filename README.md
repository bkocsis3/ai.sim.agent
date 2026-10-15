# AI.Sim.Agent

AI.Sim.Agent is a Python agent that plays [AI.Sim.Game](https://bkocsis3.github.io/ai.sim.game). It uses a LangChain agent backed by OpenAI's `gpt-5.4-mini` model to choose an in-game action and a character upgrade. Playwright opens the game in Chromium, adds the AI player, reads the game state, and executes the JavaScript returned by the agent.

## Requirements

- Python 3.10 or newer
- An OpenAI API key with access to `gpt-5.4-mini`
- A working internet connection

## Setup

Run these commands from the repository root.

### Windows PowerShell

```powershell
py -m venv venv
.\venv\Scripts\Activate.ps1
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

The game controller uses an interactive command prompt:

```text
start game   Open Chromium and load AI.Sim.Game
inject ai    Add AI_Agent and start the agent loop
quit         Stop the loop, close the browser, and exit
```

Start the game before injecting the AI. The controller reads the AI player's state, along with player and resource counts, then asks the model to choose an action and a level-up option. It evaluates the returned JavaScript in the game page and prints the agent's response in the terminal.

The loop runs for up to 12 iterations, with a 15-second delay between actions. When the AI dies or reaches the iteration limit, enter `inject ai` to restart it, or `quit` to close the game. The CLI remains available between iterations; handling a command may pause while the model is generating a response.

The controller uses async Playwright and an asyncio task for the game loop. Type `quit` to shut down cleanly rather than closing the browser directly.

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
		main.py       Interactive async game-controller CLI
		scripts/      JavaScript for injection and game-state queries
tests/            Python tests
```

The system prompt in `src/ai/prompts/survive.md` asks the agent to choose exactly one action (`gather`, `hunt`, or `wander`) and one upgrade (`attack`, `charm`, `intelligence`, `maxHealth`, or `speed`). The tools in `src/ai/tools/` return JavaScript snippets that update the injected player's state in the game.

## Notes

- Run commands from the repository root: the controller reads its JavaScript files using paths relative to that directory.
- The game is hosted externally; this project does not include or start the game server.
- The `ai.workflows.graph` module is currently a placeholder and is not used by the game controller.