import unittest
import sys
import os
from unittest.mock import MagicMock

# Adjust path to import NeonCore modules
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Mock dependencies
sys.modules['NeonCore.utils.utils'] = MagicMock()
sys.modules['NeonCore.ai_backends.ollama'] = MagicMock()
sys.modules['NeonCore.ai_backends.gemini'] = MagicMock()

from NeonCore.managers.action_manager import ActionManager

class TestTabCompletion(unittest.TestCase):
    def setUp(self):
        self.mock_deps = MagicMock()
        self.mock_deps.io = MagicMock()
        # Initialize ActionManager
        self.am = ActionManager(self.mock_deps)

    def test_completenames_active_game(self):
        """Verify that 'active_game' state allows core commands like whoami/gear."""
        self.am.game_state = "active_game"
        
        # Test specific commands that should be allowed
        # Note: completenames filters a list of 'text' candidates.
        # We assume the parent method returns everything, so we mock super().completenames?
        # Actually ActionManager.completenames calls super().completenames first.
        # Since we can't easily mock super() in a simple unit test without class patching,
        # we can verify the logic by ensuring specific inputs work if we assume super returns them.
        
        # Let's patch the class to override super().completenames behavior for the test?
        # Or just trust that if we pass the command text, it should pass the filter.
        
        # ActionManager.completenames(text, line, begidx, endidx)
        # It calls super().completenames(text, *ignored)
        
        # We can simulate the filter logic directly or patch the instance method if needed.
        # But 'completenames' logic is:
        # candidates = super().completenames(...)
        # filtered = [c for c in candidates if c in allowed]
        
        # Let's rely on the fact that ActionManager *is* the class under test.
        # We'll just check if the logic allows it.
        
        # We need to mock completenames of AsyncCmd (parent) to return our candidate
        with unittest.mock.patch('NeonCore.core.async_cmd.AsyncCmd.completenames', return_value=["whoami", "gear", "save"]):
            res = self.am.completenames("whoami")
            self.assertIn("whoami", res)
            self.assertIn("gear", res)
            self.assertIn("save", res)

    def test_completenames_restricted_state(self):
        """Verify that irrelevant commands are filtered out in other states."""
        self.am.game_state = "choose_character"
        
        with unittest.mock.patch('NeonCore.core.async_cmd.AsyncCmd.completenames', return_value=["whoami", "gear", "choose"]):
            res = self.am.completenames("x")
            
            # 'choose' should be allowed
            self.assertIn("choose", res)
            
            # 'whoami' and 'gear' should be Blocked
            self.assertNotIn("whoami", res)
            self.assertNotIn("gear", res)

if __name__ == '__main__':
    unittest.main()
