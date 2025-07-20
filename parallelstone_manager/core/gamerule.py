minecraft_gamerules = {
    "allowFireTicksAwayFromPlayer": False,
    "announceAdvancements": True,
    "blockExplosionDropDecay": True,
    "commandBlockOutput": True,
    "commandModificationBlockLimit": 32768,
    "disableElytraMovementCheck": False,
    "disablePlayerMovementCheck": False,
    "disableRaids": False,
    "doDaylightCycle": True,
    "doEntityDrops": True,
    "doFireTick": True,
    "doImmediateRespawn": False,
    "doInsomnia": True,
    "doLimitedCrafting": False,
    "doMobLoot": True,
    "doMobSpawning": True,
    "doPatrolSpawning": True,
    "doTileDrops": True,
    "doTraderSpawning": True,
    "doVinesSpread": True,
    "doWeatherCycle": True,
    "doWardenSpawning": True,
    "drowningDamage": True,
    "enderPearlsVanishOnDeath": True,
    "fallDamage": True,
    "fireDamage": True,
    "forgiveDeadPlayers": True,
    "freezeDamage": True,
    "globalSoundEvents": True,
    "keepInventory": False,
    "lavaSourceConversion": False,
    "locatorBar": True,
    "logAdminCommands": True,
    "maxCommandChainLength": 65536,
    "maxCommandForkCount": 65536,
    "maxEntityCramming": 24,
    "minecartMaxSpeed": 8,  # Experimental feature only
    "mobExplosionDropDecay": True,
    "mobGriefing": True,
    "naturalRegeneration": True,
    "playersNetherPortalCreativeDelay": 0,
    "playersNetherPortalDefaultDelay": 80,
    "playersSleepingPercentage": 100,
    "projectilesCanBreakBlocks": True,
    "randomTickSpeed": 3,  # Java Edition (Bedrock: 1)
    "reducedDebugInfo": False,
    "sendCommandFeedback": True,
    "showDeathMessages": True,
    "snowAccumulationHeight": 1,
    "spawnChunkRadius": 2,
    "spawnRadius": 10,
    "spectatorsGenerateChunks": True,
    "tntExplodes": True,
    "tntExplosionDropDecay": False,
    "universalAnger": False,
    "waterSourceConversion": True,
}

def check_rule_value(rule: str, value: str) -> bool:
    if rule not in minecraft_gamerules:
        raise ValueError(f"Unknown game rule: {rule}")

    expected_type = type(minecraft_gamerules[rule])

    if expected_type == bool:
        return value.lower() in ("true", "false")

    elif expected_type == int:
        try:
            int(value)
            return True
        except ValueError:
            return False
    else:
        return False