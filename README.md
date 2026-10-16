# AI.Sim.Agent

This repo provides a customizable AI agent that gets injected into [AI.Sim.Lab](https://bkocsis3.github.io/ai.sim.lab). It currently uses a LangChain agent backed by OpenAI's `gpt-5.4-mini` model to choose actions and  character upgrades. Playwright opens the simulation in Chromium, adds the AI agent, reads the simulation state, and executes the JavaScript returned by the agent's decision.

The main goal of this project is to experiment and learn how different prompts, LLMs, tools, memory, etc affect behavior.

# Screenshots
From the Lab:

![Lab](/screenshots/lab.png)

From the CLI:

![CLI](/screenshots/cli.png?raw=true)

## Requirements

- Python 3.10 or newer
- An OpenAI API key
- A working internet connection

## Setup

Run these commands from the repository root.

### Windows Command Prompt

```powershell
py -m venv venv
venv\Scripts\activate
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

## Run the Agent

From the repository root, with the virtual environment active:

```bash
python -m cli.main
```

The controller uses an interactive command prompt:

```text
start sim    Open Chromium and load AI.Sim.Lab
inject ai    Add AI agent and start the decision loop
quit         Stop the loop, close the browser, and exit
```

Start the simulation before injecting the AI. The controller reads the AI agent's state, along with player and resource counts, then asks the model to choose an action and a level-up option. It evaluates the returned JavaScript in the simulation and prints the agent's response in the log box.

The loop runs for up to 12 iterations, with a 15-second delay between actions. When the agent dies or reaches the iteration limit, enter `inject ai` to restart it, or `quit` to close the session. The CLI remains available between iterations; handling a command may pause while the model is generating a response.

The controller uses async Playwright and an asyncio task for the decision loop. Type `quit` to shut down cleanly rather than closing the browser directly.

## Interactive Agent Input

`src/ai/main.py` provides a text-based way to send a JSON state to the agent without opening the simulation:

```bash
python src/ai/main.py
```

Enter a JSON object representing the agent state at the prompt, or enter `quit` to exit. This mode prints the agent response; it does not execute the response in the lab/simulation.

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
	cli/
		main.py       Interactive async controller CLI
		controller.py Injects AI agent and decisions into simulation
		scripts/      JavaScript for injection and sim-state queries
tests/                Placeholder for future tests
```

The system prompt in `src/ai/prompts/survive.md` asks the agent to choose exactly one action (`gather`, `hunt`, or `wander`) and one upgrade (`attack`, `charm`, `intelligence`, `maxHealth`, or `speed`). The tools in `src/ai/tools/` return JavaScript snippets that update agent's choices in the simulation.

## Notes

- Run commands from the repository root: the controller reads its JavaScript files using paths relative to that directory.
- The lab/simulation is hosted externally; this project does not include or start the lab server.
- The `ai.workflows.graph` module is currently a placeholder and is not used by the controller.
