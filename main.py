import sys
import random
import unicodedata
from pprint import pprint

from config import THEME, VOWELS, DEFAULT_COLOR
from structures import Word, Color


def _is_default_color(color: Color) -> bool:
    return color.r == DEFAULT_COLOR and color.g == DEFAULT_COLOR and color.b == DEFAULT_COLOR
    
def _brightness(r: int, g: int, b: int) -> float:
    return 0.2126*r + 0.7152*g + 0.0722*b

def _random_color(brightness_min: int = 0, brightness_max: int = 255) -> Color:
    while True:
        r = random.randint(0, 255)
        g = random.randint(0, 255)
        b = random.randint(0, 255)
        if r == g == b and DEFAULT_COLOR - 30 <= r <= DEFAULT_COLOR + 30:
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


def full_normalize_word(word: str) -> str:
    normalized = unicodedata.normalize('NFD', word)
    normalized = "".join(c for c in normalized if unicodedata.category(c) != 'Mn')
    normalized = normalized.replace('đ', 'd').replace('Đ', 'D')
    return normalized

def filter_word(word: str) -> str:
    return "".join(filter(lambda c: c.isalpha(), word))

def special_execption(word: str, i: int) -> bool:
    if i-1 >=0 and full_normalize_word(word[i-1:i+1]).lower() == "ai":
        return False
    return True
    

def get_suffix(word: str) -> str:
    suffixes = set()
    for i in range(len(word)):
        if full_normalize_word(word[i]).lower() in VOWELS and special_execption(word, i):
            suffixes.add(word[i:].lower())
    return suffixes

def find_rhyme(word: Word, current_lyrics: list[list[Word]]) -> Color:
    # Search current line and upwards in the lyrics for a rhyme with the same suffix
    THRESHOLD = 3  # Minimum length of the suffix to consider it a rhyme
    n = len(current_lyrics)
    for line_number in range(n-1, max(n-THRESHOLD-1, -1), -1):
        for other in current_lyrics[line_number]:
            other: Word
            if word.rhyme(other):
                if _is_default_color(other.color):
                    other.color = new_color()

                return other.color

    return Color()

def main():
    processed_lyrics: list[list[Word]] = []

    for line_number, line in enumerate(sys.stdin):
        lines = []
        for word in line.split():
            suffix = get_suffix(filter_word(word))
            word_obj = Word(
                original=word,
                filtered=full_normalize_word(filter_word(word)),
                suffix=suffix,
                line=line_number,
            )
            word_color = find_rhyme(word_obj, processed_lyrics + [lines])
            word_obj.color = word_color

            lines.append(word_obj)

        processed_lyrics.append(lines)

    # print("\n".join(line for line in map(str,processed_lyrics)))
    for line in processed_lyrics:
        for word in line:
            print_style(word.original, word.color, end=' ')
        print()

    # pprint(processed_lyrics)
                
    

if __name__ == "__main__":
    if len(sys.argv) > 1:
        sys.stdin = open(sys.argv[1], 'r', encoding='utf-8')
    else:
        sys.stdin = open("lyrics.txt", 'r', encoding='utf-8')
        
    main()
