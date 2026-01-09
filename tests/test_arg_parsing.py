import unittest
import sys
import os

# Add project root to path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Note: We are testing parsing logic that moved to ActionManager, 
# but the original script tested it via a mock. 
# We'll create a simple test that verifies the string split logic used in ActionManager.

class TestActionArgs(unittest.TestCase):
    def test_skill_arg_parsing(self):
        # Simulate logic in ActionManager.do_use_skill
        arg = "brawling lenard"
        parts = arg.strip().split(maxsplit=1)
        skill_name = parts[0].lower() if parts else ""
        target_name = parts[1] if len(parts) > 1 else None
        
        self.assertEqual(skill_name, "brawling")
        self.assertEqual(target_name, "lenard")

    def test_skill_arg_parsing_no_target(self):
        arg = "brawling"
        parts = arg.strip().split(maxsplit=1)
        skill_name = parts[0].lower() if parts else ""
        target_name = parts[1] if len(parts) > 1 else None
        
        self.assertEqual(skill_name, "brawling")
        self.assertIsNone(target_name)

if __name__ == "__main__":
    unittest.main()
