import unittest
import sys
import os
import asyncio
from unittest.mock import MagicMock, AsyncMock, patch

# Adjust path to import NeonCore modules
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Mock modules that might cause side effects on import
sys.modules['NeonCore.utils.utils'] = MagicMock()
sys.modules['NeonCore.ai_backends.ollama'] = MagicMock()
sys.modules['NeonCore.ai_backends.gemini'] = MagicMock()

from NeonCore.managers.action_manager import ActionManager

class TestSaveCommand(unittest.TestCase):
    def setUp(self):
        # Mock Dependencies
        self.mock_deps = MagicMock()
        self.mock_deps.io = AsyncMock()
        self.mock_deps.char_mngr = MagicMock()
        self.mock_deps.cmd_mngr = MagicMock()
        self.mock_deps.skill_check = MagicMock()
        self.mock_deps.story_manager = AsyncMock() # Used in postcmd
        
        # Mock World and DB
        self.mock_deps.world = MagicMock()
        self.mock_deps.world.db = MagicMock()
        self.mock_deps.world.player_position = "loc_1"
        
        # Mock Player
        self.mock_player = MagicMock()
        self.mock_player.handle = "TestHero"
        self.mock_player.to_dict.return_value = {
            "stats": {"ref": 10},
            "combat": {"hp": 5},
            "inventory_ids": [],
            "equipped_ids": []
        }
        self.mock_deps.char_mngr.player = self.mock_player

    def test_do_save_success(self):
        """Test do_save command execution success path."""
        # Initialize ActionManager with mocked dependencies
        # Patching internal inits to avoid side effects
        with patch('NeonCore.managers.action_manager.GeminiBackend'), \
             patch('NeonCore.managers.action_manager.OllamaBackend'):
            
            am = ActionManager(self.mock_deps)
            
            # Setup DB return
            self.mock_deps.world.db.save_player.return_value = True
            
            # Run Async Method
            asyncio.run(am.do_save(""))
            
            # Verify save_player called with correct structure
            self.mock_deps.world.db.save_player.assert_called_once()
            call_args = self.mock_deps.world.db.save_player.call_args[0]
            
            handle, loc, full_stats, inv_ids, equip_ids = call_args
            
            self.assertEqual(handle, "TestHero")
            self.assertEqual(loc, "loc_1")
            
            # VERIFY THE FIX: full_stats should be a dict with 'attributes' and 'combat'
            # and NOT raise NameError name 'data' is not defined
            self.assertIn("attributes", full_stats)
            self.assertIn("combat", full_stats)
            self.assertEqual(full_stats["attributes"], {"ref": 10})

    def test_do_save_no_player(self):
        """Test save with no player loaded."""
        self.mock_deps.char_mngr.player = None
        
        with patch('NeonCore.managers.action_manager.GeminiBackend'), \
             patch('NeonCore.managers.action_manager.OllamaBackend'):
            
            am = ActionManager(self.mock_deps)
            asyncio.run(am.do_save(""))
            
            self.mock_deps.io.send.assert_called_with("No character loaded to save.")
            self.mock_deps.world.db.save_player.assert_not_called()

if __name__ == '__main__':
    unittest.main()
