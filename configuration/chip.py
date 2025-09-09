CHIP_SETTINGS = {
    "all_denominations": [1, 5, 25, 100, 500, 1000, 5000, 10000, 25000, 50000],
    "colors": {
        1:     "white",
        5:     "red",
        25:    "green",
        100:   "black",
        500:   "purple",
        1000:  "orange",
        5000:  "blue",
        10000: "yellow",
        25000: "gray",
        50000: "pink"
    },
    "security_features": {
        "RFID":           True,
        "UV_markings":    True,
        "unique_chip_id": True
    }
}

TABLE_CHIP_SETS = {
    "1/2":     [1, 5, 25, 100, 500],
    "2/5":     [5, 25, 100, 500, 1000],
    "5/10":    [25, 100, 500, 1000, 5000],
    "10/20":   [100, 500, 1000, 5000, 10000],
    "25/50+":  [500, 1000, 5000, 10000, 25000, 50000]
}

def get_chips_for_blinds(level: str):
    return TABLE_CHIP_SETS.get(level, CHIP_SETTINGS["all_denominations"])