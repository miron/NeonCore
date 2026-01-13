from managers.database_manager import DatabaseManager

def seed_data():
    db = DatabaseManager()
    print("Seeding database...")

    # 1. Create Templates
    burner_id = db.create_template(
        name="Glitching Burner", 
        item_type="tool", 
        description="A cheap, vibrating burner phone."
    )
    print(f"Created Template: Glitching Burner ({burner_id})")

    assault_rifle_id = db.create_template(
        name="Assault Rifle",
        item_type="weapon",
        description="Standard issue ballistics.",
        base_stats='{"damage": "5d6"}'
    )
    # Common Gear from Characters
    db.create_template("Burner Phone", "gear", "A disposable phone", '{"notes": "A disposable phone"}')
    db.create_template("Shotgun", "weapon", "Close quarters power.", '{"dmg": "5d6", "ammo": 4, "rof": 1, "notes": "8 rounds extra"}')
    db.create_template("Heavy Pistol", "weapon", "Reliable sidearm.", '{"dmg": "3d6", "ammo": 8, "rof": 2, "notes": "Standard issue"}')
    db.create_template("Assault Rifle", "weapon", "Standard military rifle.", '{"dmg": "5d6", "ammo": 25, "rof": 1, "notes": "25 rounds extra"}')
    db.create_template("Tool Hand", "cyberware", "Built-in toolkit.")
    
    # 2. Create Initial World State
    # (Optional: Spawn items in world if needed, or rely on Game Logic to spawn them)
    # db.create_instance(burner_id, location_id="start_square") 

    print("Database seeded.")

if __name__ == "__main__":
    seed_data()
