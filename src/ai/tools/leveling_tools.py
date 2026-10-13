from langchain.tools import tool

@tool
def level_up_attack() -> str:
    """Script to make the AI agent level up attack."""
    return """world.players.find(player => player.name === 'AI_Agent').lvlUpChoice = 'attack'; uiLog("ai lvlUpChoice is now attack");"""

@tool
def level_up_charm() -> str:
    """Script to make the AI agent level up charm."""
    return """world.players.find(player => player.name === 'AI_Agent').lvlUpChoice = 'charm'; uiLog("ai lvlUpChoice is now charm");"""

@tool
def level_up_intelligence() -> str:
    """Script to make the AI agent level up intelligence."""
    return """world.players.find(player => player.name === 'AI_Agent').lvlUpChoice = 'intelligence'; uiLog("ai lvlUpChoice is now intelligence");"""

@tool
def level_up_maxHealth() -> str:
    """Script to make the AI agent level up max health."""
    return """world.players.find(player => player.name === 'AI_Agent').lvlUpChoice = 'maxHealth'; uiLog("ai lvlUpChoice is now maxHealth");"""

@tool
def level_up_speed() -> str:
    """Script to make the AI agent level up speed."""
    return """world.players.find(player => player.name === 'AI_Agent').lvlUpChoice = 'speed'; uiLog("ai lvlUpChoice is now speed");"""