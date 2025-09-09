BOT_SETTINGS = {
    "enabled":         False,  # disabilitati bot in cash reale
    "bot_count":       0,
    "action_delay_ms": {"min":300,"max":2000}
}

BOT_INTELLIGENCE_SETTINGS = {
    "levels": {},
    "default_profile_params": {}
}

def get_bot_intelligence(level: str):
    return BOT_INTELLIGENCE_SETTINGS["default_profile_params"]