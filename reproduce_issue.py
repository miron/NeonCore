from NeonCore.managers.npc_manager import NPCManager

def reproduction():
    manager = NPCManager()
    npcs = manager.get_npcs_in_location("industrial_zone")
    print(f"NPCs in industrial_zone: {[npc.name for npc in npcs]}")
    
    # Check for duplicates
    names = [npc.name for npc in npcs]
    if len(names) != len(set(names)):
        print("FAIL: Duplicate NPCs found.")
    else:
        print("PASS: No duplicates found.")

if __name__ == "__main__":
    reproduction()
