
// remove AI agent
world.killPlayer(world.players.find(player => player.name === "AI_Agent")) 

// log to game that the ai agent has been removed
uiLog(">> ai has been removed");