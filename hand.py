from collections import defaultdict

"""
In all the "detect" functions below, care is taken to return the hand from least to most important
card. This way it is easier to later compare the two best hands of two players: one first determine
which are the types of the two hands and in case the type are the same (e.g. each has two pairs), 
it is suficient to compare the cards from right to left and the first of the two hands showing a smaller
card is the loser.
"""

def suit_to_numbers_number_to_suits(hand):
    """
    The two dictionaries are convenient to compute the best hand. They are both computed by a single functionn
    for efficiency.

    >>> hand = [('D', 14), ('D', 4), ('H', 14), ('D', 8), ('D', 13), ('S', 4), ('D', 2)]

    >>> dict(suit_to_numbers_number_to_suits(hand)[0])
    {'D': [14, 4, 8, 13, 2], 'H': [14], 'S': [4]}

    >>> dict(suit_to_numbers_number_to_suits(hand)[1])
    {14: ['D', 'H'], 4: ['D', 'S'], 8: ['D'], 13: ['D'], 2: ['D']}

    """

    suit_to_numbers = defaultdict(list)
    card_to_suit = defaultdict(list)
    for suit, number in hand:
        suit_to_numbers[suit].append(number)
        card_to_suit[number].append(suit)
    return suit_to_numbers, card_to_suit


def detect_flush(suit_to_numbers, min_length=5, max_length=7):
    """
    Note that the function returns the ENTIRE set of cards of the same suit, as long as it is of length at least 5.
    It is necessary to return it all to later check for straight flushes which could happen on the flush with
    lower cards.

    >>> suit_to_numbers = {'D': [14, 4, 8, 13, 2, 12], 'H': [14], 'S': [4]}
    >>> flush = detect_flush(suit_to_numbers)
    >>> flush
    [('D', 2), ('D', 4), ('D', 8), ('D', 12), ('D', 13), ('D', 14)]


    >>> suit_to_numbers = {'D': [14, 4, 8, 13, 2, 12, 10, 3]}
    >>> flush = detect_flush(suit_to_numbers, max_length=5)
    >>> flush
    [('D', 8), ('D', 10), ('D', 12), ('D', 13), ('D', 14)]

    Note that the function does not necessarily return the flush in the common sense of the word.

    >>> len(flush)
    5

    """
    for suit, cards in suit_to_numbers.items():
        if len(cards) >= min_length:
            return [(suit, card) for card in sorted(cards)[-max_length:]]


def detect_straight(hand):
    """
    Return the longest sequence of consecutive terms of length 5 or more. Note that it can return up to
    seven cards in texas holdem. Also note that the highest straight out of those cards may not be the
    one ending in the highest value, because a lower straight flush may beat it still.
    Another caveat is that if len(hand) is L, one could get a straight of length L+1 since aces count
    both as 1 and 14.

    If no straight is detected, the function returns None.

    >>> hand = [('D', 14), ('D', 4), ('H', 14), ('D', 8), ('D', 13), ('S', 4), ('D', 2)]
    >>> detect_straight(hand)

    Otherwise the straight is returned.

    >>> hand = [('S', 3), ('S', 4), ('H', 14), ('D', 5), ('H', 6), ('S', 4), ('D', 7)]
    >>> detect_straight(hand)
    [('S', 3), ('S', 4), ('D', 5), ('H', 6), ('D', 7)]

    WARNING a straight can have more than 5 cards in this context

    >>> hand = [('S', 3), ('S', 4), ('H', 8), ('D', 5), ('H', 6), ('S', 4), ('D', 7)]
    >>> detect_straight(hand)
    [('S', 3), ('S', 4), ('D', 5), ('H', 6), ('D', 7), ('H', 8)]

    An Ace can be used as a 1 (i.e. 14 == 1)

    >>> hand = [('S', 3), ('S', 4), ('H', 2), ('D', 5), ('H', 6), ('S', 14), ('D', 7)]
    >>> detect_straight(hand)
    [('S', 1), ('H', 2), ('S', 3), ('S', 4), ('D', 5), ('H', 6), ('D', 7)]

    """
    ordered = sorted(hand, key=lambda x: x[1])

    if ordered[-1][1] == 14:
        ordered = [(ordered[-1][0], 1)] + ordered

    previous_number = ordered[0][1]
    straight = [ordered[0]]

    for card in ordered[1:]:
        if card[1] == previous_number + 1:
            straight.append(card)
        elif card[1] == previous_number:
            continue
        else:
            if len(straight) >= 5:
                return straight
            straight = [card]
        previous_number = card[1]

    if len(straight) >= 5:
        return straight


