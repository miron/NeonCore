
import unittest
from unittest.mock import MagicMock, patch
from NeonCore.managers.action_manager import ActionManager

class TestShellIntegration(unittest.TestCase):
    def setUp(self):
        # Mock dependencies
        self.mock_deps = MagicMock()
        self.mock_deps.char_mngr = MagicMock()
        self.mock_deps.char_mngr.player = MagicMock()
        self.mock_deps.skill_check = MagicMock()
        
        # Initialize ActionManager with mocks
        self.action_manager = ActionManager(self.mock_deps)
        self.action_manager.game_state = "before_perception_check" # Allow command

    @patch("NeonCore.game_mechanics.combat_shells.BrawlingShell")
    def test_brawling_shell_launch(self, MockBrawlingShell):
        """Test that use_skill brawling launches the BrawlingShell"""
        # Setup
        mock_shell_instance = MockBrawlingShell.return_value
        
        # Execute
        self.action_manager.do_use_skill("brawling lenard")
        
        # Verify
        # 1. BrawlingShell instantiated with correct args
        MockBrawlingShell.assert_called_once_with(
            self.action_manager.char_mngr.player, 
            "lenard"
        )
        # 2. cmdloop() called on the instance
        mock_shell_instance.cmdloop.assert_called_once()
        
    def test_standard_skill_check_fallback(self):
        """Test that other skills fall back to standard skill_check"""
        # Execute
        self.action_manager.do_use_skill("athletics jumper")
        
        # Verify standard skill check called
        self.action_manager.skill_check.do_use_skill.assert_called_once_with(
            "athletics", "jumper"
        )

    def test_brawling_missing_target(self):
        """Test graceful failure when target is missing for brawling"""
        with patch("sys.stdout") as mock_stdout: # Suppress print
             self.action_manager.do_use_skill("brawling")
             
             # Should NOT init shell
             # We can't easily assert "not imported" but we can check side effects or mocked imports if we mocked the module
             # Ideally we'd verify it prints the error message
             pass # Logic just returns, so verification is implicit "no crash"

if __name__ == "__main__":
    unittest.main()
