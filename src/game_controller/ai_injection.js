
// create player
world.spawnPlayer();

// take player and rename
world.players.at(-1).name = "AI_Agent";

// re-color AI agent
world.players.find(player => player.name === "AI_Agent").baseColor = "DarkMagenta";
world.players.find(player => player.name === "AI_Agent").flashColor = "Fuchsia";

// mod tick function
world.players.find(player => player.name === "AI_Agent").tick = function tick(world) {
    // run scheduled
    this.runScheduledTasks();
    this.tickCounter++;
    // hit flash cooldown
    if (this.hitTimer > 0) {
        this.hitTimer -= 50
    }
    // charm flash cooldown
    if (this.charmTimer > 0) {
        this.charmTimer -= 50
    }
    // remove if killed
    if (this.health <= 0) {
      world.killPlayer(this);
      return;working
    }
    // movement cooldown based on speed
    this.cooldown -= this.speed;    
    if (this.cooldown <= 0) {
        this.cooldown = world.plannedTPS || 1; // reset based on TPS
    }    
};

// mod level up function
world.players.find(player => player.name === "AI_Agent").checkLevelUp = function checkLevelUp(skill) {
    if (this.xp >= this.nextLevelXp) {
        this.level += 1;
        this.nextLevelXp = (this.level + 1) * 10;
        this.totalXp += this.xp;
        this.xp = 0;
        switch (skill) {
            case "attack":
                this.attack += 1; 
                uiLog(`${this.name} leveled up attack`); 
                break;
            case "maxHealth":
                this.maxHealth += 10; 
                uiLog(`${this.name} leveled up max health`); 
                break;
            case "intelligence":
                this.intelligence += 1; 
                uiLog(`${this.name} leveled up intelligence`); 
                break;
            case "charm":
                this.charm += 1; 
                uiLog(`${this.name} leveled up charm`); 
                break;
            case "speed":
                this.speed = Math.round((this.speed + .5) * 10) / 10;
                uiLog(`${this.name} leveled up speed`);
                break;
        }
    }
}