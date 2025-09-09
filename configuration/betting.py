BETTING_RULES = {
    "no_limit":         True,
    "min_raise_rule":   "previous_bet",
    "raise_increment":  1,
    "all_in_allowed":   True,
    "betting_clock":    None,     # disabilitato per cash live
    "max_raises_per_street": None
}

ACTIONS_SETTINGS = {
    "allowed_actions": [
        "fold","check","call","raise","all_in"
    ],
    "string_bet_allowed":  False,
    "must_announce_raise": True
}