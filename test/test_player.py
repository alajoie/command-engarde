import unittest
from src.player import Player
from src.card import Card

class TestNewPlayer(unittest.TestCase):
    def setUp(self):
        self.player = Player("T")
    def test_token_initialized(self):
        self.assertEqual(self.player.token, "T")
    def test_str_is_token(self):
        self.assertEqual(str(self.player), self.player.token)
    def test_player_initializes_at_position_zero(self):
        self.assertEqual(self.player.position, 0)
    def test_player_initializes_with_no_space_to_retreat(self):
        self.assertEqual(self.player.range_to_end,0)
    def test_player_initializes_with_no_hits_against(self):
        self.assertEqual(self.player.hits, 0)
    def test_player_hand_starts_empty(self):
        hand = self.player.hand
        self.assertEqual(len(hand), 0)

class TestPlayerAdvances(unittest.TestCase):
    def setUp(self):
        self.player = Player("P")
    def test_player_advancing_from_left_increase_position(self):
        self.player.side = "L"
        self.player.advance(3)
        self.assertEqual(self.player.position, 3)
    def test_player_advancing_from_right_decreases_position(self):
        self.player.side = "R"
        self.player.advance(3)
        self.assertEqual(self.player.position, -3)

class TestPlayerRetreats(unittest.TestCase):
    def setUp(self):
        self.player = Player("P")
    def test_player_retreating_from_left_decreases_position(self):
        self.player.side = "L"
        self.player.retreat(2)
        self.assertEqual(self.player.position, -2)
    def test_playet_retreating_from_right_increases_position(self):
        self.player.side = "R"
        self.player.retreat(2)
        self.assertEqual(self.player.position, 2)

class TestPlayerGetsHit(unittest.TestCase):
    def setUp(self):
        self.player = Player("P")
    def test_player_gets_hit_increases_hits_against(self):
        self.player.hit()
        self.assertEqual(self.player.hits, 1)

