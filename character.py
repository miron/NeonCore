"""Character Creator"""
import random
class Character:
    def __init__(self, handle, role, stats, combat, skills, defence, weapons, role_ability, cyberware, gear, ascii_art):
        self.handle = handle
        self.role = role
        self.stats = stats
        self.combat = combat
        self.skills = skills
        self.defence = defence
        self.weapons = weapons
        self.role_ability = role_ability
        self.cyberware = cyberware
        self.gear = gear
        self.ascii_art = ascii_art
        self.lucky_pool = self.stats["luck"]
        self.x = None
        self.y = None

        self.lifepath = Lifepath()
		self.cultural_region = self.lifepath.roll('cultural_region')
		self.clothing_style = self.lifepath.roll('clothing_style')
		self.personality = self.lifepath.roll('personality')


    def skill_total(self, skill_name):
        skill_tuple = self.skills[skill_name]
        return sum(skill_tuple)

class Lifepath:
	def __init__(self):
		self.tables = {
			'cultural_regions': {
				1: "North American",
				2: "South/Central American",
				3: "Western European",
				4: "Eastern European",
				5: "Middle Eastern/North African",
				6: "Sub-Saharan African",
				7: "South Asian",
				8: "South East Asian",
				9: "East Asian",
				10: "Oceania/Pacific Islander"
			},
			'personalities': {
				1: "Shy and secretive",
				2: "Rebellious, antisocial, and violent",
				3: "Arrogant, proud, and aloof",
				4: "Moody, rash, and headstrong",
				5: "Picky, fussy, and nervous",
				6: "Stable and serious",
				7: "Silly and fluff-headed",
				8: "Sneaky and deceptive",
				9: "Intellectual and detached",
				10: "Friendly and outgoing"
			},
			'clothing_style': {
				1: "Generic Chic (Standard, Colorful, Modular)",
				2: "Leisurewear (Comfort, Agility, Athleticism)",
				3: "Urban Flash (Flashy, Technological, Streetwear)",
				4: "Businesswear (Leadership, Presence, Authority)",
				5: "High Fashion (Exclusive, Designer, Couture)",
				6: "Bohemian (Folksy, Retro, Free-spirited)",
				7: "Bag Lady Chic (Homeless, Ragged, Vagrant)",
				8: "Gang Colors (Dangerous, Violent, Rebellious)",
				9: "Nomad Leathers (Western, Rugged, Tribal)",
				10: "Asia Pop (Bright, Costume-like, Youthful)"
			},
			'hairstyle' = {
				1: "Mohawk",
				2: "Long and ratty",
				3: "Short and spiked",
				4: "Wild and all over",
				5: "Bald",
				6: "Striped",
				7: "Wild colors",
				8: "Neat and short",
				9: "Short and curly",
				10: "Long and straight"	
			},

	}


	def roll(self, table_name):
		table = self.tables[table_name]
		roll = random.randint(1, 10)
		return table[roll]




