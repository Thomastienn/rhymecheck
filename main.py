import sys
import random
import unicodedata

from config import THEME, VOWELS, DEFAULT_COLOR
from structures import Word, Color

def _brightness(r: int, g: int, b: int) -> float:
    return 0.2126*r + 0.7152*g + 0.0722*b

def _random_color(brightness_min: int = 0, brightness_max: int = 255) -> Color:
    while True:
        r = random.randint(0, 255)
        g = random.randint(0, 255)
        b = random.randint(0, 255)
        if r == g == b == DEFAULT_COLOR:
            continue
        bness = _brightness(r, g, b)
        if brightness_min <= bness <= brightness_max:
            return Color(r=r, g=g, b=b)

def print_style(text: str, color: Color, *args, **kwargs) -> None:
    print(f"{color}{text}{color.reset()}", *args, **kwargs)

def new_color() -> Color:
    if THEME == "LIGHT":
        return _random_color(brightness_max=150)
    if THEME == "DARK":
        return _random_color(brightness_min=150)
    raise ValueError(f"Unknown theme: {THEME}")


def normalize_word(word: str) -> str:
    normalized = unicodedata.normalize('NFD', word)
    normalized = "".join(c for c in normalized if unicodedata.category(c) != 'Mn')
    normalized = normalized.replace('đ', 'd').replace('Đ', 'D')
    return normalized

def filter_word(word: str) -> str:
    return "".join(filter(lambda c: c.isalpha(), word))

def get_suffix(word: str) -> str:
    for i in range(len(word)):
        if word[i].lower() in VOWELS:
            return word[i:]

def find_rhyme(suffix: str, processed_lyrics: list[list[Word]]) -> Color:
    # Search current line and upwards in the lyrics for a rhyme with the same suffix
    for line_number in range(len(processed_lyrics) - 1, -1, -1):
        for word in processed_lyrics[line_number]:
            word: Word
            if word.suffix == suffix:
                if word.color is None:
                    word.color = new_color()
                return word.color

    return Color()

def main():
    processed_lyrics: list[list[Word]] = []

    for line_number, line in enumerate(sys.stdin):
        lines = []
        for word in line.split():
            new_word = normalize_word(filter_word(word))
            if new_word:
                suffix = get_suffix(new_word)
                word_color = find_rhyme(suffix, processed_lyrics)
                lines.append(Word(
                    original=word,
                    filtered=new_word,
                    suffix=suffix,
                    line=line_number,
                    color=word_color
                ))

        processed_lyrics.append(lines)

    # print("\n".join(line for line in map(str,processed_lyrics)))
    for line in processed_lyrics:
        for word in line:
            print_style(word.original, word.color, end=' ')
        print()
                
    

if __name__ == "__main__":
    if len(sys.argv) > 1:
        sys.stdin = open(sys.argv[1], 'r', encoding='utf-8')
    else:
        sys.stdin = open("lyrics.txt", 'r', encoding='utf-8')
        
    main()
