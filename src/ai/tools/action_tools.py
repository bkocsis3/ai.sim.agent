from langchain.tools import tool

@tool
def gather() -> str:
    """Script to make the AI agent gather resources."""
    return """world.players.find(player => player.name === 'AI_Agent').actionState = 'gather'; uiLog("ai actionState is now gather");"""

@tool
def hunt() -> str:
    """Script to make the AI agent hunt enemies."""
    return """world.players.find(player => player.name === 'AI_Agent').actionState = 'hunt'; uiLog("ai actionState is now hunt");"""

@tool
def wander() -> str:
    """Script to make the AI agent wander."""
    return """world.players.find(player => player.name === 'AI_Agent').actionState = 'wander'; uiLog("ai actionState is now wander");"""