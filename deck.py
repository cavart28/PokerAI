from itertools import product
from functools import cached_property
import numpy as np

suits = ['S', 'H', 'D', 'C']
faces = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A']
faces_values = [i for i in range(2, 15)]


class ShuffledDeck:
    def __init__(self):
        self.deck = list(product(suits, faces_values))
        np.random.shuffle(self.deck)

    def deal(self, n):
        return [self.deck.pop() for i in range(n)]
    
    def __len__(self):
        return len(self.deck)
    

class Round():
    def __init__(self, n_players):
        self.n_players = n_players
        self.shuffled_deck = ShuffledDeck()
        self.flop_ = False
        self.turn_ = False
        self.river_ = False
    
    @cached_property
    def dealt_hands(self):
        return [self.shuffled_deck.deal(2) for i in range(self.n_players)]
    
    @cached_property
    def flop(self):
        self.flop_ = True
        return self.shuffled_deck.deal(3)
    
    @cached_property
    def turn(self):
        assert self.flop_, "The flop has not yet been dealt"
        self.turn_ = True
        return self.shuffled_deck.deal(1)
    
    @cached_property
    def river(self):
        assert self.turn_, "The turn has not yet been dealt"
        self.river_ = True
        return self.shuffled_deck.deal(1)
    
    @cached_property
    def deck_copy(self):
        return self.shuffled_deck.deck.copy()
    
    def simulate_end(self, n):
        np.random.shuffle(self.deck_copy)
        return self.deck_copy[:n]


class NaiveRoundEndSim():
    """It is assumed that we are player 1 and we do not know the other players' hands."""
    def __init__(self, round):
        self.round = round
        self.n_players = self.round.n_players
        self.hand = self.round

    def simulate(self, n):
        pass

