ACTIONS_SETTINGS = {
    # Lista delle azioni consentite al tavolo
    "allowed_actions": [
        "fold",
        "check",
        "call",
        "raise",
        "all_in"
    ],
    # Se True, permette di scomporre una puntata in più chip (string bet),
    # altrimenti impone di dichiarare l'importo in un’unica azione
    "string_bet_allowed": False,
    # Se True, impone di annunciare “raise” prima di specificare l’importo del rilancio
    "must_announce_raise": True
}