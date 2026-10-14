from langchain.tools import tool

@tool
def level_up_attack() -> str:
    """Script to make the AI agent level up attack. Attack increases damage dealt to resources and other players."""
    return """world.players.find(player => player.name === 'AI_Agent').lvlUpChoice = 'attack'; uiLog(">> ai lvlUpChoice is now attack");"""

@tool
def level_up_charm() -> str:
    """Script to make the AI agent level up charm. Charm increases the chance other players stop their attack towards you."""
    return """world.players.find(player => player.name === 'AI_Agent').lvlUpChoice = 'charm'; uiLog(">> ai lvlUpChoice is now charm");"""

@tool
def level_up_intelligence() -> str:
    """Script to make the AI agent level up intelligence. Intelligence increases the amount of food gathered from resources and health gained from eating."""
    return """world.players.find(player => player.name === 'AI_Agent').lvlUpChoice = 'intelligence'; uiLog(">> ai lvlUpChoice is now intelligence");"""

@tool
def level_up_maxHealth() -> str:
    """Script to make the AI agent level up max health. Max health increases the total health points of the AI agent."""
    return """world.players.find(player => player.name === 'AI_Agent').lvlUpChoice = 'maxHealth'; uiLog(">> ai lvlUpChoice is now maxHealth");"""

@tool
def level_up_speed() -> str:
    """Script to make the AI agent level up speed. Speed increases movement speed as well as attack speed on both resources and players."""
    return """world.players.find(player => player.name === 'AI_Agent').lvlUpChoice = 'speed'; uiLog(">> ai lvlUpChoice is now speed");"""