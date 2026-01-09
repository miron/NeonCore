import unittest
import asyncio
import sys
import os

# Add project root to path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from unittest.mock import MagicMock
from NeonCore.managers.action_manager import ActionManager
from NeonCore.core.async_cmd import AsyncCmd

class MockIO:
    async def send(self, t): pass
    async def prompt(self, t): return ""

class MockDeps:
    def __init__(self):
        self.io = MockIO()
        self.char_mngr = MagicMock()
        self.npc_manager = None
        self.cmd_mngr = None
        self.skill_check = None
        self.dependencies = self # Self-referential for simplicity if needed

class TestActionManagerCompletion(unittest.TestCase):
    def setUp(self):
        self.deps = MockDeps()
        self.am = ActionManager(self.deps)

    def test_get_names_introspection(self):
        """Test that ActionManager can find its own do_ commands."""
        names = self.am.get_names()
        self.assertIn("do_choose", names)
        self.assertIn("do_quit", names)
        self.assertIn("do_help", names)

    def test_completenames_filtering(self):
        """Test that completenames returns match ending in space."""
        # Test empty string (listing all)
        all_cmds = self.am.completenames("")
        self.assertTrue(len(all_cmds) > 0)
        self.assertIn("choose ", all_cmds)
        
        # Test prefix matching
        ch_cmds = self.am.completenames("ch")
        self.assertIn("choose ", ch_cmds)
        
        # Test non-matching
        nonsense = self.am.completenames("xyzabc")
        self.assertEqual(nonsense, [])

    def test_async_cmd_get_completions(self):
        """Test the full retrieval of completions via AsyncCmd logic."""
        async def run_test():
            # 1. Command completion: "qu" -> "quit "
            # cursor at 2. text="qu", line="qu"
            res = await self.am.get_completions("qu", "qu", 0, 2)
            self.assertIn("quit ", res)
            
            # 2. Argument usage (assuming do_choose calls complete_choose)
            # Setup mock char manager for complete_choose
            self.deps.char_mngr.character_names.return_value = ["Mover", "Lazlo"]
            
            # "choose " (cursor at 7)
            res_args = await self.am.get_completions("", "choose ", 7, 7)
            self.assertIn("Mover ", res_args)
            self.assertIn("Lazlo ", res_args)

        asyncio.run(run_test())

if __name__ == "__main__":
    unittest.main()
