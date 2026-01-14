import unittest
import asyncio
from unittest.mock import MagicMock
from NeonCore.managers.action_manager import ActionManager
from NeonCore.managers.character_manager import CharacterManager
from NeonCore.managers.npc_manager import NPCManager
from NeonCore.managers.story_manager import StoryManager
from NeonCore.world.world import World
from NeonCore.story_modules.heywood_ambush import HeywoodAmbush

class MockIO:
    async def send(self, msg):
        pass

class TestAmbushLogic(unittest.IsolatedAsyncioTestCase):
    async def asyncSetUp(self):
        self.char_mngr = CharacterManager()
        self.npc_mngr = NPCManager(self.char_mngr)
        self.io = MockIO()
        
        # World needs dependencies in constructor
        self.world = World(self.char_mngr, self.npc_mngr, self.io)
        
        # Mock Dependencies object
        self.deps = MagicMock()
        self.deps.io = self.io
        self.deps.world = self.world
        
        self.story_mngr = StoryManager()
        self.story_mngr.set_dependencies(self.deps)
        
        self.deps.npc_manager = self.npc_mngr
        self.deps.char_mngr = self.char_mngr
        self.deps.story_manager = self.story_mngr

        # Load NPCs (This normally reads from npcs.json, ensuring we have the data)
        self.char_mngr.load_characters()
        
        # FIX: Set a player so update() doesn't return early
        if self.char_mngr.characters:
            self.char_mngr.set_player(next(iter(self.char_mngr.characters.values())))

        # Ensure Lenard exists in manager but has NO location (mimicking current bug)
        lenard = self.npc_mngr.get_npc("Lenard")
        if lenard:
            lenard.location = None 
            
    async def test_lenard_spawn_on_scene_start(self):
        """Verify Lenard appears in heywood_alley when Ambush story starts"""
        # Setup
        self.world.player_position = "heywood_alley"
        story = HeywoodAmbush()
        self.story_mngr.register_story(HeywoodAmbush)
        self.story_mngr.current_story = story
        
        # Act: Trigger Start (which calls update -> run_intro_scene)
        await story.start(self.deps)
        
        # Assert: Lenard should be in heywood_alley
        lenard = self.npc_mngr.get_npc("Lenard")
        self.assertIsNotNone(lenard, "Lenard NPC should exist")
        self.assertEqual(lenard.location, "heywood_alley", "Lenard should be moved to heywood_alley")
        
        # Assert: Dirty Cop should NOT be there yet (wait for trigger)
        cop = self.npc_mngr.get_npc("Dirty Cop")
        self.assertNotEqual(cop.location, "heywood_alley", "Dirty Cop should not appear yet")

if __name__ == '__main__':
    unittest.main()
