#!/usr/bin/env python3
import json
from pathlib import Path

# Ordine ufficiale dei semi nei casino (Texas Hold’em):
SUITS       = ["hearts", "diamonds", "clubs", "spades"]
BASE_DIR    = Path(__file__).parent.parent / "static" / "card_images"
OUTPUT_FILE = Path(__file__).parent / "deck.json"

def build_deck():
    cards = []
    face_map = {"01":"A", "11":"J", "12":"Q", "13":"K"}

    for suit in SUITS:
        suit_dir = BASE_DIR / suit
        for img in sorted(suit_dir.glob("*.png")):
            idx = img.stem.split("_")[0]            # es. "02"
            value = face_map.get(idx, str(int(idx)))
            cards.append({
                "value": value,
                "seed":  suit.capitalize(),
                "img":   f"card_images/{suit}/{img.name}"
            })

    back_file = BASE_DIR / "card_back.jpg"
    back_path = f"card_images/{back_file.name}" if back_file.exists() else ""
    return {"cards": cards, "back": back_path}

def main():
    deck_data = build_deck()
    with open(OUTPUT_FILE, "w") as f:
        json.dump(deck_data, f, indent=2)
    print(f"Generato {len(deck_data['cards'])} carte + retro in → {OUTPUT_FILE}")

if __name__ == "__main__":
    main()