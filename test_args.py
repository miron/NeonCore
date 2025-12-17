
class MockPlayer:
    def get_skills(self): return ["brawling"]
    def skill_total(self, s): return 10
    
class MockCharMngr:
    player = MockPlayer()

class MockSkillCheck:
    char_mngr = MockCharMngr()
    def do_use_skill(self, skill_name, target_name=None):
        print(f"Called with skill_name='{skill_name}', target_name='{target_name}'")
        if skill_name not in self.char_mngr.player.get_skills():
            print("Skill not found")
        else:
            print("Skill found")
            
m = MockSkillCheck()
m.do_use_skill("brawling lenard")
