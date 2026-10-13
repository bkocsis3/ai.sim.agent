
// create player
world.spawnPlayer();

// take player and rename
world.players.at(-1).name = "AI_Agent";

// re-color AI agent
world.players.find(player => player.name === "AI_Agent").baseColor = "DarkMagenta";
world.players.find(player => player.name === "AI_Agent").flashColor = "Fuchsia";

// add attributes to AI agent
world.players.find(player => player.name === "AI_Agent").lvlUpChoice = "attack";
world.players.find(player => player.name === "AI_Agent").actionState = "gather";

// mod tick function
world.players.find(player => player.name === "AI_Agent").tick = function tick(world) {
    // eat if hungry
    if (this.health < (this.maxHealth * .5) && this.food > 0) {this.eat();}
    // level up if possible
    this.checkLevelUp(this.lvlUpChoice);
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
      return;
    }
    // movement based on speed
    this.cooldown -= this.speed;
    if (this.cooldown <= 0) {
        this.cooldown = world.plannedTPS || 1; // reset based on TPS
        switch (this.actionState) {
        case "gather":
            const nearest = world.findNearestResource(this);
            if (nearest) {
                this.moveToward(world, nearest.x, nearest.y);
                return;
            }
        case "hunt":
            const enemy = world.findNearestEnemy(this);
            if (enemy) {
                this.moveToward(world, enemy.x, enemy.y);
                return;
            }
        case "wander":
            this.wander(world);
        }
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

// log to game that the ai agent has been injected
uiLog(">> ai has been injected");