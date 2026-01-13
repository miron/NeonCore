import unittest
import json
import os
import sys
import shutil
import sqlite3
import asyncio

# Adjust path to import NeonCore modules
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from NeonCore.managers.database_manager import DatabaseManager
from NeonCore.managers.action_manager import ActionManager
from NeonCore.managers.character_manager import CharacterManager
from unittest.mock import MagicMock, AsyncMock, patch

class TestWorldPersistence(unittest.TestCase):
    def setUp(self):
        # RESET SINGLETON to valid separate DBs for tests
        DatabaseManager._instance = None
        
        # Use simple file name for testing
        self.test_db_path = "test_world_persistence.db"
        
        # Ensure clean slate physically
        if os.path.exists(self.test_db_path):
             os.remove(self.test_db_path)
             
        self.db = DatabaseManager(db_path=self.test_db_path)
        # Force initialization just in case logic skips it (it shouldn't)
        self.db._initialize_db()
        # User observed: "Burner Phone (A disposable phone)" -> "Burner Phone"
        # This implies the template name is "Burner Phone" and description is "A disposable phone"
        # And the UI combines them in 'gear'? Or the name itself was constructed?
        
        self.template_name = "Burner Phone"
        self.template_desc = "A disposable phone"
        self.t_id = self.db.create_template(
            self.template_name, 
            "gear", 
            self.template_desc, 
            base_stats=json.dumps({"cost": 50})
        )
        
    def tearDown(self):
        self.db.close()
        if os.path.exists(self.test_db_path):
            os.remove(self.test_db_path)

    def test_persistence_between_sessions(self):
        """
        Verify that an item dropped by Player A is visible to Player B (New Game).
        """
        # 1. Player A drops item
        loc_id = "loc_start"
        i_id_A = self.db.create_instance(self.t_id, owner_id="PlayerA")
        
        # Simulate Drop: Update Item State to Location, Owner=None
        self.db.update_item_state(i_id_A, location_id=loc_id, owner_id=None)
        
        # 2. Player B (New Game) looks in location
        items_in_loc = self.db.get_items_in_location(loc_id)
        
        # Verify Player B sees the item
        found = False
        for item in items_in_loc:
            if item['id'] == i_id_A:
                found = True
                break
        
        self.assertTrue(found, "Dropped item should persist for other players/sessions")

    def test_name_consistency(self):
        """
        Reproduce the 'Name Change' bug.
        Expected: Item name should remain consistent or predictable.
        """
        # 1. Create Instance
        # If the item in inventory was "Burner Phone (A disposable phone)",
        # maybe the template name IS "Burner Phone".
        # Let's see what get_items_in_location returns.
        
        i_id = self.db.create_instance(self.t_id, owner_id="PlayerA")
        
        # 2. Check Database Return (Simulate 'gear' loading form DB)
        item_data = self.db.get_item(i_id)
        
        # Logic in DatabaseManager.get_item:
        # final_name = item_data['name'] if item_data['name'] else item_data['template_name']
        
        # Since we didn't provide an override name in create_instance, it uses template name.
        self.assertEqual(item_data['name'], "Burner Phone")
        
        # If the user saw "Burner Phone (A disposable phone)", where did that come from?
        # A) The UI (ActionManager.do_gear or CharacterManager) appends description?
        # B) The item WAS created with a name including the description?
        
        # If it's UI formatting:
        # "Name (Description)" or "Name (Notes)"
        
        # Let's assume the UI creates the formatted string.
        # If I drop it, get_items_in_location returns name/desc separately.
        # "Items on ground: Burner Phone" (User log).
        # This matches Template Name.
        
        # When I 'take' it:
        # ActionManager.do_take -> updates owner_id.
        # Then I 'gear':
        # output is "- Burner Phone" (User log).
        # Original was "- Burner Phone (A disposable phone)".
        
        # Implication: The ORIGINAL item had a custom NAME stored in 'item_instances.name'.
        # OR the original item in inventory came from a different source (hardcoded dict in Character?)
        
        # Let's test if create_instance allows preserving a custom name.
        stored_name = "Burner Phone (A disposable phone)"
        
        # Manually insert to simulate what might have happened during Intro generation?
        # NO, DatabaseManager.create_instance doesn;t take a 'name' arg currently!
        # It ONLY takes template_id, location_id, owner_id.
        # So 'item_instances.name' is ALWAYS NULL by default.
        
        # CONCLUSION: The original "Burner Phone (A disposable phone)" likely
        # came from a hardcoded inventory list in `ActionManager` or `CharacterManager` 
        # that wasn't yet backed by a DB instance with that exact name?
        # OR the UI adds the description ONLY for certain items?
        
        pass

if __name__ == '__main__':
    unittest.main()
