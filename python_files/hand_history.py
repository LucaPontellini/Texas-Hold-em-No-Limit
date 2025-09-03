import json
from datetime import datetime
import logging

logger = logging.getLogger(__name__)


class HandHistory:
    """
    Costruisce la cronologia completa di una mano e la esporta in JSON.
    Struttura:
      - hand_id, timestamp, configurazione bui/ante/straddle/button
      - lista di giocatori con seat e stack iniziale
      - lista di azioni con timestamp e fase (PRE_FLOP, FLOP, TURN, RIVER)
      - board separato per flop, turn e river
      - side-pots con importi ed eleggibilità
      - showdown con payouts e rake
    """

    def __init__(self):
        now = datetime.utcnow()
        self.hand = {
            'hand_id':    now.strftime("%Y%m%d%H%M%S%f"),
            'timestamp':  now.isoformat(),
            'button':     None,
            'small_blind': None,
            'big_blind':   None,
            'ante':        None,
            'straddle':    None,
            'players':     [],
            'actions':     [],
            'boards': {
                'flop':  [],
                'turn':  [],
                'river': []
            },
            'side_pots':   [],
            'showdown': {
                'payouts': {},
                'rake':    0
            }
        }

    def record_config(self, button_idx, small_blind, big_blind, ante, straddle):
        """
        Registra posizione bottone e rilevamenti bui/ante/straddle.
        Chiamare subito dopo start_hand().
        """
        self.hand['button']      = button_idx
        self.hand['small_blind'] = small_blind
        self.hand['big_blind']   = big_blind
        self.hand['ante']        = ante
        self.hand['straddle']    = straddle

    def record_player(self, player, seat_idx):
        """
        Registra ogni giocatore con nome, seat e stack iniziale.
        """
        self.hand['players'].append({
            'name':           player.name,
            'seat':           seat_idx,
            'starting_chips': player.chips
        })

    def record_action(self, player, action, amount, phase):
        """
        Registra un’azione:
          - player: nome
          - action: 'fold', 'call', 'raise', etc.
          - amount: importo puntato
          - phase: BettingRound enum
          - timestamp: ISO
        """
        self.hand['actions'].append({
            'timestamp': datetime.utcnow().isoformat(),
            'player':    player.name,
            'action':    action,
            'amount':    amount,
            'phase':     phase.name
        })

    def record_board(self, cards, phase):
        """
        Registra il board per la fase specifica:
        - phase.name in ('FLOP','TURN','RIVER')
        """
        key = phase.name.lower()
        if key in self.hand['boards']:
            self.hand['boards'][key] = [str(c) for c in cards]
        else:
            logger.warning("Phase %s non valida per board", phase)

    def record_side_pots(self, side_pots):
        """
        side_pots: lista di dict {'amount': int, 'eligible': [Player,...]}
        """
        formatted = []
        for pot in side_pots:
            formatted.append({
                'amount':   pot['amount'],
                'eligible': [p.name for p in pot['eligible']]
            })
        self.hand['side_pots'] = formatted

    def record_showdown(self, payouts, rake):
        """
        Registra payout per vincitore e rake finale.
        """
        self.hand['showdown']['payouts'] = {p.name: amt for p, amt in payouts.items()}
        self.hand['showdown']['rake']    = rake

    def export(self, path):
        """
        Esporta la hand history in JSON indentato.
        """
        try:
            with open(path, 'w') as f:
                json.dump(self.hand, f, indent=2)
            logger.info("Hand history exported to %s", path)
        except Exception as e:
            logger.error("Errore esportazione hand history: %s", e)