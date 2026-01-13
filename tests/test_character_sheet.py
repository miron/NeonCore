
import unittest
from unittest.mock import MagicMock
from NeonCore.managers.character_manager import CharacterManager
from NeonCore.managers.character import Character

class TestCharacterSheetData(unittest.TestCase):
    def setUp(self):
        self.char_mngr = CharacterManager()
        # Mocking generic character since we don't need persistent DB for this
        self.mock_char = MagicMock(spec=Character)
        self.mock_char.handle = "TestChar"
        self.mock_char.role = "Solo"
        self.mock_char.stats = {"body": 7} # Should give 3d6
        self.mock_char.weapons = [{"name": "Pistol"}]
        self.mock_char.role_ability = {"name": "Combat Sense", "notes": "Test"}
        
        # Ensure copy works on mocks (limitations)
        # We might need a real object or clearer mock structure
        # Let's use a dict-like structure for components if deepcopy is used
        
    def test_brawling_injection(self):
        """Test that Brawling weapon is injected correctly based on Body stat"""
        # Create a real-ish character to avoid deepcopy issues with Mocks
        char = MagicMock()
        char.handle = "Test"
        char.role = "Solo"
        char.stats = {"body": 7}
        char.combat = {}
        char.skills = {}
        char.ascii_art = ""
        char.defence = {}
        char.weapons = [{"name": "Pistol"}]
        char.role_ability = {"name": "Combat Sense", "notes": "Test"}
        char.cyberware = []
        char.inventory = []
        
        # Test Body 7 -> 3d6
        data = self.char_mngr.get_character_sheet_data(char)
        
        # Check Weapons List
        weapons = data['weapons']
        self.assertEqual(len(weapons), 2) # Pistol + Brawling
        
        # Find Brawling
        brawling = next((w for w in weapons if w['name'] == "Brawling"), None)
        self.assertIsNotNone(brawling)
        self.assertEqual(brawling['dmg'], "3d6")
        self.assertEqual(brawling['rof'], 2)
        
        # Verify original pistol is still there
        pistol = next((w for w in weapons if w['name'] == "Pistol"), None)
        self.assertIsNotNone(pistol)
        
        # Verify Original Character Object was NOT mutated
        self.assertEqual(len(char.weapons), 1)

    def test_brawling_damage_tiers(self):
        """Verify damage tiers"""
        tiers = [
            (4, "1d6"),
            (5, "2d6"),
            (6, "2d6"),
            (7, "3d6"),
            (10, "3d6"),
            (11, "4d6")
        ]
        
        for body, expected_dmg in tiers:
            char = MagicMock()
            char.stats = {"body": body}
            char.weapons = []
            char.role_ability = {} # prevent getattr error
            
            data = self.char_mngr.get_character_sheet_data(char)
            brawling = data['weapons'][0]
            self.assertEqual(brawling['dmg'], expected_dmg, f"Body {body} should be {expected_dmg}")

if __name__ == "__main__":
    unittest.main()
