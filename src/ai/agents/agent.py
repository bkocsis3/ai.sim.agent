from langchain.agents import create_agent
from models.gpt_5_4_mini import get_gpt_5_4_mini
from tools import game_tools
from pathlib import Path

def create_my_agent():
    llm = get_gpt_5_4_mini()
    tools = [
        game_tools.eat,
        game_tools.gather,
        game_tools.hunt,
        game_tools.wander,
        game_tools.level_up_attack,
        game_tools.level_up_charm,
        game_tools.level_up_intelligence,
        game_tools.level_up_maxHealth,
        game_tools.level_up_speed
    ]
    prompt_path = Path(__file__).resolve().parent.parent / "prompts" / "survive.md"
    prompt = prompt_path.read_text(encoding="utf-8")
    agent = create_agent(
        model=llm,
        tools=tools,
        system_prompt=prompt
    )

    return agent