#!/usr/bin/env python3
"""
Simple test file for the 2D game components
"""

import unittest
from unittest.mock import Mock, patch
import pygame
import sys
import os

# Add the current directory to the path so we can import game
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
dasdasdas ds 
# Mock pygame for testing
pygame.init = Mock()
pygame.display = Mock()
pygame.time = Mock()
pygame.font = Mock()
pygame.event = Mock()
pygame.key = Mock()
pygame.draw = Mock()
pygame.Rect = Mock()

class TestGameComponents(unittest.TestCase):
    
    def setUp(self):
        """Set up test fixtures"""
        # Mock pygame components
        self.mock_screen = Mock()
        self.mock_clock = Mock()
        self.mock_font = Mock()
        
        pygame.display.set_mode.return_value = self.mock_screen
        pygame.time.Clock.return_value = self.mock_clock
        pygame.font.Font.return_value = self.mock_font
        
    def test_player_initialization(self):
        """Test that player initializes correctly"""
        try:
            from game import Player
            player = Player(100, 200)
            
            self.assertEqual(player.x, 100)
            self.assertEqual(player.y, 200)
            self.assertEqual(player.width, 30)  # PLAYER_SIZE
            self.assertEqual(player.height, 30)
            self.assertEqual(player.vel_x, 0)
            self.assertEqual(player.vel_y, 0)
            self.assertFalse(player.on_ground)
            
        except ImportError as e:
            self.skipTest(f"Could not import game module: {e}")
            
    def test_collectible_initialization(self):
        """Test that collectible initializes correctly"""
        try:
            from game import Collectible
            collectible = Collectible(150, 250)
            
            self.assertEqual(collectible.x, 150)
            self.assertEqual(collectible.y, 250)
            self.assertEqual(collectible.width, 20)  # COLLECTIBLE_SIZE
            self.assertEqual(collectible.height, 20)
            self.assertFalse(collectible.collected)
            self.assertEqual(collectible.animation_offset, 0)
            
        except ImportError as e:
            self.skipTest(f"Could not import game module: {e}")
            
    def test_obstacle_initialization(self):
        """Test that obstacle initializes correctly"""
        try:
            from game import Obstacle
            obstacle = Obstacle(200, 300, 50, 60)
            
            self.assertEqual(obstacle.x, 200)
            self.assertEqual(obstacle.y, 300)
            self.assertEqual(obstacle.width, 50)
            self.assertEqual(obstacle.height, 60)
            
        except ImportError as e:
            self.skipTest(f"Could not import game module: {e}")
            
    def test_game_constants(self):
        """Test that game constants are defined correctly"""
        try:
            from game import SCREEN_WIDTH, SCREEN_HEIGHT, FPS
            from game import PLAYER_SIZE, PLAYER_SPEED, PLAYER_JUMP_POWER
            
            self.assertEqual(SCREEN_WIDTH, 800)
            self.assertEqual(SCREEN_HEIGHT, 600)
            self.assertEqual(FPS, 60)
            self.assertEqual(PLAYER_SIZE, 30)
            self.assertEqual(PLAYER_SPEED, 5)
            self.assertEqual(PLAYER_JUMP_POWER, 15)
            
        except ImportError as e:
            self.skipTest(f"Could not import game module: {e}")

if __name__ == '__main__':
    # Check if pygame is available
    try:
        import pygame
        print("Pygame is available - running tests...")
        unittest.main(verbosity=2)
    except ImportError:
        print("Pygame not available - skipping tests")
        print("Install pygame with: pip install pygame")
        sys.exit(1)
