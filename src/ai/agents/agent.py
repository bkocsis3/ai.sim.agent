from langchain.agents import create_agent
from ai.models.gpt_5_4_mini import get_gpt_5_4_mini
from ai.tools import action_tools, leveling_tools
from pathlib import Path

def create_my_agent():
    llm = get_gpt_5_4_mini()
    tools = [
        action_tools.gather,
        action_tools.hunt,
        action_tools.wander,
        leveling_tools.level_up_attack,
        leveling_tools.level_up_charm,
        leveling_tools.level_up_intelligence,
        leveling_tools.level_up_maxHealth,
        leveling_tools.level_up_speed
    ]
    prompt_path = Path(__file__).resolve().parent.parent / "prompts" / "survive.md"
    prompt = prompt_path.read_text(encoding="utf-8")
    agent = create_agent(
        model=llm,
        tools=tools,
        system_prompt=prompt
    )

    return agent