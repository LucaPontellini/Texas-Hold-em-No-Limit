import logging
from random import Random
from deck import Deck, DeckEmptyError
from poker_rules import PokerRules
import config

logger = logging.getLogger(__name__)

class EquityCalculator:
    """
    Simula runout casuali per stimare il win% di una mano.
    Usa un PRNG privato e non tocca lo stato di random globale.
    """

    def __init__(self, trials=None, rng=None):
        self.trials = trials if trials is not None else config.EQUITY_TRIALS
        self.rules = PokerRules()
        # PRNG dedicato per simulazioni riproducibili
        self._rng = rng if rng is not None else Random()

    def _simulate_once(self, hole_cards, known_community, num_opponents):
        # 1) Mazzo pulito in ordine standard, ignorando qualunque seed globale
        deck = Deck()
        # Se Deck applica un seed iniziale, ri-creiamo il mazzo in modo standard:
        deck._load_deck_data()

        # 2) Otteniamo copia indipendente delle carte
        available = deck._deck_data.copy()

        # 3) Rimuoviamo hole e community note
        for c in hole_cards + known_community:
            try:
                available.remove(c)
            except ValueError:
                raise RuntimeError(f"Card {c} not in deck for simulation")

        # 4) Validiamo che ci siano abbastanza carte
        needed_comm = 5 - len(known_community)
        needed_total = needed_comm + 2 * num_opponents
        if len(available) < needed_total:
            raise RuntimeError("Not enough cards for simulation runout")

        # 5) Mischiamo e stacchiamo board + opp_hole
        self._rng.shuffle(available)

        # 6) Board completion
        board = known_community + available[:needed_comm]
        pos = needed_comm

        # 7) Hole cards avversari
        opp_ranks = []
        for _ in range(num_opponents):
            opp_hole = available[pos : pos + 2]
            pos += 2
            opp_ranks.append(self.rules.calculate_hand_ranking(opp_hole + board))

        # 8) Ranking nostra mano
        our_rank = self.rules.calculate_hand_ranking(hole_cards + board)

        # 9) Win/Tie decision
        win = all(our_rank > r for r in opp_ranks)
        tie = any(our_rank == r for r in opp_ranks)
        return win, tie

    def estimate_equity(self, hole_cards, known_community, num_opponents):
        """
        Esegue `self.trials` simulazioni e restituisce percentuali:
          - 'win%'  = vittorie / trials
          - 'tie%'  = pareggi / trials
          - 'lose%' = perdite / trials
        """
        wins = ties = 0
        for _ in range(self.trials):
            win, tie = self._simulate_once(
                hole_cards, known_community, num_opponents
            )
            if win:
                wins += 1
            elif tie:
                ties += 1

        total = self.trials
        return {
            'win%':  wins / total,
            'tie%':  ties / total,
            'lose%': (total - wins - ties) / total
        }