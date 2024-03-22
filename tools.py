from dataclasses import dataclass, field
from random import shuffle

from enum import Enum

class Suit(Enum):
    HEART = "HEART"
    DIAMOND = "DIAMOND"
    CLUB = "CLUB"
    SPADE = "SPADE"

class Rank(Enum):
    ACE = "A"
    TWO = "2"
    THREE = 3
    FOUR = 4
    FIVE = 5
    SIX = 6
    SEVEN = 7
    EIGHT = 8
    NINE = 9
    TEN = 10
    JACK = "J"
    QUEEN = "Q"
    KING = "K"

@dataclass
class Card:
    suit: Suit
    rank: Rank

@dataclass
class Deck:
    cards: list[Card] = field(default_factory=list)

    def initialize(self) -> None:
        self.cards = [Card(suit, rank) for suit in Suit for rank in Rank]

    def shuffle(self) -> None:
        shuffle(self.cards)

    def size(self) -> int:
        return len(self.cards)

def main():
    deck = Deck()
    deck.initialize()
    deck.shuffle()
    print(deck.cards)

if __name__ == "__main__":
    main()