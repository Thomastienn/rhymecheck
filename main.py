import sys
import random
from config import THEME

def brightness(r, g, b):
    return 0.299*r + 0.587*g + 0.114*b

def random_color(brightness_min=0, brightness_max=255):
    while True:
        r = random.randint(0, 255)
        g = random.randint(0, 255)
        b = random.randint(0, 255)
        bness = brightness(r, g, b)
        if brightness_min <= bness <= brightness_max:
            return (r, g, b)

def new_color():
    # or "DARK" if wanna use dark themej
    if THEME == "LIGHT":
        return random_color(brightness_max=50)

    return random_color(brightness_min=150)

def print_style(text, r, g, b, *args, **kwargs):
    print(f"\033[4;38;2;{r};{g};{b}m{text}\033[0m", *args, **kwargs)

for line in sys.stdin:
    line = line.strip()
    if not line:
        continue

    for word in line.split():
        new_color = random_color()
        print_style(word, *new_color, end=' ')
    print()  # Print a newline after each line of input
