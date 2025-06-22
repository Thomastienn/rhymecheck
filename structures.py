from config import DEFAULT_COLOR

from pydantic import BaseModel

class Color(BaseModel):
    r: int = DEFAULT_COLOR
    g: int = DEFAULT_COLOR
    b: int = DEFAULT_COLOR

    def __str__(self) -> str:
        underline = "" if (self.r == self.g == self.b == DEFAULT_COLOR) else "4"
        return f"\033[{underline};38;2;{self.r};{self.g};{self.b}m"
    
    def __hash__(self) -> int:
        return hash((self.r, self.g, self.b))

    def reset(self) -> str:
        return "\033[0m"

class Word(BaseModel):
    original: str
    filtered: str
    suffix: str
    line: int
    color: Color | None = None

