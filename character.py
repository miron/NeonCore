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
        self.hairstyle = self.lifepath.roll('hairstyle')
        self.value = self.lifepath.roll('value')
        self.original_background = self.lifepath.roll('original_background')
        self.childchood_environment = self.lifepath.roll('childhood_environment')
        self.family_crisis = self.lifepath.roll('family_crisis')
		


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
            'hairstyle': {
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
           'value': {
                    1: "Money",
                    2: "Honor",
                    3: "Your word",
                    4: "Honesty",
                    5: "Knowledge",
                    6: "Vengeance",
                    7: "Love",
                    8: "Power",
                    9: "Family",
                    10: "Friendship"
            },
            'traits': {
                1: "I stay neutral.",
                2: "I stay neutral.",
                3: "I like almost everyone.",
                4: "I hate almost everyone.",
                5: "People are tools. Use them for your own goals then discard them.",
                6: "Every person is a valuable individual.",
                7: "People are obstacles to be destroyed if they cross me.",
                8: "People are untrustworthy. Don't depend on anyone.",
                9: "Wipe 'em all out and let the cockroaches take over.",
                10: "People are wonderful!"
            },
            'original_background': {
                1: "Corporate Execs",
                2: "Corporate Managers",
                3: "Corporate Technicians",
                4: "Nomad Pack",
                5: "Ganger 'Family'",
                6: "Combat Zoners",
                7: "Urban Homeless",
                8: "Megastructure",
                9: "Warren Rats",
                10: "Reclaimers",
                11: "Edgerunners"
            },
			'original_background' {
				1: {'name': 'Corporate Execs', 'description': 'Wealthy, powerful, with servants, luxury homes, and the best of everything. Private security made sure you were always safe. You definitely went to a big-name private school.'},
				2: {'name': 'Corporate Managers', 'description': 'Well to do, with large homes, safe neighborhoods, nice cars, etc. Sometimes your parents) would hire servants, although this was rare. You had a mix of private and corporate education.'},
				3: {'name': 'Corporate Technicians', 'description': 'Middle-middle class, with comfortable conapts or Beaverville suburban homes, minivans and corporate-run technical schools. Kind of like living 1950s America crossed with 1984.'},
				4: {'name': 'Nomad Pack', 'description': 'You had a mix of rugged trailers, vehicles, and huge road kombis for your home. You learned to drive and fight at an early age, but the family was always there to care for you. Food was adually fresh and abundant. Mostly home schooled.'},
				5: {'name': 'Ganger "Family"', 'description': "A savage, violent home in any place the gang could take over. You were usually hungry, cold, and scared. You probably didn't know who your actual parents were. Education? The Gang taught you how to fight, kill, and steal--what else did you need to know?"},
				6: {'name': 'Combat Zoners', 'description': 'A step up from a gang "family," your home was a decaying building somewhere in the \'Zone\', heavily fortified. You were hungry at times, but regularly could score a bed and a meal. Home schooled.'},
				7: {'name': 'Urban Homeless', 'description': 'You lived in cars, dumpsters, or abandoned shipping modules. If you were lucky. You were usually hungry, cold, and scared, unless you were tough enough to fight for the scraps. Education? School of Hard Knocks.'},
				8: {'name': 'Megastructure', 'description': 'You grew up in one of the huge new megastructures that went up after the War. A tiny conapt, kibble and scop for food, a mostly warm bed. Some better educated adult warren dwellers or a local Corporation may have set up a school.'},
				9: {'name': 'Warren Rats', 'description': 'You started out on the road, but then moved into one of the deserted ghost towns or cities to rebuild it. A pioneer life: dangerous, but with plenty of simple food and a safe place to sleep. You were home schooled if there was anyone who had the time.'},
				10: {'name': 'Reclaimers', 'description': 'Your home was always changing based on your parents\' current "job." Could be a luxury apartment, an urban conapt, or a dumpster if you were on the run. Food and shelter ran the gamut from gourmet to kibble.'}
			},
			'childhood_environment' {
				1: "Ran on The Street, with no adult supervision.",
				2: "Spent in a safe Corp Zone walled off from the rest of the City.",
				3: "In a Nomad pack moving from place to place.",
				4: "In a Nomad pack with roots in transport (ships, planes, caravans).",
				5: "In a decaying, once upscale neighborhood, now holding off the boosters to survive.",
				6: "In the heart of the Combat Zone, living in a wrecked building or other squat.",
				7: "In a huge 'megastructure' buildingcontrolled by a Corp or the City.",
				8: "In the ruins of a deserted town or city taken over by Reclaimers.",
				9: "In a Drift Nation (a floating offshore city) that is a meeting place for all kinds of people.",
				10: "In a Corporate luxury 'starscraper,' high above the rest of the teeming rabble."
			},
			'family_crisis' {
				1: "Your family lost everything through betrayal.",
				2: "Your family lost everything through bad management.",
				3: "Your family was exiled or otherwise driven from their original home/ nation/ Corporation.",
				4: "Your family is imprisoned, and you alone escaped.",
				5: "Your family vanished. You are the only remaining member.",
				6: "Your family was killed, and you were the only survivor.",
				7: "Your family is involved in a long-term conspiracy, organization, or association, such as a crime family or revolutionary group.",
				8: "Your family was scattered to the winds due to relegation.",
				9: "Your family is cursed with a hereditary feud that has lasted for generations.",
				10: "You are the inheritor of a family debt, you must honor this debt before moving on with your life.",
			},










    }


    def roll(self, table_name):
        table = self.tables[table_name]
        roll = random.randint(1, 10)
        return table[roll]




