import logging
import config

logger = logging.getLogger(__name__)


def apply_ante(players, pot_manager, game_state):
    """
    Se ANTE>0, tutti pagano ante upfront.
    Aggiorna game_state['pot'] e conserva game_state['ante'].
    """
    ante = config.ANTE
    if ante <= 0:
        game_state['ante'] = 0
        return

    for p in players:
        amt = min(p.chips, ante)
        p.bet(amt)
        pot_manager.place_bet(p, amt)
        game_state['pot'] += amt

    # registra in game_state per uso in hand history o reporting
    game_state['ante'] = ante
    logger.info("Ante of %d collected from each player", ante)


def apply_straddle(dealer_button_idx, players, pot_manager, game_state):
    """
    Se STRADDLE_ENABLED, il giocatore dopo BB può straddlare.
    Lo straddle è un blind “live”, quindi:
      - viene puntato immediatamente
      - aggiorna current_max_bet a STRADDLE_AMOUNT
    """
    if not config.STRADDLE_ENABLED:
        game_state['straddle'] = 0
        return

    sb_idx       = (dealer_button_idx + 1) % len(players)
    bb_idx       = (sb_idx + 1) % len(players)
    straddle_idx = (bb_idx + 1) % len(players)
    p            = players[straddle_idx]

    amt = min(p.chips, config.STRADDLE_AMOUNT)
    if amt <= 0:
        game_state['straddle'] = 0
        return

    # Punta lo straddle
    p.bet(amt)
    pot_manager.place_bet(p, amt)
    game_state['pot'] += amt

    # Lo straddle conta come current_max_bet pre-flop
    prev = game_state.get('current_max_bet', 0)
    game_state['current_max_bet'] = max(prev, amt)

    # Salva in game_state per hand history/report
    game_state['straddle'] = amt
    game_state['straddle_player'] = p.name

    logger.info("%s straddles %d", p.name, amt)