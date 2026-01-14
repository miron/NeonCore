import unittest
from unittest.mock import MagicMock
import sys
import os

# Add the project root to the path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from NeonCore.world.world import World

class TestWorldExpansion(unittest.TestCase):
    def setUp(self):
        self.mock_char_mngr = MagicMock()
        self.mock_npc_manager = MagicMock()
        self.mock_io = MagicMock()
        self.world = World(self.mock_char_mngr, self.mock_npc_manager, self.mock_io)

    def test_heywood_locations_exist(self):
        """Verify that the new Heywood locations exist in the world."""
        self.assertIn("heywood_industrial", self.world.locations)
        self.assertIn("heywood_alley", self.world.locations)
        self.assertIn("warehouse_entrance", self.world.locations)
        self.assertIn("warehouse_interior", self.world.locations)

    def test_navigation_chain(self):
        """Verify that the player can navigate from start to the warehouse."""
        # Check link from start_square (existing) or accessible area to heywood
        # Assuming we link industrial_zone -> heywood_industrial
        
        # 1. Industrial Zone -> Heywood Industrial
        ind_zone = self.world.locations.get("industrial_zone")
        self.assertTrue(ind_zone, "Industrial Zone missing")
        self.assertIn("heywood_industrial", ind_zone["exits"].values(), "No exit to Heywood Industrial from Industrial Zone")
        
        # 2. Heywood Industrial -> Heywood Alley
        heywood_ind = self.world.locations["heywood_industrial"]
        self.assertIn("heywood_alley", heywood_ind["exits"].values(), "No exit to Alley from Heywood Industrial")

        # 3. Heywood Alley -> Warehouse Entrance
        alley = self.world.locations["heywood_alley"]
        self.assertIn("warehouse_entrance", alley["exits"].values(), "No exit to Warehouse from Alley")

        # 4. Warehouse Entrance -> Warehouse Interior
        entrance = self.world.locations["warehouse_entrance"]
        self.assertIn("warehouse_interior", entrance["exits"].values(), "No exit to Interior from Warehouse Entrance")

    def test_ascii_art_presence(self):
        """Verify that the new locations have ASCII art populated."""
        self.assertIsNotNone(self.world.locations["heywood_alley"].get("ascii_art"))
        self.assertIsNotNone(self.world.locations["warehouse_interior"].get("ascii_art"))

if __name__ == '__main__':
    unittest.main()
