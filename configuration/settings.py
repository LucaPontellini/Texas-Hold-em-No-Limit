from .general import GENERAL
from .player import PLAYER_SETTINGS
from .table import TABLE_SETTINGS
from .chip import CHIP_SETTINGS, TABLE_CHIP_SETS, get_chips_for_blinds
from .deck import DECK_SETTINGS
from .blinds import BLINDS_ANTE_SETTINGS
from .straddle import STRADDLE_SETTINGS
from .betting import BETTING_RULES, ACTIONS_SETTINGS
from .rake import RAKE_SETTINGS
from .time_bank import TIME_BANK_SETTINGS
from .anti_collusion import ANTI_COLLUSION_SETTINGS
from .jackpot import JACKPOT_SETTINGS
from .hud_stats import HUD_STATS_SETTINGS
from .ui import UI_SETTINGS
from .banking import BANKING_SETTINGS
from .session import SESSION_SETTINGS
from .gamification import GAMIFICATION_SETTINGS
from .bot import BOT_SETTINGS, BOT_INTELLIGENCE_SETTINGS, get_bot_intelligence
from .rng import RNG_SETTINGS
from .logging import LOGGING_SETTINGS

def as_dict():
    return {
        "GENERAL":           GENERAL,
        "PLAYER_SETTINGS":   PLAYER_SETTINGS,
        "TABLE_SETTINGS":    TABLE_SETTINGS,
        "CHIP_SETTINGS":     CHIP_SETTINGS,
        "TABLE_CHIP_SETS":   TABLE_CHIP_SETS,
        "DECK_SETTINGS":     DECK_SETTINGS,
        "BLINDS_ANTE":       BLINDS_ANTE_SETTINGS,
        "STRADDLE":          STRADDLE_SETTINGS,
        "BETTING_RULES":     BETTING_RULES,
        "ACTIONS":           ACTIONS_SETTINGS,
        "RAKE_SETTINGS":     RAKE_SETTINGS,
        "TIME_BANK":         TIME_BANK_SETTINGS,
        "ANTI_COLLUSION":    ANTI_COLLUSION_SETTINGS,
        "JACKPOT":           JACKPOT_SETTINGS,
        "HUD_STATS":         HUD_STATS_SETTINGS,
        "UI":                UI_SETTINGS,
        "BANKING":           BANKING_SETTINGS,
        "SESSION":           SESSION_SETTINGS,
        "GAMIFICATION":      GAMIFICATION_SETTINGS,
        "BOT_SETTINGS":      BOT_SETTINGS,
        "BOT_INTELLIGENCE":  BOT_INTELLIGENCE_SETTINGS,
        "RNG_SETTINGS":      RNG_SETTINGS,
        "LOGGING_SETTINGS":  LOGGING_SETTINGS
    }