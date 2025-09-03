import logging
import time

import config

logger = logging.getLogger(__name__)


class TournamentManager:
    """
    Gestisce livelli di bui, pause, re-buy e add-on in modalità torneo.
    """

    def __init__(self):
        self.level_idx       = 0
        self.level_start_ts  = None
        self.rebuys_used     = set()
        self._level_up_cb    = None
        # Track delle pause già erogate
        self._breaks_done    = set()

    def start_tournament(self):
        """
        Inizializza il torneo al primo livello,
        azzera timer, rebuys e break.
        """
        self.level_idx      = 0
        self.level_start_ts = None
        self.rebuys_used.clear()
        self._breaks_done.clear()
        logger.info("Tournament started at level 0")

    def get_current_level(self):
        """Restituisce la configurazione corrente di bui."""
        return config.TOURNAMENT_BLINDS_STRUCTURE[self.level_idx]

    def advance_level_if_needed(self, now_ts=None):
        """
        Controlla se scaduta la durata del livello corrente
        e avanza al successivo. Se avanza, richiama il callback
        registrato via on_level_up().
        Returns True se effettua l'avanzamento.
        """
        now = now_ts if now_ts is not None else time.time()
        lvl = self.get_current_level()

        # prima chiamata: inizio livello
        if self.level_start_ts is None:
            self.level_start_ts = now
            logger.info(
                "Level %d started: %d/%d",
                lvl['level'], lvl['small_blind'], lvl['big_blind']
            )
            return False

        # check pausa
        br = self._next_break_due()
        if br:
            # pausa da gestire a livello di Game/UI
            logger.info(
                "Break %d seconds due after level %d",
                br['duration'], br['after_level']
            )
            return False

        # se durata livello trascorsa, avanza
        if now - self.level_start_ts >= lvl['duration']:
            prev = lvl['level']
            self.level_idx = min(
                self.level_idx + 1,
                len(config.TOURNAMENT_BLINDS_STRUCTURE) - 1
            )
            self.level_start_ts = now
            new = self.get_current_level()
            logger.info(
                "Advanced from level %d to %d: %d/%d",
                prev, new['level'],
                new['small_blind'], new['big_blind']
            )
            # callback esterno
            if self._level_up_cb:
                try:
                    self._level_up_cb(new)
                except Exception as e:
                    logger.error("Level-up callback error: %s", e)
            return True

        return False

    def on_level_up(self, callback):
        """
        Registra un callback(level_config) chiamato a ogni avanzamento.
        """
        self._level_up_cb = callback

    def _next_break_due(self):
        """
        Controlla se è il momento di una pausa definita in config.TOURNAMENT_BREAKS.
        Restituisce la config della pausa (dict) o None.
        """
        breaks = getattr(config, 'TOURNAMENT_BREAKS', [])
        for br in breaks:
            lvl = br.get('after_level')
            if (self.level_idx == lvl
                    and br.get('duration', 0) > 0
                    and lvl not in self._breaks_done):
                # segna pausa consumata
                self._breaks_done.add(lvl)
                return br
        return None

    def is_final_level(self):
        """True se siamo all'ultimo livello dei bui."""
        return self.level_idx == len(config.TOURNAMENT_BLINDS_STRUCTURE) - 1

    def is_tournament_over(self, now_ts=None):
        """
        True se al final level è trascorsa la sua durata.
        """
        now = now_ts if now_ts is not None else time.time()
        if not self.is_final_level():
            return False
        lvl = self.get_current_level()
        return (self.level_start_ts is not None
                and (now - self.level_start_ts) >= lvl['duration'])

    def allow_rebuy(self, player, now_ts=None):
        """
        Esegue il rebuy se abilitato, ancora non usato, e
        nel periodo consentito (config.REBUY_PERIOD_DURATION).
        Ritorna True se il rebuy è stato concesso.
        """
        if not config.REBUY_ALLOWED:
            return False
        if player in self.rebuys_used:
            return False

        now = now_ts if now_ts is not None else time.time()
        start = self.level_start_ts or now
        window = getattr(config, 'REBUY_PERIOD_DURATION', 0)
        if window > 0 and (now - start) > window:
            logger.info("%s missed rebuy window", player.name)
            return False

        # concede rebuy
        self.rebuys_used.add(player)
        player.chips += config.REBUY_CHIPS
        logger.info("%s rebought %d chips", player.name, config.REBUY_CHIPS)
        return True

    def allow_add_on(self, player, now_ts=None):
        """
        Esegue l'add-on se abilitato. Puoi applicare
        logiche simili a allow_rebuy per window temporale.
        """
        if not config.ADD_ON_ALLOWED:
            return False

        # se vuoi timeline, puoi usare REBUY_PERIOD_DURATION o
        # definire config.ADD_ON_PERIOD_DURATION
        now = now_ts if now_ts is not None else time.time()
        # esempio: stessa finestra dei rebuys
        window = getattr(config, 'REBUY_PERIOD_DURATION', 0)
        start = self.level_start_ts or now
        if window > 0 and (now - start) > window:
            logger.info("%s missed add-on window", player.name)
            return False

        player.chips += config.ADD_ON_CHIPS
        logger.info("%s took add-on of %d chips", player.name, config.ADD_ON_CHIPS)
        return True