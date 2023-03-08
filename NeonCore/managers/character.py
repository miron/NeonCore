"""Character Creator"""
import random


class Character:
    def __init__(
            self, char_id, handle, role, stats, combat, skills, defence,
            weapons, role_ability, cyberware, gear, ascii_art):
        self.char_id = char_id
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
        self.personality = self.lifepath.roll('personality')
        self.clothing_style = self.lifepath.roll('clothing_style')
        self.hairstyle = self.lifepath.roll('hairstyle')
        self.affectation = self.lifepath.roll('affectation')
        self.value = self.lifepath.roll('value')
        self.trait = self.lifepath.roll('trait')
        self.valued_person = self.lifepath.roll('valued_person')
        self.valued_possession = self.lifepath.roll('valued_possession')
        self.original_background = self.lifepath.roll('original_backgrounds')
        self.childhood_environment = self.lifepath.roll(
            'childhood_environments')
        self.family_crisis = self.lifepath.roll('family_crises')
        self.friends = self.lifepath.get_friends()
        self.enemies = self.lifepath.get_enemies()
        self.lovers = self.lifepath.get_lovers()
        self.life_goal = self.lifepath.roll('life_goals')

    def skill_total(self, skill_name):
        skill_list = self.skills[skill_name]
        return sum(skill_list)
    
    def get_skills(self):
        return list(self.skills.keys())


