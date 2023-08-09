from PokerAI.hand import (
    detect_flush,
    detect_full_house,
    detect_two_pairs,
    detect_three_of_a_kind,
    detect_four_of_a_kind,
    detect_highest_five,
    detect_pair,
    detect_straight,
    suit_to_numbers_number_to_suits,
    best_five
)

from PokerAI.deck import ShuffledDeck
from PokerAI.plot import plot_hand
import pickle
import os


test_set = {
    ("flush", "pair", "two_pairs"): [
        ("D", 14),
        ("D", 4),
        ("H", 14),
        ("D", 8),
        ("D", 13),
        ("S", 4),
        ("D", 2),
    ],
    ("straight", "pair"): [
        ("D", 5),
        ("D", 8),
        ("H", 6),
        ("D", 5),
        ("S", 3),
        ("S", 4),
        ("D", 2),
    ],
    ("straight", "pair", "flush"): [
        ("D", 14),
        ("D", 2),
        ("H", 3),
        ("D", 4),
        ("S", 4),
        ("D", 2),
        ("D", 5),
    ],
    ("flush", "straight"): [
        ("D", 9),
        ("D", 10),
        ("H", 14),
        ("D", 8),
        ("D", 11),
        ("S", 4),
        ("D", 12),
    ],
    ("triple", "pair", "full_house"): [
        ("D", 14),
        ("S", 14),
        ("H", 3),
        ("D", 4),
        ("S", 4),
        ("H", 14),
        ("C", 5),
    ],
    (None,): [("D", 9), ("D", 10), ("H", 14), ("D", 2), ("S", 11), ("S", 4), ("D", 12)],
}


def test_hand_val_functions(test_set):
    for name, hand in test_set.items():
        suit_to_numbers, number_to_suits = suit_to_numbers_number_to_suits(hand)
        if "flush" in set(name):
            assert detect_flush(suit_to_numbers) is not None
        if "straight" in set(name):
            assert detect_straight(hand) is not None
        if "two_pairs" in set(name):
            assert detect_two_pairs(number_to_suits) is not None
        if "full_house" in set(name):
            assert detect_full_house(number_to_suits) is not None
        if None in set(name):
            assert detect_straight(hand) is None
            for func in [detect_flush, detect_two_pairs, detect_full_house]:
                assert func(number_to_suits) is None


test_hand_val_functions(test_set=test_set)


def pickle_dump(obj, path):
    """
    Dump a pickle
    """
    with open(path, 'wb') as outfile:
        return pickle.dump(obj, outfile)


def pickle_load(path):
    """
    Load a pickle
    """
    with open(path, 'rb') as pickle_in:
        return pickle.load(pickle_in)


# little class to test quickly best_five and also record what is deemed correct for later testing 
test_set = [] 
dir_path = os.path.dirname(os.path.realpath(__file__))
filename = 'test_hand.pkl'
test_file_loc = os.path.join(dir_path, filename)

class TestBestFive():
    def __init__(self, test_set=None):
        try:
            self.load_test_set()
        except:
            self.test_set = []

    def generate_random_full_hand(self):
        sd = ShuffledDeck()
        self.hand = sd.deal(7)
        self.computed_best_five =  best_five(self.hand)
        plot_hand(self.hand)
        print(self.computed_best_five[0])
        plot_hand(self.computed_best_five[1])
        self.test_set.append((self.hand, self.computed_best_five))

    def test_hand(self, hand):
        self.computed_best_five =  best_five(hand)
        plot_hand(self.hand)
        print(self.computed_best_five[0])
        plot_hand(self.computed_best_five[1])
        self.test_set.append((hand, self.computed_best_five))

    def remove_last(self):
        self.test_set.pop()

    def save_test_set(self):
        pickle_dump(self.test_set, test_file_loc)

    def load_test_set(self):
        self.test_set = pickle_load(test_file_loc)

    def extend_test_set(self):
        pickle_dump(self.test_set, test_file_loc)

    def run_test(self):
        for (hand, result) in self.test_set:
            assert best_five(hand) == result, f"Hand {hand} wasn't correctly predicted"


def test_best_five():
    tbf = TestBestFive()
    tbf.load_test_set()
    tbf.run_test()

test_best_five()

