import unittest
from src.card import Card

class TestCard(unittest.TestCase):
    def setUp(self):
        self.card = Card(1)
    def test_1(self):
        self.assertTrue(True)
    def test_card_value(self):
        self.assertEqual(self.card.value, 1)


if __name__ == '__main__':
    unittest.main()
