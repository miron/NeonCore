import sqlite3
import uuid
import logging
import os
import json

class DatabaseManager:
    _instance = None
    
    
    def __new__(cls, db_path=None):
        if cls._instance is None:
            cls._instance = super(DatabaseManager, cls).__new__(cls)
            
            if db_path is None:
                # Default to Project Root (../../ from managers dir)
                base_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
                db_path = os.path.join(base_dir, "neoncore.db")
                
            cls._instance.db_path = db_path
            cls._instance.connection = None
            cls._instance._initialize_db()
        return cls._instance

    def _get_connection(self):
        """Establish or return existing connection."""
        if self.connection is None:
            try:
                self.connection = sqlite3.connect(self.db_path)
                self.connection.row_factory = sqlite3.Row  # Access columns by name
            except sqlite3.Error as e:
                logging.error(f"Database connection failed: {e}")
                return None
        return self.connection

    def _initialize_db(self):
        """Create necessary tables if they don't exist."""
        conn = self._get_connection()
        if not conn:
            return

        cursor = conn.cursor()
        
        # 1. Item Templates (Base Definitions)
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS item_templates (
                id TEXT PRIMARY KEY,
                name TEXT NOT NULL,
                type TEXT NOT NULL,
                description TEXT,
                base_stats JSON  -- Store stats like damage, armor, effect, etc.
            )
        ''')
        
        # 2. Item Instances (Unique Entities)
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS item_instances (
                instance_id TEXT PRIMARY KEY,
                template_id TEXT NOT NULL,
                name TEXT, -- Optional override name
                owner_id TEXT, -- Character Handle or NULL
                location_id TEXT, -- Location ID or NULL
                current_stats JSON, -- Mutable stats (ammo, condition)
                FOREIGN KEY (template_id) REFERENCES item_templates(id)
            )
        ''')

        # 3. Player Saves (Persistence)
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS player_saves (
                handle TEXT PRIMARY KEY,
                location_id TEXT,
                stats JSON,         -- HP, SP, etc.
                inventory_ids JSON, -- List of Item UUIDs
                equipped_ids JSON   -- List of Item UUIDs
            )
        ''')

        conn.commit()
        logging.info("Database initialized successfully.")

    def close(self):
        if self.connection:
            self.connection.close()
            self.connection = None

    
    def get_template_id_by_name(self, name):
        """Find a template ID by exact name."""
        conn = self._get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT id FROM item_templates WHERE name = ?", (name,))
        row = cursor.fetchone()
        return row['id'] if row else None

    # --- Item Operations ---

    def create_template(self, name, item_type, description, base_stats="{}"):
        """Create a new item template."""
        conn = self._get_connection()
        cursor = conn.cursor()
        t_id = str(uuid.uuid4())
        
        try:
            cursor.execute('''
                INSERT INTO item_templates (id, name, type, description, base_stats)
                VALUES (?, ?, ?, ?, ?)
            ''', (t_id, name, item_type, description, str(base_stats)))
            conn.commit()
            return t_id
        except sqlite3.Error as e:
            logging.error(f"Failed to create template: {e}")
            return None

    def create_instance(self, template_id, location_id=None, owner_id=None):
        """Spawn a unique instance of an item."""
        conn = self._get_connection()
        cursor = conn.cursor()
        i_id = str(uuid.uuid4())
        
        try:
            cursor.execute('''
                INSERT INTO item_instances (instance_id, template_id, location_id, owner_id, current_stats)
                VALUES (?, ?, ?, ?, '{}')
            ''', (i_id, template_id, location_id, owner_id))
            conn.commit()
            return i_id
        except sqlite3.Error as e:
            logging.error(f"Failed to create instance: {e}")
            return None

    def get_items_in_location(self, location_id):
        """Retrieve all items in a specific location."""
        conn = self._get_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT i.instance_id, i.name, t.name as template_name, t.type, t.description 
            FROM item_instances i
            JOIN item_templates t ON i.template_id = t.id
            WHERE i.location_id = ?
        ''', (location_id,))
        
        items = []
        for row in cursor.fetchall():
            # Merge template and instance data
            item_data = dict(row)
            # Use instance name if set, else template name
            final_name = item_data['name'] if item_data['name'] else item_data['template_name']
            items.append({
                "id": item_data['instance_id'],
                "name": final_name,
                "type": item_data['type'],
                "description": item_data['description']
            })
        return items

    
    def get_item(self, instance_id):
        """Retrieve a specific item by ID."""
        conn = self._get_connection()
        cursor = conn.cursor()
        
        # Select current_stats as well
        cursor.execute('''
            SELECT i.instance_id, i.name, i.current_stats, t.name as template_name, t.type, t.description, t.base_stats
            FROM item_instances i
            JOIN item_templates t ON i.template_id = t.id
            WHERE i.instance_id = ?
        ''', (instance_id,))
        
        row = cursor.fetchone()
        if row:
            item_data = dict(row)
            final_name = item_data['name'] if item_data['name'] else item_data['template_name']
            
            # 1. Parse Template Stats (Base)
            stats = {}
            if item_data['base_stats']:
                try:
                    stats = json.loads(item_data['base_stats'])
                except:
                    pass
            
            # 2. Parse/Merge Instance Stats (Current/Mutable Overrides)
            if item_data['current_stats']:
                try:
                    curr = json.loads(item_data['current_stats'])
                    stats.update(curr) # Instance overrides Template
                except:
                    pass
            
            return {
                "id": item_data['instance_id'],
                "name": final_name,
                "type": item_data['type'],
                "description": item_data['description'],
                **stats # Merge combined stats
            }
        return None

    def update_item_state(self, instance_id, location_id=None, owner_id=None):
        """Move an item to a new location or owner."""
        conn = self._get_connection()
        cursor = conn.cursor()
        
        try:
            cursor.execute('''
                UPDATE item_instances 
                SET location_id = ?, owner_id = ?
                WHERE instance_id = ?
            ''', (location_id, owner_id, instance_id))
            conn.commit()
            return True
        except sqlite3.Error as e:
            logging.error(f"Failed to move item: {e}")
            return False

    def update_instance_stats(self, instance_id, new_stats):
        """Update the mutable stats (current_stats) of an item instance."""
        conn = self._get_connection()
        cursor = conn.cursor()
        
        try:
            cursor.execute('''
                UPDATE item_instances 
                SET current_stats = ?
                WHERE instance_id = ?
            ''', (json.dumps(new_stats), instance_id))
            conn.commit()
            return True
        except sqlite3.Error as e:
            logging.error(f"Failed to update item stats: {e}")
            return False

    # --- Player Persistence ---

    def save_player(self, handle, location_id, stats, inventory_ids, equipped_ids):
        """Save player state to DB."""
        conn = self._get_connection()
        cursor = conn.cursor()
        
        # Upsert (Insert or Replace)
        try:
            cursor.execute('''
                INSERT OR REPLACE INTO player_saves (handle, location_id, stats, inventory_ids, equipped_ids)
                VALUES (?, ?, ?, ?, ?)
            ''', (handle, location_id, json.dumps(stats), json.dumps(inventory_ids), json.dumps(equipped_ids)))
            conn.commit()
            return True
        except sqlite3.Error as e:
            logging.error(f"Failed to save player: {e}")
            return False

    def load_player(self, handle):
        """Load player state from DB."""
        conn = self._get_connection()
        cursor = conn.cursor()
        
        cursor.execute("SELECT * FROM player_saves WHERE handle = ?", (handle,))
        row = cursor.fetchone()
        
        if row:
            return dict(row)
        return None

    def delete_player(self, handle):
        """Delete a player's save file."""
        conn = self._get_connection()
        cursor = conn.cursor()
        try:
             cursor.execute("DELETE FROM player_saves WHERE handle = ?", (handle,))
             if cursor.rowcount > 0:
                 conn.commit()
                 return True
             return False
        except sqlite3.Error as e:
            logging.error(f"Failed to delete save: {e}")
            return False

    def get_all_saved_handles(self):
        """Retrieve list of handles with save files."""
        conn = self._get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT handle FROM player_saves")
        rows = cursor.fetchall()
        return [row['handle'] for row in rows]
