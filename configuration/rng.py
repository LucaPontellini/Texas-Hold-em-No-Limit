from .deck import DECK_SETTINGS

RNG_SETTINGS = {
    "algorithm":          DECK_SETTINGS["shuffle_algorithm"],
    "secure_seed":        True,
    "audit_log_enabled":  True,
    "hand_replay_enabled": True
}