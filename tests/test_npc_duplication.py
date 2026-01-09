import unittest
import sys
import os

# Add project root to path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from NeonCore.managers.npc_manager import NPCManager

class TestNPCManager(unittest.TestCase):
    def test_no_duplicate_npcs(self):
        """Ensure get_npcs_in_location doesn't return duplicates."""
        # Note: This requires the actual JSON files to be present.
        # Ideally we'd mock the JSON loading, but for a regression test
        # of the current data state, running against real data is acceptable 
        # as per the original script.
        
        manager = NPCManager()
        # Test a known location
        npcs = manager.get_npcs_in_location("industrial_zone")
        
        names = [npc.name for npc in npcs]
        self.assertEqual(len(names), len(set(names)), "Duplicate NPCs found in industrial_zone")

if __name__ == "__main__":
    unittest.main()
