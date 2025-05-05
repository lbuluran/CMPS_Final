import unittest
from dataclasses import dataclass

# ----- Core Classes for Testing -----
@dataclass
class Card:
    suit: str
    rank: str

HI_LO_VALUES = {
    '2': 1, '3': 1, '4': 1, '5': 1, '6': 1,
    '7': 0, '8': 0, '9': 0,
    '10': -1, 'J': -1, 'Q': -1, 'K': -1, 'A': -1
}

class Deck:
    suits = ['Hearts', 'Diamonds', 'Clubs', 'Spades']
    ranks = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'Jack', 'Queen', 'King', 'Ace']

    def __init__(self, num_decks=1):
        self.cards = [Card(suit, rank) for _ in range(num_decks)
                      for suit in self.suits for rank in self.ranks]

    def shuffle(self):
        import random
        random.shuffle(self.cards)

    def deal_card(self):
        return self.cards.pop() if self.cards else None

class CardCounter:
    def __init__(self):
        self.running_count = 0
        self.cards_dealt = 0

    def update_count(self, card):
        value = HI_LO_VALUES.get(card.rank, 0)
        self.running_count += value
        self.cards_dealt += 1

    def true_count(self, remaining_cards):
        if remaining_cards == 0:
            return self.running_count
        return self.running_count / (remaining_cards / 52)

    def reset(self):
        self.running_count = 0
        self.cards_dealt = 0

# ----- Test Suite -----
class TestCardCounting(unittest.TestCase):

    def test_deck_initialization_and_dealing(self):
        deck = Deck(num_decks=1)
        self.assertEqual(len(deck.cards), 52, "Deck should initialize with 52 cards")
        dealt_card = deck.deal_card()
        self.assertIsInstance(dealt_card, Card, "Dealt item should be a Card")
        self.assertEqual(len(deck.cards), 51, "Deck should decrease by one after dealing")

    def test_card_counter_basic_updates(self):
        counter = CardCounter()
        counter.update_count(Card('Hearts', '2'))  # +1
        counter.update_count(Card('Spades', 'K'))  # -1
        counter.update_count(Card('Clubs', '8'))   # 0
        self.assertEqual(counter.running_count, 0, "Count should be 0 after +1, -1, 0")
        self.assertEqual(counter.cards_dealt, 3, "Should have dealt 3 cards")

    def test_true_count_logic(self):
        counter = CardCounter()
        ranks = ['2', '3', '10', 'K', '6']  # Count: +1, +1, -1, -1, +1 = +1
        for rank in ranks:
            counter.update_count(Card('Hearts', rank))
        remaining = 47  # 5 cards dealt
        expected_true = 1 / (remaining / 52)
        self.assertAlmostEqual(counter.true_count(remaining), expected_true, delta=0.001,
                               msg="True count should be correctly scaled")

    def test_counter_reset_functionality(self):
        counter = CardCounter()
        counter.update_count(Card('Diamonds', '5'))
        counter.update_count(Card('Spades', 'J'))
        counter.reset()
        self.assertEqual(counter.running_count, 0, "Reset should clear running count")
        self.assertEqual(counter.cards_dealt, 0, "Reset should clear cards dealt")

# ----- Main Entry -----
if __name__ == "__main__":
    unittest.main()

