from collections import Counter
from enum import Enum, auto

class PokerHand(Enum):
    HIGH_CARD = auto()
    PAIR = auto()
    TWO_PAIR = auto()
    THREE_OF_A_KIND = auto()
    STRAIGHT = auto()
    FLUSH = auto()
    FULL_HOUSE = auto()
    FOUR_OF_A_KIND = auto()
    STRAIGHT_FLUSH = auto()
    ROYAL_FLUSH = auto()

def evaluate_hand(cards):
    """
    Evaluate a poker hand and return a tuple of (hand_type, high_cards)
    where high_cards is a list of values used for breaking ties.
    """
    if not cards or len(cards) != 5:
        return (PokerHand.HIGH_CARD, [])
    
    # Sort cards by value
    values = sorted([card[0] for card in cards], reverse=True)
    suits = [card[1] for card in cards]
    
    # Check for flush
    is_flush = len(set(suits)) == 1
    
    # Check for straight
    is_straight = False
    poker_values = {
        "2": 2,
        "3": 3,
        "4": 4,
        "5": 5,
        "6": 6,
        "7": 7,
        "8": 8,
        "9": 9,
        "10": 10,
        "J": 11,
        "Q": 12,
        "K": 13,
        "A": 14
    }

    straight_values = [poker_values[v] for v in values]
    if len(set(straight_values)) == 5:
        if max(straight_values) - min(straight_values) == 4:
            is_straight = True
        # Check for Ace-low straight (A,2,3,4,5)
        elif straight_values == [14, 5, 4, 3, 2]:
            is_straight = True
            values = [5, 4, 3, 2, 1]  # Ace counts as low
    
    # Straight flush and royal flush
    if is_straight and is_flush:
        if values[0] == 14:
            return (PokerHand.ROYAL_FLUSH, values)
        return (PokerHand.STRAIGHT_FLUSH, values)
    
    # Count frequencies of values
    value_counts = Counter(values)
    counts = sorted(value_counts.values(), reverse=True)
    
    # Four of a kind
    if counts == [4, 1]:
        four_value = [v for v, c in value_counts.items() if c == 4][0]
        kicker = [v for v, c in value_counts.items() if c == 1][0]
        return (PokerHand.FOUR_OF_A_KIND, [four_value, kicker])
    
    # Full house
    if counts == [3, 2]:
        three_value = [v for v, c in value_counts.items() if c == 3][0]
        two_value = [v for v, c in value_counts.items() if c == 2][0]
        return (PokerHand.FULL_HOUSE, [three_value, two_value])
    
    # Flush
    if is_flush:
        return (PokerHand.FLUSH, values)
    
    # Straight
    if is_straight:
        return (PokerHand.STRAIGHT, values)
    
    # Three of a kind
    if counts == [3, 1, 1]:
        three_value = [v for v, c in value_counts.items() if c == 3][0]
        kickers = sorted([v for v, c in value_counts.items() if c == 1], reverse=True)
        return (PokerHand.THREE_OF_A_KIND, [three_value] + kickers)
    
    # Two pair
    if counts == [2, 2, 1]:
        pairs = sorted([v for v, c in value_counts.items() if c == 2], reverse=True)
        kicker = [v for v, c in value_counts.items() if c == 1][0]
        return (PokerHand.TWO_PAIR, pairs + [kicker])
    
    # Pair
    if counts == [2, 1, 1, 1]:
        pair_value = [v for v, c in value_counts.items() if c == 2][0]
        kickers = sorted([v for v, c in value_counts.items() if c == 1], reverse=True)
        return (PokerHand.PAIR, [pair_value] + kickers)
    
    # High card
    return (PokerHand.HIGH_CARD, values)

def compare_hands(hand1_cards, hand2_cards):
    """
    Compare two poker hands and return:
    1 if hand1 wins
    -1 if hand2 wins
    0 if tie
    """
    hand1 = evaluate_hand(hand1_cards)
    hand2 = evaluate_hand(hand2_cards)
    
    # Compare hand types
    if hand1[0].value > hand2[0].value:
        return 1
    if hand1[0].value < hand2[0].value:
        return -1
        
    # If hand types are equal, compare high cards
    for card1, card2 in zip(hand1[1], hand2[1]):
        if card1 > card2:
            return 1
        if card1 < card2:
            return -1
    
    return 0  # Tie