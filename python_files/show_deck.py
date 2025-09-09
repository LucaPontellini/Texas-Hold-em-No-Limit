import pygame
import json
from pathlib import Path

# 1. Imposta i path base
BASE_DIR   = Path(__file__).parent            # .../Texas-Hold-em-No-Limit/python_files
PROJECT    = BASE_DIR.parent                  # .../Texas-Hold-em-No-Limit
STATIC_DIR = PROJECT / "static"               # .../Texas-Hold-em-No-Limit/static
DECK_FILE  = BASE_DIR / "deck.json"           # .../Texas-Hold-em-No-Limit/python_files/deck.json

# 2. Carica deck.json
def load_deck():
    with open(DECK_FILE, "r") as f:
        data = json.load(f)
    return data["cards"], data["back"]

def main():
    pygame.init()
    cards, back = load_deck()

    # 3. Ordina per semi (cuori, quadri, fiori, picche)
    SUITS = ["hearts", "diamonds", "clubs", "spades"]
    ordered = []
    for suit in SUITS:
        ordered += [c for c in cards if c["seed"].lower() == suit]

    # 4. Carica le immagini
    face_images = [
        pygame.image.load(str(STATIC_DIR / c["img"]))
        for c in ordered
    ]
    back_image = pygame.image.load(str(STATIC_DIR / back))

    cols, rows = 13, 4

    # 5. Scala per adattarsi allo schermo
    info      = pygame.display.Info()
    max_w     = info.current_w * 0.8
    max_h     = info.current_h * 0.8
    orig_w, orig_h = face_images[0].get_size()
    total_w   = orig_w * cols
    total_h   = orig_h * (rows + 1)
    scale     = min(max_w/total_w, max_h/total_h, 1.0)

    new_w = int(orig_w * scale)
    new_h = int(orig_h * scale)

    face_images = [
        pygame.transform.smoothscale(img, (new_w, new_h))
        for img in face_images
    ]
    back_image = pygame.transform.smoothscale(back_image, (new_w, new_h))

    # 6. Crea finestra Pygame
    screen = pygame.display.set_mode((new_w * cols, new_h * (rows + 1)))
    pygame.display.set_caption("Deck Texas Hold'em")

    # 7. Loop principale
    running = True
    while running:
        for evt in pygame.event.get():
            if evt.type == pygame.QUIT:
                running = False

        screen.fill((0, 128, 0))
        for i, img in enumerate(face_images):
            row = i // cols
            col = i % cols
            screen.blit(img, (col * new_w, row * new_h))

        # dorso centrato sulla quinta riga
        back_x = (cols * new_w - new_w) // 2
        back_y = rows * new_h
        screen.blit(back_image, (back_x, back_y))

        pygame.display.flip()

    pygame.quit()

if __name__ == "__main__":
    main()