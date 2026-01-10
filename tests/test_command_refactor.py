
import asyncio
import unittest
from unittest.mock import MagicMock
from NeonCore.managers.action_manager import ActionManager
from NeonCore.managers.character import Character
from NeonCore.managers.npc_manager import NPC, NPCManager

class TestCommandRefactor(unittest.TestCase):
    def setUp(self):
        # Mock Dependencies
        self.mock_game = MagicMock()
        self.mock_io = MagicMock()
        self.mock_io.send =  MagicMock(side_effect=lambda x: print(f"[MOCK IO] {x}")) 
        
        # Mock Managers
        self.char_mngr = MagicMock()
        self.npc_mngr = MagicMock() # We will replace with real logic if needed or just mock
        self.world = MagicMock()
        self.world.player_position = "test_loc"
        
        self.dependencies = MagicMock()
        self.dependencies.world = self.world
        self.dependencies.npc_manager = self.npc_mngr
        self.dependencies.io = self.mock_io
        self.dependencies.char_mngr = self.char_mngr
        self.dependencies.cmd_mngr = MagicMock()
        self.dependencies.skill_check = MagicMock()
        
        # Setup Player
        self.player = Character(
            char_id=1, handle="Sim", role="Solo",
            stats={'dex': 8, 'body': 8, 'luck': 5}, 
            combat={'hp': 20},
            skills={'brawling': {'stat': 'dex', 'lvl': 5}},
            defence={}, weapons=[],
            role_ability={}, cyberware=[], gear=[], ascii_art=""
        )
        self.char_mngr.player = self.player
        
        # Init ActionManager
        # Mocking generic backends to avoid init crash
        with unittest.mock.patch('NeonCore.managers.action_manager.GeminiBackend'), \
             unittest.mock.patch('NeonCore.managers.action_manager.OllamaBackend'), \
             unittest.mock.patch('NeonCore.utils.utils.HelpSystem'):
             self.am = ActionManager(self.dependencies)
        self.am.game_state = "before_perception_check"

    def test_smart_take_pickup(self):
        """Test 'take' on ground item (simulated by failing inventory check)"""
        # Note: logic mocks 'case' behavior specifically for environment in current code
        # But generic pickup is commented out. We test the failure msg "You don't see that..."
        # or if we implement a find_item mock.
        pass 

    def test_smart_take_draw(self):
        """Test 'take' drawing weapon from inventory"""
        weapon = {'name': 'Pistol', 'dmg': '2d6'}
        self.player.inventory.append(weapon)
        
        asyncio.run(self.am.do_take("pistol"))
        
        self.assertIn(weapon, self.player.weapons)
        self.assertNotIn(weapon, self.player.inventory)

    def test_use_object_stow(self):
        """Test 'use_object' stowing weapon"""
        weapon = {'name': 'Pistol', 'dmg': '2d6'}
        self.player.weapons.append(weapon)
        
        asyncio.run(self.am.do_use_object("pistol"))
        
        self.assertIn(weapon, self.player.inventory)
        self.assertNotIn(weapon, self.player.weapons)

    def test_grab_snatch(self):
        """Test 'grab item target' logic"""
        # Setup Target
        target = NPC(name="Lenard", role="Target", location="test_loc", description="", inventory=["Briefcase (Locked)"])
        self.npc_mngr.get_npc.return_value = target
        
        # Mock roll to success
        self.player.roll_check = MagicMock(return_value={'result': 'success'})
        self.am._trigger_ambush = MagicMock()
        
        asyncio.run(self.am.do_grab("case lenard"))
        
        # Check Transfer
        self.assertIn("Briefcase (Locked)", self.player.inventory)
        self.am._trigger_ambush.assert_called()

    def test_grab_grapple(self):
        """Test 'grab target' logic"""
        target = NPC(name="Lenard", role="Target", location="test_loc", description="")
        self.npc_mngr.get_npc.return_value = target
        
        self.player.roll_check = MagicMock(return_value={'result': 'success'})
        
        asyncio.run(self.am.do_grab("lenard"))
        
        self.assertEqual(self.am.game_state, "grappling")
        self.assertEqual(self.am.grappled_target, target)

if __name__ == '__main__':
    unittest.main()
