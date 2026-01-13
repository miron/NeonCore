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

class TestItemPersistence(unittest.TestCase):
    def setUp(self):
        # RESET SINGLETON
        DatabaseManager._instance = None
        
        self.test_db_path = "test_items_custom.db"
        if os.path.exists(self.test_db_path):
             os.remove(self.test_db_path)
             
        self.db = DatabaseManager(db_path=self.test_db_path)
        self.db._initialize_db()
        
        # Define an Item with stats
        self.weapon_name = "Super Gun"
        self.weapon_stats = {"damage": "10d6", "ammo": 100, "rof": 2}
        
    def tearDown(self):
        self.db.close()
        if os.path.exists(self.test_db_path):
            os.remove(self.test_db_path)

    def test_weapon_stats_persistence(self):
        """
        Verify that a weapon created with custom stats retains them
        after being saved to and loaded from the DB.
        """
        # 1. Create Template with Stats
        # Logic mimics ActionManager.do_choose New Game creation
        # It dumps stats into base_stats
        t_id = self.db.create_template(
            self.weapon_name, 
            "weapon", 
            "A test gun.", 
            base_stats=json.dumps(self.weapon_stats)
        )
        self.assertIsNotNone(t_id)

        # 2. Create INSTANCE
        i_id = self.db.create_instance(t_id, owner_id="TestHero")
        self.assertIsNotNone(i_id)
        
        # 3. VERIFY INSTANCE RETRIEVAL (Simulate Load)
        # ActionManager uses db.get_item(i_id)
        loaded_item = self.db.get_item(i_id)
        
        print(f"DEBUG: Loaded Item: {loaded_item}")
        
        self.assertIn("damage", loaded_item, "Damage stat missing from loaded item")
        self.assertEqual(loaded_item["damage"], "10d6")
        self.assertEqual(loaded_item["ammo"], 100)
        self.assertEqual(loaded_item["rof"], 2)

if __name__ == '__main__':
    unittest.main()
