from dataclasses import dataclass, field
from typing import Callable
from pprint import pprint

from tools import Deck
from user import Player, HumanPlayer, AIPlayer


@dataclass
class ExchangeRecord:
    record: list = field(default_factory=list)
    players: Callable = field(default_factory=list)

    def initialize(self):
        self.record = []

    def check(self, turns: int):
        if len(self.record) == 0:
            return
        for i in range(len(self.record) - 1, -1, -1):
            if self.record[i]["turns"] + 3 == turns:
                self.exchange_back(self.record[i]["index"], self.record[i]["exchangee_index"])
                self.record.pop(i)

    def add_record(self, index, exchangee_index, current_turn):
        self.record.insert(0, {
            "index": index, 
            "exchangee_index": exchangee_index, 
            "turns": current_turn
        })

    def exchange_back(self, index: int, exchangee_index: int):
        players: list[Player] = self.players()
        players[index].hand_card, players[exchangee_index].hand_card = players[exchangee_index].hand_card, players[index].hand_card
        print(f"""
        -----------------------------------------------------------------------------  
        | Exchange back between {players[index].name} and {players[exchangee_index].name}. |
        -----------------------------------------------------------------------------
        """)    

@dataclass
class PokerGame:
    players: list[Player] = field(default_factory=list)
    deck: Deck = field(default_factory=Deck)
    current_turn: int = field(default=1)
    exchange_record: ExchangeRecord = field(default_factory=ExchangeRecord)

    def __post_init__(self):
        self.exchange_record.players = self.__callback_players

    def initialize(self):
        self.deck.initialize()
        self.deck.shuffle()
        self.exchange_record.initialize()

    def add_player(self, player: Player):
        if len(self.players) < 4:
            self.players.append(player)
            self.start()
        else:
            print("The game is full, you can't add more players.")

    def start(self):
        if len(self.players) == 4:
            self.__draw_card()
            while self.current_turn <= 13:
                self.check_exchange_record()
                self.take_next_turn()
            self.announce_winner()

    def __draw_card(self):
        while self.deck.size() > 0:
            for player in self.players:
                if player.hand_card.size < 13:
                    player.draw_card(self.deck)

    def take_next_turn(self):
        print("================================================================================")
        print(f"Begins turn {self.current_turn}.")       
        for index, player in enumerate(self.players):
            exchangee_index = player.exchange_card(self.players)
            if exchangee_index is not None:
                self.exchange_record.add_record(index, exchangee_index, self.current_turn)
            player.show_card()
        self.count_score()
        self.current_turn += 1

    def check_exchange_record(self):
        self.exchange_record.check(self.current_turn)

    def count_score(self):
        rank_values = {'2': 2, '3': 3, '4': 4, '5': 5, '6': 6, '7': 7, '8': 8, '9': 9, '10': 10, 'J': 11, 'Q': 12, 'K': 13, 'A': 14}
        suit_values = {'CLUB': 1, 'DIAMOND': 2, 'HEART': 3, 'SPADE': 4}

        winner = None
        highest_socre = -1

        for player in self.players:
            score = rank_values[f"{player.show_on_table.rank.value}"] * 10 + suit_values[player.show_on_table.suit.value]
            if score > highest_socre:
                highest_socre = score
                winner = player

        winner.point += 1

        pprint(f"Turns {self.current_turn} winner is {winner.name} with {winner.show_on_table.rank.value} of {winner.show_on_table.suit.value}.")
        for player in self.players:
            pprint(f"{player.name} has {player.point} points.")

    def announce_winner(self):
        winner = None
        highest_point = -1
        for player in self.players:
            if player.point > highest_point:
                highest_point = player.point
                winner = player
        print(f"""
        -----------------------------------------------------------------
            The winner is {winner.name} with {winner.point} points.
        -----------------------------------------------------------------
        """)

    def __callback_players(self):
        return self.players

def main():
    poker_game = PokerGame()
    poker_game.initialize()

    herman = HumanPlayer()
    herman.name_self("Herman")

    ai_01 = AIPlayer()
    ai_02 = AIPlayer()
    ai_03 = AIPlayer()

    
    poker_game.add_player(ai_01)
    poker_game.add_player(ai_02)
    poker_game.add_player(herman)
    poker_game.add_player(ai_03)



if __name__ == "__main__":
    main()