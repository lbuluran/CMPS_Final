import unittest
from main import Deck, CardCounter, Card  # Ensure this matches your actual main filename (main.py)

class TestCardCounting(unittest.TestCase):

    def setUp(self):
        """Initialize a fresh deck and counter before each test."""
        self.deck = Deck(num_decks=1)
        self.counter = CardCounter(num_decks=1)

    def test_deck_initialization(self):
        """Test that the deck initializes with 52 cards and deals valid Card objects."""
        self.assertEqual(len(self.deck.cards), 52)
        card = self.deck.deal_card()
        self.assertIsInstance(card, Card)

    def test_deck_shuffle_changes_order(self):
        """Ensure shuffling changes the order of the deck (most of the time)."""
        deck1 = Deck()
        deck2 = Deck()
        same_order = all(
            card1.rank == card2.rank and card1.suit == card2.suit
            for card1, card2 in zip(deck1.cards, deck2.cards)
        )
        self.assertFalse(same_order, "Decks should be shuffled into different orders.")

    def test_counter_increments_and_decrements(self):
        """Test that the Hi-Lo count changes correctly with different card types."""
        low_card = Card(suit='Hearts', rank='2')  # +1
        high_card = Card(suit='Spades', rank='K')  # -1
        neutral_card = Card(suit='Clubs', rank='8')  # 0

        self.counter.update_count(low_card)
        self.assertEqual(self.counter.running_count, 1)

        self.counter.update_count(neutral_card)
        self.assertEqual(self.counter.running_count, 1)  # Still 1

        self.counter.update_count(high_card)
        self.assertEqual(self.counter.running_count, 0)

    def test_counter_reset(self):
        """Test that resetting the counter sets all values back to zero."""
        self.counter.running_count = 5
        self.counter.cards_dealt = 10
        self.counter.reset()
        self.assertEqual(self.counter.running_count, 0)
        self.assertEqual(self.counter.cards_dealt, 0)

if __name__ == "__main__":
    unittest.main()
