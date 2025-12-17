import sys
import unittest
from unittest.mock import MagicMock
from NeonCore.managers.action_manager import ActionManager

class TestTabCompletion(unittest.TestCase):
    def setUp(self):
        # Mock dependencies
        self.mock_deps = MagicMock()
        self.mock_deps.char_mngr.character_names.return_value = ["V (Solo)", "Jackie (Solo)"]
        self.mock_deps.world.player_position = "street"
        self.mock_deps.world.locations = {"street": {"exits": {"north": "bar"}}}
        
        # Mock NPC manager to return a Judy npc
        mock_npc = MagicMock()
        mock_npc.name = "Judy"
        self.mock_deps.npc_manager.get_npcs_in_location.return_value = [mock_npc]
        
        self.am = ActionManager(self.mock_deps)
        # Suppress prints
        self.am.stdout = MagicMock()

    def test_completenames_adds_space(self):
        """Test that main command completion adds a space"""
        # We need to set a game state that allows commands
        self.am.game_state = "before_perception_check"
        
        # 'tal' should complete to 'talk '
        completions = self.am.completenames("tal")
        # We expect only 'talk' or 'talk '
        self.assertTrue(len(completions) > 0, "Should find 'talk' command")
        
        # Check if ANY completion is 'talk ' (with space)
        # Note: Pre-fix, this will likely fail or return just 'talk'
        print(f"DEBUG: completenames('tal') returned: {completions}")
        
        # Strictly check for space suffix
        has_spaced_talk = any(c == "talk " for c in completions)
        self.assertTrue(has_spaced_talk, f"Expected 'talk ' in completions, got {completions}")

    def test_complete_talk_adds_space(self):
        """Test that argument completion adds a space"""
        self.am.game_state = "before_perception_check"
        
        # 'Ju' should complete to 'Judy '
        # Note: distinct complete_talk methods exist, we test the active one
        completions = self.am.complete_talk("Ju", "talk Ju", 0, 0)
        
        print(f"DEBUG: complete_talk('Ju') returned: {completions}")
        
        has_spaced_judy = any(c == "Judy " for c in completions)
        self.assertTrue(has_spaced_judy, f"Expected 'Judy ' in completions, got {completions}")

if __name__ == '__main__':
    unittest.main()
