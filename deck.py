from itertools import product
from functools import cached_property
from collections import Counter, defaultdict
import numpy as np
from PokerAI.hand import best_five, is_better

suits = ['S', 'H', 'D', 'C']
faces = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A']
faces_values = [i for i in range(2, 15)]

def my_hand_wins(results):
    if -1 in results:
        return -1
    elif np.sum(results) == 0:
        return 0
    else:
        return 1


def get_raw_proba_of_winning(my_hand, n_players, n_runs=100):
    loss_draw_win = []
    round = Round(n_players=n_players)
    for i in range(n_runs):
        round = Round(n_players=n_players)
        best_hands, results = round.simulate_blindly(my_hand=my_hand)
        loss_draw_win.append(my_hand_wins(results))
    c = Counter(loss_draw_win)
    p = {k: v / n_runs for k, v in c.items()}
    return defaultdict(int, p)


class ShuffledDeck:
    def __init__(self, exclude=None):
        self.deck = list(product(suits, faces_values))

        if exclude is not None:
            self.deck = [card for card in self.deck if card not in exclude]

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
    
    def simulate_blindly(self, my_hand=None):
        """
        Generate possible outcome for the hand you were dealt. Other players hand are re-dealt since we 
        have no way to know which they are at any point
        """
        if my_hand is None:
            my_hand = self.dealt_hands[0]
        
        sd = ShuffledDeck(exclude=my_hand)

        other_hands = [sd.deal(2) for i in range(self.n_players - 1)]
        common_cards = sd.deal(5)

        own_best_five_hand = best_five(my_hand + common_cards)
        others_best_hand = [best_five(hand + common_cards) for hand in other_hands]

        win = []
        for hand in others_best_hand:
            win.append(is_better(own_best_five_hand, hand))
        
        return ([own_best_five_hand] + others_best_hand, win)
    






        