def detect_full_house(card_to_suit):
    """
    Return the best full house detected, or None

    >>> hand = [('D', 14), ('D', 4), ('H', 14), ('D', 8), ('D', 13), ('S', 4), ('D', 2)]
    >>> suit_to_numbers, card_to_suit = suit_to_numbers_number_to_suits(hand)
    >>> detect_full_house(card_to_suit)

    >>> hand = [('S', 3), ('S', 4), ('H', 3), ('D', 3), ('H', 6), ('H', 4), ('D', 7)]
    >>> suit_to_numbers, card_to_suit = suit_to_numbers_number_to_suits(hand)
    >>> detect_full_house(card_to_suit)
    [('S', 4), ('H', 4), ('S', 3), ('H', 3), ('D', 3)]

    """

    triple = []
    pair = []
    for number, suits in card_to_suit.items():
        if len(suits) == 3:
            triple.append([(suit, number) for suit in suits])
        elif len(suits) == 2:
            pair.append([(suit, number) for suit in suits])
    if len(triple) > 0 and len(pair) > 0:
        max_triple = max(triple, key=lambda x: x[0][0])
        max_pair = max(pair, key=lambda x: x[0][0])
        return max_pair + max_triple


def find_largest_others(hand, excluded, n=1):
    """
    Find the largest cards number from hand excluding those present in excluded. This is useful to complement
    a hand like a three of a kind, with the highest remaining two cards.

    >>> hand = [('D', 14), ('D', 4), ('H', 14), ('D', 8), ('D', 13)]
    >>> excluded = [('H', 14), ('D', 8), ('S', 10)]
    >>> find_largest_others(hand, excluded, n=3)
    [('D', 4), ('D', 13), ('D', 14)]

    """
    sorted_others = sorted(
        [card for card in hand if card not in excluded], key=lambda x: x[1]
    )
    return sorted_others[-n:]


def card_to_suit_to_hand(number_to_suits):
    """
    >>> hand = [('D', 14), ('D', 4), ('H', 14), ('D', 8), ('D', 13), ('S', 4), ('D', 2)]
    >>> suit_to_numbers, number_to_suits = suit_to_numbers_number_to_suits(hand)
    >>> recovered_hand = card_to_suit_to_hand(number_to_suits)
    >>> set(recovered_hand) == set(hand)
    True
    """
    hand = [(suit, card) for card, suits in number_to_suits.items() for suit in suits]
    return hand


def detect_four_of_a_kind(number_to_suits):
    """
    Return the best hand with four of a kind if four of a kind is detected. Otherwise return None.

    >>> hand = [('D', 14), ('D', 4), ('H', 2), ('S', 4), ('D', 13), ('C', 4), ('D', 2)]
    >>> suit_to_numbers, number_to_suits = suit_to_numbers_number_to_suits(hand)

    If a four of a kind is here, detect nothing

    >>> detect_four_of_a_kind(number_to_suits)

    Otherwise detect the largest single remaining card plus those 4 cards

    >>> hand = [('S', 7), ('D', 7), ('H', 7), ('C', 7), ('D', 4), ('C', 14), ('D', 2)]
    >>> suit_to_numbers, number_to_suits = suit_to_numbers_number_to_suits(hand)
    >>> detect_four_of_a_kind(number_to_suits)
    [('C', 14), ('S', 7), ('D', 7), ('H', 7), ('C', 7)]


    """

    for number, suits in number_to_suits.items():
        if len(suits) == 4:
            four_of_a_kind = [(suit, number) for suit in suits]
            hand = card_to_suit_to_hand(number_to_suits)
            highest_other_card = find_largest_others(hand, four_of_a_kind, n=1)
            best_hand = highest_other_card + four_of_a_kind
            return best_hand


