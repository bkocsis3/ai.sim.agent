from langchain.tools import tool

@tool
def eat() -> str:
    """Script to make the AI agent eat."""
    return "world.players.find(player => player.name === 'AI_Agent').eat();"

@tool
def gather() -> str:
    """Script to make the AI agent gather resources."""
    return """food = world.findNearestResource(world.players.find(player => player.name === 'AI_Agent'));
if (food) {world.players.find(player => player.name === 'AI_Agent').moveToward(world, food.x, food.y);}"""  

@tool
def hunt() -> str:
    """Script to make the AI agent hunt enemies."""
    return """enemy = world.findNearestEnemy(world.players.find(player => player.name === 'AI_Agent'));
if (enemy) {world.players.find(player => player.name === 'AI_Agent').moveToward(world,enemy.x,enemy.y);}"""

@tool
def wander() -> str:
    """Script to make the AI agent wander."""
    return "world.players.find(player => player.name === 'AI_Agent').wander(world);"

@tool
def level_up_attack() -> str:
    """Script to make the AI agent level up attack."""
    return "world.players.find(player => player.name === 'AI_Agent').checkLevelUp('attack');"

@tool
def level_up_charm() -> str:
    """Script to make the AI agent level up charm."""
    return "world.players.find(player => player.name === 'AI_Agent').checkLevelUp('charm');"

@tool
def level_up_intelligence() -> str:
    """Script to make the AI agent level up intelligence."""
    return "world.players.find(player => player.name === 'AI_Agent').checkLevelUp('intelligence');"

@tool
def level_up_maxHealth() -> str:
    """Script to make the AI agent level up max health."""
    return "world.players.find(player => player.name === 'AI_Agent').checkLevelUp('maxHealth');"

@tool
def level_up_speed() -> str:
    """Script to make the AI agent level up speed."""
    return "world.players.find(player => player.name === 'AI_Agent').checkLevelUp('speed');"

