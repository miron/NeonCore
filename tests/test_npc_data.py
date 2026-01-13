import unittest
import json
from pathlib import Path
from NeonCore.managers.npc_manager import NPCManager

class TestNPCData(unittest.TestCase):
    def setUp(self):
        self.npc_path = Path(__file__).parent.parent / "NeonCore/character_assets/npcs.json"
        
    def test_npc_json_exists(self):
        """Verify npcs.json file exists"""
        self.assertTrue(self.npc_path.exists(), "npcs.json should exist")

    def test_story_npcs_defined(self):
        """Verify critical story NPCs (Lazlo, Lenard) are in npcs.json"""
        if not self.npc_path.exists():
            self.fail("npcs.json missing")
            
        with open(self.npc_path) as f:
            data = json.load(f)
            
        handles = [npc.get("handle", "").lower() for npc in data]
        
        self.assertIn("lazlo", handles, "Lazlo should be defined in npcs.json")
        self.assertIn("lenard", handles, "Lenard should be defined in npcs.json")

    def test_character_manager_loading(self):
        """Integration: Verify CharacterManager loads these NPCs"""
        from NeonCore.managers.character_manager import CharacterManager
        
        cm = CharacterManager()
        # Ensure cm has loaded npcs
        npc_handles = [n.handle.lower() for n in cm.npcs]
        
        self.assertIn("lazlo", npc_handles)
        self.assertIn("lenard", npc_handles)
        
        # Verify stats loading
        lazlo = cm.get_npc("lazlo")
        self.assertEqual(lazlo.role, "Fixer")
        self.assertEqual(lazlo.location, "industrial_zone")


    def test_npc_visibility_by_location(self):
        """Verify NPCManager correctly calls get_npcs_in_location"""
        from NeonCore.managers.character_manager import CharacterManager
        from NeonCore.managers.npc_manager import NPCManager
        
        cm = CharacterManager()
        nm = NPCManager(cm)
        
        # Test Industrial Zone
        visible = nm.get_npcs_in_location("industrial_zone")
        handles = [n.handle.lower() for n in visible]
        
        self.assertIn("lazlo", handles, "Lazlo should be visible in industrial_zone")
        self.assertIn("lenard", handles, "Lenard should be visible in industrial_zone")
        
    def test_npc_description_loaded(self):
        """Verify NPCs have descriptions loaded from JSON"""
        from NeonCore.managers.character_manager import CharacterManager
        cm = CharacterManager()
        
        lazlo = cm.get_npc("lazlo")
        self.assertTrue(lazlo.description, "Lazlo should have a description")
        
        lenard = cm.get_npc("lenard")
        self.assertTrue(lenard.description, "Lenard should have a description")