def detect_three_of_a_kind(number_to_suits):
    """
    Return the best hand with three of a kind if three of a kind is detected. Otherwise return None.
    Does not work with" full house!! Will only look at the highest separate two cards to add to the three of a kind.

    >>> hand = [('D', 14), ('D', 10), ('H', 4), ('S', 4), ('D', 7), ('C', 7), ('S', 7)]
    >>> suit_to_numbers, number_to_suits = suit_to_numbers_number_to_suits(hand)
    >>> detect_three_of_a_kind(number_to_suits)
    [('D', 10), ('D', 14), ('D', 7), ('C', 7), ('S', 7)]


    >>> hand = [('D', 14), ('S', 14), ('H', 14), ('S', 4), ('D', 7), ('C', 7), ('S', 10)]
    >>> suit_to_numbers, number_to_suits = suit_to_numbers_number_to_suits(hand)
    >>> detect_three_of_a_kind(number_to_suits)
    [('C', 7), ('S', 10), ('D', 14), ('S', 14), ('H', 14)]
    """
    three_of_a_kinds = []
    for number, suits in number_to_suits.items():
        if len(suits) == 3:
            three_of_a_kinds.extend([(suit, number) for suit in suits])
    if len(three_of_a_kinds) != 0:
        sorted(three_of_a_kinds, key=lambda x: x[1])
        best_triple = three_of_a_kinds[-3:]
        hand = card_to_suit_to_hand(number_to_suits)
        highest_other_cards = find_largest_others(hand, best_triple, n=2)
        best_triple = highest_other_cards + best_triple
        return best_triple


def detect_two_pairs(number_to_suits):
    """
    Return the best hand with two pairs if two pairs are detected. Otherwise return None.

    >>> hand = [('D', 14), ('D', 4), ('H', 14), ('D', 8), ('D', 13), ('S', 4), ('D', 2)]
    >>> suit_to_numbers, number_to_suits = suit_to_numbers_number_to_suits(hand)
    >>> detect_two_pairs(number_to_suits)
    [('D', 13), ('D', 4), ('S', 4), ('D', 14), ('H', 14)]
    """

    pairs = []
    for number, suits in number_to_suits.items():
        if len(suits) == 2:
            pairs.extend([(suit, number) for suit in suits])
    if len(pairs) >= 4:
        pairs = sorted(pairs, key=lambda x: x[1])
        best_pairs = pairs[-4:]
        hand = card_to_suit_to_hand(number_to_suits)
        highest_other_card = find_largest_others(hand, best_pairs, n=1)
        best_pairs = highest_other_card + best_pairs
        return best_pairs


def detect_pair(number_to_suits):
    """
    Return the best hand with a pair detected. Otherwise return None.

    >>> hand = [('D', 14), ('D', 10), ('H', 14), ('S', 2), ('D', 11), ('C', 9), ('S', 7)]
    >>> suit_to_numbers, number_to_suits = suit_to_numbers_number_to_suits(hand)
    >>> detect_pair(number_to_suits)
    [('C', 9), ('D', 10), ('D', 11), ('D', 14), ('H', 14)]
    """

    pairs = []
    for number, suits in number_to_suits.items():
        if len(suits) == 2:
            pairs.extend([(suit, number) for suit in suits])
    if len(pairs) != 0:
        sorted(pairs, key=lambda x: x[1])
        best_pair = pairs[-2:]
        hand = card_to_suit_to_hand(number_to_suits)
        highest_other_cards = find_largest_others(hand, best_pair, n=3)
        best_pair = highest_other_cards + best_pair
        return best_pair


def detect_highest_five(hand):
    """
    >>> hand = [('D', 14), ('D', 10), ('H', 7), ('S', 4), ('D', 9), ('C', 12), ('S', 7)]
    >>> detect_highest_five(hand)
    [('S', 7), ('D', 9), ('D', 10), ('C', 12), ('D', 14)]

    """
    return find_largest_others(hand, [], n=5)


