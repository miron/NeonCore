from sheet import characters_sheet
"""Character Creator"""
class Character:
    def __init__(self, character_data):
        self.handle = character_data[0]
        self.role = character_data[1]

        self.stats = {}
        self.stats["INT"] = character_data[2][0]
        self.stats["REF"] = character_data[3][0]
        self.stats["DEX"] = character_data[4][0]
        self.stats["TECH"] = character_data[5][0]
        self.stats["COOL"] = character_data[6][0]
        self.stats["WILL"] = character_data[7][0]
        self.stats["LUCK"] = character_data[8]
        self.stats["MOVE"] = character_data[9]
        self.stats["BODY"] = character_data[10]
        self.stats["EMP"] = character_data[11][0]

        self.skills = {}
        self.skills["Accounting"] = (self.stats["INT"], character_data[2][1])
        self.skills["Bureaucracy"] = (self.stats["INT"], character_data[2][2])
        self.skills["Business"] = (self.stats["INT"], character_data[2][3])
        self.skills["Composition"] = (self.stats["INT"], character_data[2][4])
        self.skills["Conceal/Reveal Object"] = (self.stats["INT"], character_data[2][5])
        self.skills["Criminology"] = (self.stats["INT"], character_data[2][6])
        self.skills["Cryptography"] = (self.stats["INT"], character_data[2][7])
        self.skills["Deduction"] = (self.stats["INT"], character_data[2][8])
        self.skills["Education"] = (self.stats["INT"], character_data[2][9])
        self.skills["Library Search"] = (self.stats["INT"], character_data[2][10])
        self.skills["Local Expert"] = (self.stats["INT"], character_data[2][11])
        self.skills["Perception"] = (self.stats["INT"], character_data[2][12])
        self.skills["Tactics"] = (self.stats["INT"], character_data[2][13])
        self.skills["Tracking"] = (self.stats["INT"], character_data[2][14])

        self.skills["Drive Land Vehicle"] = (self.stats["REF"], character_data[3][1])
        self.skills["Handgun"] = (self.stats["REF"], character_data[3][2])
        self.skills["Shoulder Arms"] = (self.stats["REF"], character_data[3][3])

        self.skills["Athletics"] = (self.stats["DEX"], character_data[4][1])
        self.skills["Brawling"] = (self.stats["DEX"], character_data[4][2])
        self.skills["Evasion"] = (self.stats["DEX"], character_data[4][3])
        self.skills["Melee Weapon"] = (self.stats["DEX"], character_data[4][4])
        self.skills["Stealth"] = (self.stats["DEX"], character_data[4][5])

        self.skills["Electronics/Security Tech"] = (self.stats["TECH"], character_data[5][1])
        self.skills["First Aid"] = (self.stats["TECH"], character_data[5][2])
        self.skills["Forgery"] = (self.stats["TECH"], character_data[5][3])
        self.skills["Paramedic"] = (self.stats["TECH"], character_data[5][4])
        self.skills["Photography/Film"] = (self.stats["TECH"], character_data[5][5])
        self.skills["Pick Lock"] = (self.stats["TECH"], character_data[5][6])
        self.skills["Pick Pocket"] = (self.stats["TECH"], character_data[5][7])
        self.skills["Play Instrument"] = (self.stats["TECH"], character_data[5][8])

        self.skills["Acting"] = (self.stats["COOL"], character_data[6][1])
        self.skills["Bribery"] = (self.stats["COOL"], character_data[6][2])
        self.skills["Interrogation"] = (self.stats["COOL"], character_data[6][3])
        self.skills["Persuasion"] = (self.stats["COOL"], character_data[6][4])
        self.skills["Streetwise"] = (self.stats["COOL"], character_data[6][5])
        self.skills["Trading"] = (self.stats["COOL"], character_data[6][6])
        self.skills["Wardrobe & Style"] = (self.stats["COOL"], character_data[6][7])

        self.skills["Concentration"] = (self.stats["WILL"], character_data[7][1])
        self.skills["Resist Torture/Drugs"] = (self.stats["WILL"], character_data[7][2])

        self.skills["Conversation"] = (self.stats["EMP"], character_data[11][1])
        self.skills["Human Perception"] = (self.stats["EMP"], character_data[11][2])

        self.hp = character_data[12]
        self.seriously_wounded = character_data[13]
        self.death_save = character_data[14]
        self.armor = (character_data[15][0], character_data[15][1])
        self.weapon_1 = (character_data[16][0], character_data[16][1], character_data[16][2], 
                            character_data[16][3], character_data[16][4])
        self.weapon_2 = (character_data[17][0], character_data[17][1], character_data[17][2], 
                            character_data[17][3], character_data[17][4])
        self.role_ability = character_data[18]
        self.cyberware_1 = character_data[19]
        self.cyberware_2 = character_data[20]
        self.gear = character_data[21]
        self.portrait = character_data[22]
        self.notes = character_data[23]
        self.lifepath = self.generate_lifepath()
    
    # Lifepath generator function
    def generate_lifepath(self):
        """ Generate and assign lifepath data""" 
        return "lifepath placeholder"


    def skill_total(self, skill_name)
        skill_tuple = self.skills[skill_name]
        return sum(skill_tuple)