class Lifepath:
    def __init__(self):
        self.tables = {
            'cultural_region': {
                1: {'region': "North American",
                    'language': ('Chinese', 'Cree', 'Creole', 'English',
                                 'French', 'Navajo', 'Spanish')},
                2: {'region': "South/Central American",
                    'language': ('Creole', 'English', 'German', 'Guarani',
                                 'Mayan', 'Portugese', 'Quechua', 'Spanish')},
                3: {'region': "Western European",
                    'language': ('Dutch', 'English', 'French', 'German',
                                 'Italian', 'Norwegian', 'Portuguese',
                                 'Spanish')},
                4: {'region': "Eastern European",
                    'language': ('English', 'Finnish', 'Polish', 'Romanian',
                                 'Russian', 'Ukrainian')},
                5: {'region': "Middle Eastern/North African",
                    'language': ('Arabic', 'Berber', 'English', 'Farsi',
                                 'French', 'Hebrew', 'Turkish')},
                6: {'region': "Sub-Saharan African",
                    'language': ('Arabic', 'English', 'French', 'Hausa',
                                 'Lingala', 'Oromo', 'Portuguese', 'Swahili',
                                 'Twi', 'Yoruba')},
                7: {'region': "South Asian",
                    'language' : ('Bengali', 'Dari', 'English', 'Hindi',
                                  'Nepali', 'Sinhalese', 'Tamil', 'Urdu')},
                8: {'region': "South East Asian",
                    'language': ('Arabic', 'Burmese', 'English', 'Filipino',
                                 'Hindi', 'Indonesian', 'Khmer', 'Malayan',
                                 'Vietnamese')},
                9: {'region': "East Asian",
                    'language': ('Cantonese Chinese', 'English', 'Japanese',
                                 'Korean', 'Mandarin Chinese', 'Mongolian')},
                10: {'region': "Oceania/Pacific Islander",
                     'language': ('English', 'French', 'Hawaiian', 'Maori',
                                  'Pama-Nyungan', 'Tahitian')}
            },
            'personality': {
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
            'affectation': {
                1: 'Tattoos',
                2: 'Mirrorshades',
                3: 'Ritual scars',
                4: 'Spiked gloves',
                5: 'Nose rings',
                6: 'Tongue or other piercings',
                7: 'Strange fingernail implants',
                8: 'Spiked boots or heels',
                9: 'Fingerless gloves',
                10: 'Strange contacts'
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
            'trait': {
                1: "I stay neutral.",
                2: "I stay neutral.",
                3: "I like almost everyone.",
                4: "I hate almost everyone.",
                5: ("People are tools. Use them for your own goals then "
                    "discard them."),
                6: "Every person is a valuable individual.",
                7: "People are obstacles to be destroyed if they cross me.",
                8: "People are untrustworthy. Don't depend on anyone.",
                9: "Wipe 'em all out and let the cockroaches take over.",
                10: "People are wonderful!"
            },
            'valued_person': {
                1: 'A parent',
                2: 'A brother or sister',
                3: 'A lover',
                4: 'A friend',
                5: 'Yourself',
                6: 'A pet',
                7: 'A teacher or mentor',
                8: 'A public figure',
                9: 'A personal hero',
                10: 'No one'
            },
            'valued_possession': {
                1: 'A weapon',
                2: 'A tool',
                3: 'A piece of clothing',
                4: 'A photograph',
                5: 'A book or diary',
                6: 'A recording',
                7: 'A musical instrument',
                8: 'A piece of jewelry',
                9: 'A toy',
                10: 'A letter'
            },
            'original_backgrounds': {
                1: {'name': 'Corporate Execs',
                    'description': (
                        "Wealthy, powerful, with servants, luxury homes, and "
                        "the best of everything. Private security made sure "
                        "you were always safe. You definitely went to a "
                        "big-name private school.")},
                2: {'name': 'Corporate Managers', 
                    'description': (
                        "Well to do, with large homes, safe neighborhoods, "
                        "nice cars, etc. Sometimes your parents would hire "
                        "servants, although this was rare. You had a mix of "
                        "private and corporate education.")},
                3: {'name': 'Corporate Technicians', 
                    'description': (
                        "Middle-middle class, with comfortable conapts or "
                        "Beaverville suburban homes, minivans and "
                        "corporate-run technical schools. Kind of like living "
                        "1950s America crossed with 1984.")},
                4: {'name': 'Nomad Pack', 
                    'description': (
                        "You had a mix of rugged trailers, vehicles, and huge "
                        "road kombis for your home. You learned to drive and "
                        "fight at an early age, but the family was always "
                        "there to care for you. Food was adually fresh and "
                        "abundant. Mostly home schooled.")},
                5: {'name': 'Ganger "Family"', 
                    'description': (
                        "A savage, violent home in any place the gang could "
                        "take over. You were usually hungry, cold, and scared."
                        " You probably didn't know who your actual parents "
                        "were. Education? The Gang taught you how to fight, "
                        "kill, and steal--what else did you need to know?")},
                6: {'name': 'Combat Zoners', 
                    'description': (
                        'A step up from a gang "family," your home was a '
                        "decaying building somewhere in the 'Zone', heavily "
                        "fortified. You were hungry at times, but regularly "
                        "could score a bed and a meal. Home schooled.")},
                7: {'name': 'Urban Homeless', 
                    'description': (
                        'You lived in cars, dumpsters, or abandoned shipping '
                        "modules. If you were lucky. You were usually hungry, "
                        "cold, and scared, unless you were tough enough to "
                        "fight for the scraps. Education? School of Hard "
                        "Knocks.")},
                8: {'name': 'Megastructure', 
                    'description': (
                        'You grew up in one of the huge new megastructures '
                        "that went up after the War. A tiny conapt, kibble and"
                        " scop for food, a mostly warm bed. Some better "
                        "educated adult warren dwellers or a local Corporation"
                        " may have set up a school.")},
                9: {'name': 'Warren Rats', 
                    'description': (
                        'You started out on the road, but then moved into one '
                        "of the deserted ghost towns or cities to rebuild it. "
                        "A pioneer life: dangerous, but with plenty of simple "
                        "food and a safe place to sleep. You were home "
                        "schooled if there was anyone who had the time.")},
                10: {'name': 'Reclaimers', 
                     'description': (
                         "Your home was always changing based on your parents'"
                         ' current "job." Could be a luxury apartment, an '
                         "urban conapt, or a dumpster if you were on the run. "
                         "Food and shelter ran the gamut from gourmet to "
                         "kibble.")}
            },
            'childhood_environments': {
                1: "Ran on The Street, with no adult supervision.",
                2: ("Spent in a safe Corp Zone walled off from the rest of the"
                    " City."),
                3: "In a Nomad pack moving from place to place.",
                4: ("In a Nomad pack with roots in transport (ships, planes, "
                    "caravans)."),
                5: ("In a decaying, once upscale neighborhood, now holding off"
                    " the boosters to survive."),
                6: ("In the heart of the Combat Zone, living in a wrecked "
                    "building or other squat."),
                7: ("In a huge 'megastructure' buildingcontrolled by a Corp or"
                    " the City."),
                8: ("In the ruins of a deserted town or city taken over by "
                    "Reclaimers."),
                9: ("In a Drift Nation (a floating offshore city) that is a "
                    "meeting place for all kinds of people."),
                10: ("In a Corporate luxury 'starscraper,' high above the rest"
                     " of the teeming rabble.")
            },
            'family_crises': {
                1: "Your family lost everything through betrayal.",
                2: "Your family lost everything through bad management.",
                3: ("Your family was exiled or otherwise driven from their "
                    "original home/ nation/ Corporation."),
                4: "Your family is imprisoned, and you alone escaped.",
                5: "Your family vanished. You are the only remaining member.",
                6: "Your family was killed, and you were the only survivor.",
                7: ("Your family is involved in a long-term conspiracy, "
                    "organization, or association, such as a crime family or "
                    "revolutionary group."),
                8: "Your family was scattered to the winds due to relegation.",
                9: ("Your family is cursed with a hereditary feud that has "
                    "lasted for generations."),
                10: ("You are the inheritor of a family debt, you must honor "
                     "this debt before moving on with your life."),
            },
			'life_goals': {
                1: "Get rid of a bad reputation",
                2: "Gain power and control",
                3: "Get off The Street no matter what it takes",
                4: "Cause pain and suffering to anyone who crosses you",
                5: "Live down your past life and try to forget it",
                6: ("Hunt down those responsible for your miserable life and "
                    "make them pay"),
                7: "Get what's rightfully yours",
                8: ("Save, if possible, anyone else involved in your "
                    "background, like a lover, or family member"),
                9: "Gain fame and recognition",
                10: "Become feared and respected"
			}
        }
        self.friends = {}
        self.enemies_list = {
            "Who": [
                "Ex-friend", "Ex-lover", "Estranged relative",
                "Childhood enemy", "Person working for you",
                "Person you work for", "Partner or coworker",
                "Corporate exec", "Government official", "Boosterganger"],
            "What caused it": [
                "Caused the other to lose face or status.", 
                "Caused the loss of lover, friend, or relative.", 
                "Caused a major public humiliation.", (
                "Accused the other of cowardice or some other major "
                    "personal flaw."), 
                "Deserted or betrayed the other.", (
                "Turned down the other's offer of a job or romantic "
                    "involvement."), 
                "You just don't like each other.", 
                "One of you was a romantic rival.",
                "One of you was a business rival.", 
                "One of you set the other up for a crime they didn't commit"],
            "What happens": [
                'Avoid the scum.', 'Avoid the scum.', (
                "Go into a murderous rage and try to physically rip their face"
                    "off."), (
                "Go into a murderous rage and try to physically rip their face"
                    "off."), 'Backstab them indirectly.', 
                'Backstab them indirectly.', 'Verbally attack them.', 
                'Verbally attack them.', (
                "Set them up for a crime or other transgression they didn't "
                    "commit."), 'Set out to murder or maim them.']
        }
        self.lovers = {}

    def roll(self, table_name):
        table = self.tables[table_name]
        roll = random.randint(1, 10)
        return table[roll]

    def get_friends(self):
        friend_types = {
            1: "Like an older sibling to you.",
            2: "Like a younger sibling to you.",
            3: "A teacher or mentor.",
            4: "A partner or coworker.",
            5: "A former lover.",
            6: "An old enemy.",
            7: "Like a parent to you.",
            8: "An old childhood friend.",
            9: "Someone you know from The Street.",
            10: "Someone with a common interest or goal."
        }

        num_friends = max(0, random.randint(1, 10) - 7)
        for i in range(num_friends):
            friend_type = random.randint(1, 10)
            self.friends[f"Friend {i+1}"] = friend_types[friend_type]
        return self.friends

    def get_enemies(self):
        num_enemies = max(0, random.randint(1, 10) - 7)
        enemies = []
        for _ in range(num_enemies):
            enemy = {}
            enemy["Who"] = random.choice(self.enemies_list["Who"])
            enemy["What caused it"] = random.choice(
                self.enemies_list["What caused it"])
            enemy["What happens"] = random.choice(
                self.enemies_list["What happens"])
            enemies.append(enemy)
        return enemies

    def get_lovers(self):
        tragic_love_affair = {
            1: "Your lover died in an accident.",
            2: "Your lover mysteriously vanished.",
            3: "It just didn't work out.",
            4: "A personal goal or vendetta came between you and your lover.",
            5: "Your lover was kidnapped.",
            6: "Your lover went insane or cyberpsycho.",
            7: "Your lover committed suicide.",
            8: "Your lover was killed in a fight.",
            9: "A rival cut you out of the action.",
            10: "Your lover is imprisoned or exiled."
        }

        num_lovers = max(0, random.randint(1, 10) - 7)
        for i in range(num_lovers):
            love_tragedy = random.randint(1, 10)
            self.lovers[f'Lover {i+1}'] = tragic_love_affair[love_tragedy]
        return self.lovers