def best_five(hand):

    suit_to_numbers, number_to_suits = suit_to_numbers_number_to_suits(hand)
    flush = detect_flush(suit_to_numbers)

    # if a flush is detected
    if flush is not None:

        # the only higher hand that can occur when a flush is present is a straight flush
        straight_flush = detect_straight(flush)
        if straight_flush is not None:
            # return the last 5 best cards
            return ('straight_flush', straight_flush[-5:])
        
        return ('flush', flush)
    
    # otherwise there is no flush, we can check from highest possible hand to lowest
    else:
        # check for four of a kind
        four_of_a_kind = detect_four_of_a_kind(number_to_suits)
        if four_of_a_kind is not None:
            return ('four_of_a_kind', four_of_a_kind)
        
        # check for full house
        full_house = detect_full_house(number_to_suits)
        if full_house is not None:
            return ('full_house', full_house)
        
        # check for a straight 
        straight = detect_straight(hand)
        if straight is not None:
            return ('straight', straight)
        
        # check for three of a kind
        three_of_a_kind = detect_three_of_a_kind(number_to_suits)
        if three_of_a_kind is not None:
            return ('three_of_a_kind', three_of_a_kind)
    
        # check for two pairs
        two_pairs = detect_two_pairs(number_to_suits)
        if two_pairs is not None:
            return ('two_pairs', two_pairs)
        
        # check for one pair
        pair = detect_pair(number_to_suits)
        if pair is not None:
            return ('pair', pair)
        
        # otherwise return highest five cards
        else:
            return ('highest_cards', detect_highest_five(hand))
        
        
def is_better(best_hand_1, best_hand_2):

    """
    >>> best_hand_1 = ('full_house', [('S', 10), ('C', 10), ('D', 10), ('S', 13), ('C', 13)])
    >>> best_hand_2 = ('full_house', [('S', 10), ('C', 10), ('D', 13), ('S', 13), ('C', 13)])
    >>> is_better(best_hand_1, best_hand_2)
    -1


    >>> best_hand_1 = ('straight', [('S', 10), ('C', 11), ('D', 12), ('S', 13), ('C', 14)])
    >>> best_hand_2 = ('pair', [('S', 10), ('C', 10), ('D', 8), ('S', 11), ('C', 14)])
    >>> is_better(best_hand_1, best_hand_2)
    1

    >>> hand_1 = ('straight', [('S', 10), ('C', 11), ('D', 12), ('S', 13), ('C', 14)])
    >>> hand_2 = ('straight', [('S', 9), ('S', 10), ('C', 11), ('D', 12), ('S', 13)])
    >>> is_better(hand_1, hand_2)
    1

    >>> hand_1 = ('straight', [('S', 10), ('C', 11), ('D', 12), ('S', 13), ('C', 14)])
    >>> hand_2 = hand_1
    >>> is_better(hand_1, hand_2)
    0

    >>> hand_1 = ('highest_cards', [('S', 2), ('C', 11), ('D', 12), ('S', 13), ('C', 14)])
    >>> hand_2 = ('highest_cards', [('H', 2), ('S', 11), ('S', 12), ('S', 13), ('C', 14)])
    >>> is_better(hand_1, hand_2)
    0
    """

    ranking = {'highest_cards': 0, 'pair': 1, 'two_pairs': 2, 'three_of_a_kind': 3, 'straight': 4,
               'flush': 5, 'full_house': 6, 'four_of_a_kind': 7, 'straight_flush': 8}
    
    same_hand = best_hand_1 == best_hand_2
    if same_hand:
        return 0
    
    same_type = ranking[best_hand_1[0]] == ranking[best_hand_2[0]]
    if same_type:
        numbers_1 = [card[1] for card in best_hand_1[1]]
        numbers_2 = [card[1] for card in best_hand_2[1]]

        if numbers_1 == numbers_2:
            return 0
        else:
            win =  numbers_1[::-1] > numbers_2[::-1]

    else:
        win = ranking[best_hand_1[0]] > ranking[best_hand_2[0]]


    if win:
        return 1
    else:
        return -1
    

    

        
   

  
        


