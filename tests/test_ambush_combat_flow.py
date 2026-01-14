import unittest
import asyncio
from unittest.mock import MagicMock, AsyncMock, patch
from NeonCore.game_mechanics.combat_system import CombatEncounter
from NeonCore.managers.character_manager import Character
from NeonCore.core.async_cmd import AsyncCmd

class TestAmbushCombatFlow(unittest.TestCase):
    def setUp(self):
        self.mock_io = AsyncMock()
        self.player = MagicMock(spec=Character)
        self.player.handle = "V"
        self.player.combat = {"hp": 30}
        self.player.skill_total.return_value = 14 
        
        self.enemy1 = MagicMock(spec=Character)
        self.enemy1.handle = "Dirty Cop 1"
        self.enemy1.hp = 35
        self.enemy1.sp = 7
        
        self.enemies = [self.enemy1]

    def test_combat_init_signature(self):
        """Test that CombatEncounter supports the new async signature (injecting IO)"""
        combat = CombatEncounter(self.player, self.enemies, self.mock_io)
        self.assertIsInstance(combat, AsyncCmd)

    def test_combat_methods_are_async(self):
        """Verify key methods are now async"""
        combat = CombatEncounter(self.player, self.enemies, self.mock_io)
        self.assertTrue(asyncio.iscoroutinefunction(combat.start_combat))
        self.assertTrue(asyncio.iscoroutinefunction(combat.do_shoot))
        
    def test_combat_flow_simulation(self):
        """Simulate a combat turn via start_combat (mocking cmdloop)"""
        async def run_simulation():
            combat = CombatEncounter(self.player, self.enemies, self.mock_io)
            # Mock cmdloop to avoid hanging
            combat.cmdloop = AsyncMock()
            
            result = await combat.start_combat()
            
            # Verify it set up the turn
            self.assertEqual(combat.turn_count, 1)
            # Verify it called cmdloop
            combat.cmdloop.assert_called_once()
            
        asyncio.run(run_simulation())

    def test_available_commands(self):
        """Verify that only whitelist commands are available"""
        combat = CombatEncounter(self.player, self.enemies, self.mock_io)
        names = combat.get_names()
        
        # Equip REMOVED
        expected = ["do_shoot", "do_cover", "do_flee", "do_take", "do_look", "do_help", "do_quit"]
        for cmd in expected:
            self.assertIn(cmd, names)
            
        # Verify do_equip is GONE
        self.assertNotIn("do_equip", names)

        # Verify completenames logic
        completions = combat.completenames("sh")
        self.assertIn("shoot ", completions)
        
        # Verify NO leakage
        self.assertNotIn("do_say", names)

    def test_postcmd_free_actions(self):
        """Verify free actions don't trigger enemy turn"""
        combat = CombatEncounter(self.player, self.enemies, self.mock_io)
        combat._enemy_turn = AsyncMock()
        
        # Test Free Action: look
        async def check_free():
             # Initialize turn count
             combat.turn_count = 0
             advance = await combat.postcmd(False, "look")
             return advance
        
        asyncio.run(check_free())
        combat._enemy_turn.assert_not_called()
        self.assertEqual(combat.turn_count, 0)
        
        # Test Turn Action: shoot
        async def check_turn():
             combat.turn_count = 0
             await combat.postcmd(False, "shoot 1")
        
        asyncio.run(check_turn())
        combat._enemy_turn.assert_called_once()
        self.assertEqual(combat.turn_count, 1)

    def test_do_quit(self):
        """Verify do_quit returns True (signals stop) instead of SystemExit"""
        combat = CombatEncounter(self.player, self.enemies, self.mock_io)
        async def check_quit():
             return await combat.do_quit("")
             
        result = asyncio.run(check_quit())
        result = asyncio.run(check_quit())
        self.assertTrue(result)

    def test_complete_shoot(self):
        """Verify complete_shoot returns enemy handles"""
        combat = CombatEncounter(self.player, self.enemies, self.mock_io)
        
        # Test empty input -> all enemies
        comps = combat.complete_shoot("", "shoot ", 0, 0)
        self.assertIn("Dirty Cop 1", comps)
        
        # Test partial input "Dirty" -> match
        comps_partial = combat.complete_shoot("Dirty", "shoot Dirty", 0, 0)
        self.assertIn("Dirty Cop 1", comps_partial)
        
        # Test selection by name (integration-ish)
        async def check_select():
             # Mock enemies with correct handle
             combat.enemies = [self.enemy1] 
             # Should find "Dirty Cop 1" via "Dirty"
             target = await combat._select_target("Dirty")
             return target
             
        found = asyncio.run(check_select())
        self.assertEqual(found, self.enemy1)

if __name__ == '__main__':
    unittest.main()
