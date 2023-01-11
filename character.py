"""Character Creator"""
class Character:
    def __init__(self, handle, role, stats, combat, skills, armor, weapons, role_ability, cyberware, gear, ascii_art):
        self.handle = handle
        self.role = role
        self.stats = stats
        self.combat = combat
        self.skills = skills
        self.armor = armor
        self.weapons = weapons
        self.role_ability = role_ability
        self.cyberware = cyberware
        self.gear = gear
        self.ascii_art = ascii_art
        self.lucky_pool = self.stats["luck"]

        self.lifepath = self.generate_lifepath()
    
    # Lifepath generator function
    def generate_lifepath(self):
        """ Generate and assign lifepath data""" 
        return "lifepath placeholder"

    def skill_total(self, skill_name):
        skill_tuple = self.skills[skill_name]
        return sum(skill_tuple)


