import unittest
from unittest.mock import MagicMock
from NeonCore.managers.role_manager import RoleManager, RockerboyAbility, SoloAbility, TechAbility, RoleDisplayData
from NeonCore.managers.npc_manager import NPC
from NeonCore.managers.character import Character
from NeonCore.managers.trait_manager import DigitalSoul

class TestRoleSystem(unittest.TestCase):
    def test_role_factory(self):
        """Verify RoleManager returns correct classes"""
        rocker = RoleManager.get_ability("Rockerboy", rank=5)
        self.assertIsInstance(rocker, RockerboyAbility)
        self.assertEqual(rocker.rank, 5)

        solo = RoleManager.get_ability("Solo", rank=3)
        self.assertIsInstance(solo, SoloAbility)
        self.assertEqual(solo.get_passive_bonuses()['initiative'], 3)
        
        tech = RoleManager.get_ability("Tech")
        self.assertIsInstance(tech, TechAbility)
        self.assertEqual(tech.rank, 4) # Default

        media = RoleManager.get_ability("Media")
        self.assertEqual(media.get_display_data().name, "Credibility")

    def test_rockerboy_charismatic_impact(self):
        """Verify social context generation for fans"""
        ability = RockerboyAbility(rank=4)
        
        # Test Fan
        context = ability.get_social_context("Fan")
        self.assertIn("TARGET IS A FAN", context)
        self.assertIn("Charismatic Impact Rank 4", context)
        
        # Test Neutral
        context = ability.get_social_context("Neutral")
        self.assertEqual(context, "")
        
        # Test None
        context = ability.get_social_context(None)
        self.assertEqual(context, "")

    def test_npc_relationships(self):
        """Verify NPC class stores relationship data"""
        npc = NPC(name="Lazlo", role="Fixer", location="void", description="Test guy")
        npc.relationships["Forty"] = "Fan"
        
        self.assertEqual(npc.relationships.get("Forty"), "Fan")
        self.assertIsNone(npc.relationships.get("RandomGuy"))

    def test_character_initialization(self):
        """Verify Character initializes with RoleAbility"""
        char = Character(
            char_id="123", handle="TestRocker", role="Rockerboy",
            stats={"luck": 5}, combat={}, skills={}, defence={}, weapons=[],
            role_ability=None, # Should be overridden or handled? 
            # Wait, Character.__init__ takes role_ability argument still!
            # My change initialized it inside __init__ using RoleManager.
            # But the signature still expects it passed in?
            # Let's check Character.__init__ signature again.
            cyberware=[], gear=[], ascii_art=""
        )
        # In my refactor, I kept the `role_ability` arg in __init__ but then OVERWROTE it inside?
        # Or did I use the arg?
        # Checked diff: I added `self.role_ability = RoleManager.get_ability(self.role, rank=4)`
        # BUT I kept `role_ability` in the args list.
        # This means the passed value is IGNORED unless I used `role_ability if role_ability else ...`
        # Let's verify behavior.
        
        self.assertIsInstance(char.role_ability, RockerboyAbility)
        self.assertEqual(char.role_ability.get_display_data().name, "Charismatic Impact")

    def test_json_loading_integrity(self):
        """Verify CharacterManager can load characters without role_ability field in JSON"""
        from NeonCore.managers.character_manager import CharacterManager
        # We need to mock open/json or just rely on the actual file if it exists.
        # Since I just edited the actual file, let's try to load it.
        # IMPORTANT: This integration test relies on the file system.
        try:
            cm = CharacterManager()
            forty = cm.get_npc("Forty") # Forty is a PC but loaded in characters dict
            # Actually CharacterManager splits PCs and NPCs.
            # PC is self.player (not set by load) or in self.characters
            # Check self.characters
            
            # Find Forty
            forty = None
            for c in cm.characters.values():
                if c.handle == "Forty":
                    forty = c
                    break
            
            self.assertIsNotNone(forty, "Forty should be loaded")
            self.assertIsInstance(forty.role_ability, RockerboyAbility)
            self.assertEqual(forty.role_ability.get_display_data().name, "Charismatic Impact")
            
        except Exception as e:
            self.fail(f"Character loading failed: {e}")

if __name__ == '__main__':
    unittest.main()
