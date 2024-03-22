from typing import Protocol
from dataclasses import dataclass, field
import uuid
import random

from tools import Card, Deck


@dataclass
class HandCard:
    cards: list[Card] = field(default_factory=list)

    def add_card(self, card: Card):
        self.cards.append(card)

    def remove_card(self, card: Card):
        self.cards.remove(card)

    @property
    def size(self) -> int:
        return len(self.cards)
    
@dataclass
class Player(Protocol):
    name: str
    hand_card: HandCard
    show_on_table: Card
    point: int    

    def name_self(self):
        ...

    def draw_card(self):
        ...

    def exchange_card(self):
        ...

    def show_card(self):
        ...
   
@dataclass
class CommandLineInterface:
    
    def choose_exchange_player(self, exchanger: Player, players: list[Player]) -> int | None:       
        while True:
            is_exchange = input("Do you want to exchange cards with other players? please input yes or no.")
            if is_exchange.lower() == "yes":

                can_exchange_list_index = []

                print("Choose a player to exchange cards with:")
                for i, player in enumerate(players):
                    if player != exchanger:
                        print(f"{i + 1}: {player.name}")
                        can_exchange_list_index.append(i + 1)
                while True:
                    try:
                        index = int(input("Please input the number of the player you want to exchange cards with: "))
                        if index not in can_exchange_list_index:
                            print(f"You have to choose a number in {can_exchange_list_index}.")
                            continue
                        return index - 1
                    except ValueError:
                        print(f"You have to choose a number in {can_exchange_list_index}.")
            elif is_exchange.lower() == "no":
                return
            else:
                print("Please input yes or no.")


    def show_card(self, hand_card: HandCard) -> Card:
        print("Your hand cards are:")
        for index, card in enumerate(hand_card.cards):
            print(f"{index + 1}: {card.rank.value} of {card.suit.value}")
        
        while True:
            try:
                i = int(input("Please input the number of the card you want to show: "))
                if not 1 <= i <= hand_card.size:
                    raise ValueError
                card = hand_card.cards[i - 1]
                hand_card.remove_card(card)
                return card
            except ValueError:
                print(f"Please input a number between 1 and {hand_card.size}.")

@dataclass
class HumanPlayer:
    name: str = None
    hand_card: HandCard = field(default_factory=HandCard)
    show_on_table: Card = None
    point: int = field(default=0)
    exchange_remain_count: int = field(default=1)
    command: CommandLineInterface = field(default_factory=CommandLineInterface)

    def name_self(self, name: str) -> None:
        self.name = name

    def draw_card(self, deck: Deck) -> None:
        if deck.size == 0:
            raise ValueError("The deck is empty.")
        self.hand_card.add_card(deck.cards.pop())        

    def exchange_card(self, players: list[Player]) -> int | None:
        if self.exchange_remain_count <= 0:
            return
        index = self.command.choose_exchange_player(self, players)
        if index is None:
            return
        self.hand_card, players[index].hand_card = players[index].hand_card, self.hand_card
        self.exchange_remain_count -= 1
        return index                
            
    def show_card(self) -> None:
        if self.hand_card.size == 0:
            return
        self.show_on_table = self.command.show_card(self.hand_card)
        
@dataclass
class AIPlayer:
    name: str = f"AI-{uuid.uuid4()}"
    hand_card: HandCard = field(default_factory=HandCard)
    show_on_table: Card = None
    point: int = field(default=0)

    def name_self(self):
        pass

    def draw_card(self, deck: Deck) -> None:
        self.hand_card.add_card(deck.cards.pop())

    def exchange_card(self, players: list[Player]) -> None:
        pass

    def show_card(self) -> None:
        if self.hand_card.size == 0:
            return
        card = random.choice(self.hand_card.cards)
        self.hand_card.remove_card(card)
        self.show_on_table = card

        