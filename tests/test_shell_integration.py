
import unittest
from unittest.mock import MagicMock, patch, AsyncMock
from NeonCore.managers.action_manager import ActionManager

class TestShellIntegration(unittest.IsolatedAsyncioTestCase):
    def setUp(self):
        # Mock dependencies
        self.mock_deps = MagicMock()
        self.mock_deps.char_mngr = MagicMock()
        self.mock_deps.char_mngr.player = MagicMock()
        self.mock_deps.skill_check = MagicMock()
        self.mock_deps.npc_manager = MagicMock()
        
        # Initialize ActionManager with mocks
        self.action_manager = ActionManager(self.mock_deps)
        self.action_manager.game_state = "before_perception_check" # Allow command
        
        # Async Mocking for io
        self.action_manager.io = AsyncMock()

    @patch("NeonCore.game_mechanics.combat_shells.GrappleShell")
    async def test_grab_initiates_grapple_shell(self, MockGrappleShell):
        """Test that do_grab launches the GrappleShell on success"""
        # Setup
        # Mock NPC
        mock_npc = MagicMock()
        mock_npc.location = "loc1"
        mock_npc.handle = "lenard"
        self.mock_deps.npc_manager.get_npc.return_value = mock_npc
        self.mock_deps.world.player_position = "loc1"
        
        # Mock Roll Success
        self.action_manager.char_mngr.player.roll_check.return_value = {"result": "success"}

        # Execute
        await self.action_manager.do_grab("lenard")
        
        # Verify
        # 1. GrappleShell instantiated
        # Note: do_grab instantiates it but doesn't call cmdloop() anymore in new design.
        # It sets self.grapple_shell
        MockGrappleShell.assert_called_once()
        self.assertIsNotNone(self.action_manager.grapple_shell)
        self.assertEqual(self.action_manager.game_state, "grappling")

    async def test_brawling_double_attack(self):
        """Test that brawling executes 2 attacks without shell"""
        # Setup
        mock_npc = MagicMock()
        self.mock_deps.npc_manager.get_npc.return_value = mock_npc
        
        # Mock Roll Success
        self.action_manager.char_mngr.player.roll_check.return_value = {"result": "success"}

        # Execute
        await self.action_manager.do_use_skill("brawling lenard")
        
        # Verify interaction
        # roll_check called twice
        self.assertEqual(self.action_manager.char_mngr.player.roll_check.call_count, 2)
        # take_damage called twice (since we mocked success)
        self.assertEqual(mock_npc.take_damage.call_count, 2)

    async def test_standard_skill_check_fallback(self):
        """Test that other skills fall back to standard skill_check"""
        # Execute
        await self.action_manager.do_use_skill("athletics jumper")
        
        # Verify standard skill check called
        self.action_manager.skill_check.do_use_skill.assert_called_once_with(
            "athletics", "jumper"
        )

if __name__ == "__main__":
    unittest.main()
