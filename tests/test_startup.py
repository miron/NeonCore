import unittest
import sys
import os
from unittest.mock import MagicMock, patch

# Add package root to path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from NeonCore.core.dependencies import GameDependencies
from NeonCore.managers.action_manager import ActionManager


class TestStartup(unittest.TestCase):
    @patch("NeonCore.managers.action_manager.sys.exit")
    @patch("NeonCore.managers.action_manager.ActionManager.cmdloop")
    def test_initialization_and_start(self, mock_cmdloop, mock_exit):
        """Test initialization AND start_game to catch runtime imports."""
        try:
            am = GameDependencies.initialize_game()
            self.assertIsInstance(am, ActionManager)
            print("\nSuccessfully initialized ActionManager")

            # Mock os.system to avoid clearing actual screen
            with patch("os.system") as mock_os:
                am.start_game()

            print("Successfully ran start_game()")
        except Exception as e:
            self.fail(f"Game crash on start: {e}")


if __name__ == "__main__":
    unittest.main()
