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
    print(f"Created Template: Assault Rifle ({assault_rifle_id})")
    
    # 2. Create Initial World State
    # (Optional: Spawn items in world if needed, or rely on Game Logic to spawn them)
    # db.create_instance(burner_id, location_id="start_square") 

    print("Database seeded.")

if __name__ == "__main__":
    seed_data()
