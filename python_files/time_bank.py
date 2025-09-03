import time
import logging
import config

logger = logging.getLogger(__name__)

class TimeBank:
    """
    Time-bank per ciascun Player:
      - remaining: secondi rimanenti
      - last_action_ts: quando è iniziata l’ultima azione
    """

    def __init__(self):
        self.remaining      = config.TIME_BANK_SECONDS
        self.last_action_ts = None

    def start_action(self):
        """Avvia il conteggio se abilitato."""
        if not config.TIME_BANK_ENABLED:
            return
        self.last_action_ts = time.monotonic()

    def stop_action(self):
        """Ferma il conteggio e riduce remaining."""
        if not config.TIME_BANK_ENABLED or self.last_action_ts is None:
            return
        elapsed = time.monotonic() - self.last_action_ts
        self.remaining = max(0, self.remaining - elapsed)
        self.last_action_ts = None
        logger.debug("TimeBank: %ds left", self.remaining)

    def refresh(self, new_level: bool = False):
        """
        Ricarica la riserva.
        - se new_level=True (es. cambio bui/nuovo round), reset completo
        - altrimenti ricarica di TIME_BANK_REFRESH_AMOUNT
        """
        if not config.TIME_BANK_ENABLED:
            return

        if new_level:
            self.remaining = config.TIME_BANK_SECONDS
            logger.debug("TimeBank reset to %ds on new level", self.remaining)
        else:
            added = config.TIME_BANK_REFRESH_AMOUNT if config.TIME_BANK_REFRESH else 0
            self.remaining = min(config.TIME_BANK_SECONDS, self.remaining + added)
            logger.debug("TimeBank refreshed to %ds", self.remaining)

    def reset(self):
        """Chiamare all’inizio di ogni mano per standardizzare lo stato."""
        self.remaining      = config.TIME_BANK_SECONDS
        self.last_action_ts = None

    def is_expired(self) -> bool:
        """True se la riserva è finita."""
        if not config.TIME_BANK_ENABLED:
            return False
        expired = self.remaining <= 0
        if expired:
            logger.info("TimeBank expired")
        return expired