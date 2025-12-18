import unittest
import sys
import os
import importlib.util

# Helper to import module bypassing package __init__ to avoid circular deps
def import_npc_manager():
    file_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "../NeonCore/managers/npc_manager.py"))
    spec = importlib.util.spec_from_file_location("npc_manager", file_path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.NPC

NPC = import_npc_manager()

class TestNPCCombat(unittest.TestCase):
    def test_npc_combat_attributes(self):
        # Create an NPC similar to Lenard
        lenard = NPC(
            name="Lenard",
            role="Dirty Cop",
            location="industrial_zone",
            description="...",
            skills={"handgun": 12, "brawling": 11},
            combat_stats={"hp": 30, "max_hp": 30},
            sp=5
        )
        
        # 1. Test Handle Property
        self.assertEqual(lenard.handle, "Lenard", "NPC handle should return name")
        
        # 2. Test Skill Total
        self.assertEqual(lenard.skill_total("brawling"), 11, "NPC skill_total should return skill value")
        self.assertEqual(lenard.skill_total("unknown"), 0, "NPC skill_total should return 0 for unknown skill")
        
        # 3. Test Take Damage
        lenard.take_damage(10, ignore_armor=False)
        # SP is 5, Damage 10 -> Effective 5
        self.assertEqual(lenard.combat_stats["hp"], 25, "NPC should take damage correctly after armor")
        
        # 4. Test Ignore Armor
        lenard.take_damage(5, ignore_armor=True)
        # Damage 5 direct
        self.assertEqual(lenard.combat_stats["hp"], 20, "NPC should take full damage when ignore_armor=True")

if __name__ == "__main__":
    unittest.main()
