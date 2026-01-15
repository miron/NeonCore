import unittest
from unittest.mock import MagicMock, AsyncMock, patch
import asyncio
from NeonCore.story_modules.heywood_ambush import HeywoodAmbush
from NeonCore.managers.character import Character

class TestSceneSkills(unittest.IsolatedAsyncioTestCase):
    async def test_forgery_check_in_ambush(self):
        # Setup Context
        story = HeywoodAmbush()
        story.state = "briefcase_dropped" # Updated state assumption
        story._trigger_ambush = AsyncMock() # Mock the combat trigger
        
        # Mock Dependencies
        mock_io = AsyncMock()
        mock_player = MagicMock()
        mock_player.skill_total.return_value = 10 # Base Skill
        
        mock_context = MagicMock()
        mock_context.io = mock_io
        mock_context.char_mngr.player = mock_player
        mock_context.action_manager.log_event = AsyncMock()
        
        # 1. Test Success (High Roll)
        with patch('random.randint', return_value=8): # 10 + 8 = 18 >= 17
            result = await story.handle_use_skill(mock_context, "forgery", "briefcase")
            
            self.assertTrue(result)
            mock_io.send.assert_any_call("\n\033[1;36m[SUCCESS]\033[0m You inspect the bills closely. The holograms are off-center.")
            mock_context.action_manager.log_event.assert_called_with("Discovered Counterfeit Money")

        # 2. Test Failure (Low Roll) - Open briefcase first
        mock_io.reset_mock()
        story.briefcase_open = True # Prerequisite for checking money
        with patch('random.randint', return_value=2): # 10 + 2 = 12 < 17
            result = await story.handle_use_skill(mock_context, "forgery", "money")
            
            self.assertTrue(result)
            mock_io.send.assert_any_call("\n\033[1;31m[FAILURE]\033[0m Look real enough to you.")

        # 3. Test Invalid Target
        mock_io.reset_mock()
        result = await story.handle_use_skill(mock_context, "forgery", "banana")
        self.assertTrue(result) # It handles it by saying "Check what?"
        mock_io.send.assert_any_call("Check forgery on what? (e.g., 'money' or 'briefcase')")

        # 4. Test Irrelevant Skill (Should return False)
        result = await story.handle_use_skill(mock_context, "athletics", "wall")
        self.assertFalse(result)

if __name__ == '__main__':
    unittest.main()
