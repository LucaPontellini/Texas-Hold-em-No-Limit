from .general import GENERAL

PLAYER_SETTINGS = {
    "seat_count":       GENERAL["max_players"],
    "human_player":     {"seat": 1, "id": "LOCAL_USER"},
    "bot_player_count": GENERAL["max_players"] - 2,
    "dealer":           {"type": "AI", "is_player": False}
}