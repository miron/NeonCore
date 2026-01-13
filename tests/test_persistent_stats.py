import unittest
import json
import os
import sys
import shutil
import sqlite3

# Adjust path to import NeonCore modules
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from NeonCore.managers.database_manager import DatabaseManager
from NeonCore.managers.character import Character

class TestPersistentStats(unittest.TestCase):
    def setUp(self):
        # Use a temporary file db for testing (in-memory might behave differently with connection closing)
        self.test_db_path = "test_persistence.db"
        self.db = DatabaseManager(db_path=self.test_db_path)
        
        # Test Data
        self.handle = "test_hero"
        self.stats = {"ref": 8, "int": 5, "cool": 4, "luck": 5, "body": 5} # Attributes (Added luck/body)
        self.combat = {"hp": 1, "sp": 10}            # Combat Stats (Modified)
        
        # Mock Character
        self.char = Character(
            char_id="123",
            handle=self.handle,
            role="Solo",
            stats=self.stats.copy(),
            combat=self.combat.copy(),
            skills={},
            defence={},
            weapons=[],
            cyberware=[],
            gear=[],
            ascii_art=""
        )

    def tearDown(self):
        self.db.close()
        if os.path.exists(self.test_db_path):
            os.remove(self.test_db_path)

    def test_stats_persistence_flow(self):
        """
        Verify that saving a character with modified combat stats 
        and then loading it restores those exact stats.
        """
        # 1. MIMIC ActionManager.do_save LOGIC
        # We must replicate exactly what ActionManager does: construct the full_stats dict
        full_stats = {
            "attributes": self.char.stats,
            "combat": self.char.combat
        }
        
        # Save to DB
        self.db.save_player(
            self.char.handle,
            "location_id_1",
            full_stats, # The fix: Passing the dict, not just attributes
            [],
            []
        )
        
        # 2. MIMIC ActionManager.do_choose (Load) LOGIC
        loaded_row = self.db.load_player(self.handle)
        self.assertIsNotNone(loaded_row, "Failed to load player from DB")
        
        # Parse the JSON from the DB row
        # DatabaseManager saves it as JSON string, load_player returns row (dict-like)
        raw_stats_json = loaded_row['stats']
        loaded_payload = json.loads(raw_stats_json)
        
        # 3. VERIFY PAYLOAD STRUCTURE
        self.assertIn("attributes", loaded_payload)
        self.assertIn("combat", loaded_payload)
        self.assertEqual(loaded_payload['combat']['hp'], 1) 
        
        # 4. RESTORE STATE (Character logic)
        new_char = Character(
            char_id="999",
            handle="new_instance",
            role="Solo",
            stats={"ref": 1, "luck": 5}, # Default/Wrong stats
            combat={"hp": 100}, # Default/Wrong stats
            skills={},
            defence={},
            weapons=[],
            cyberware=[],
            gear=[],
            ascii_art=""
        )
        
        new_char.restore_state(loaded_payload, [], [])
        
        # 5. FINAL ASSERTIONS
        self.assertEqual(new_char.stats['ref'], 8, "Attributes not restored")
        self.assertEqual(new_char.combat['hp'], 1, "Combat stats (HP) not restored!")
        self.assertEqual(new_char.combat['sp'], 10, "Combat stats (SP) not restored!")

if __name__ == '__main__':
    unittest.main()
