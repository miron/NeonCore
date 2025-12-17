import unittest
from NeonCore.managers.npc_manager import NPCManager

class TestNPCManager(unittest.TestCase):
    def test_get_npcs_in_location_deduplication(self):
        """Test that get_npcs_in_location does not return duplicates for aliased NPCs"""
        manager = NPCManager()
        # "industrial_zone" is where Lazlo and Lenard (aliased as dirty_cop) are
        npcs = manager.get_npcs_in_location("industrial_zone")
        
        names = [npc.name for npc in npcs]
        self.assertEqual(len(names), len(set(names)), f"Duplicate NPCs found: {names}")
        
        # Verify Lenard is present (since he was the one duplicated)
        self.assertIn("Lenard", names)
        # Verify Lazlo is present
        self.assertIn("Lazlo", names)

if __name__ == "__main__":
    unittest.main()
