from hand import (
    detect_flush,
    detect_full_house,
    detect_two_pairs,
    detect_three_of_a_kind,
    detect_four_of_a_kind,
    detect_highest_five,
    detect_pair,
    detect_straight,
    suit_to_cards_card_to_suits
)

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
        suit_to_cards, card_to_suits = suit_to_cards_card_to_suits(hand)
        if "flush" in set(name):
            assert detect_flush(suit_to_cards) is not None
        if "straight" in set(name):
            assert detect_straight(hand) is not None
        if "two_pairs" in set(name):
            assert detect_two_pairs(card_to_suits) is not None
        if "full_house" in set(name):
            assert detect_full_house(card_to_suits) is not None
        if None in set(name):
            assert detect_straight(hand) is None
            for func in [detect_flush, detect_two_pairs, detect_full_house]:
                assert func(card_to_suits) is None


test_hand_val_functions(test_set=test_set)
