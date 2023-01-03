# Character stats
stats = {
    "INT":   0, #intelligence
    "REF":   0, #reflexes
    "DEX":   0, #dexterity
    "TECH":  0, #technique
    "COOL":  0, #cool
    "WILL":  0, #will
    "LUCK": 20, #luck
    "MOVE":  0, #movement
    "BODY":  0, #body
    "EMP":   0  #empathy
}

# Character skills
skills = {
    "Accounting":               [0, stats["INT"]],
    "Acting":                   [0, stats["COOL"]],
    "Athletics":                [0, stats["DEX"]],
    "Brawling":                 [0, stats["DEX"]],
    "Bribery":                  [0, stats["COOL"]],
    "Bureaucracy":              [0, stats["INT"]],
    "Business":                 [0, stats["INT"]],
    "Composition":              [0, stats["INT"]],
    "Conceal/Reveal Object":    [0, stats["INT"]],
    "Concentration":            [0, stats["WILL"]],
    "Conversation":             [0, stats["EMP"]],
    "Criminology":              [0, stats["INT"]],
    "Cryptography":             [0, stats["INT"]],
    "Deduction":                [0, stats["INT"]],
    "Drive Land Vehicle":       [0, stats["REF"]],
    "Education":                [0, stats["INT"]],
    "Electronics/Security Tech":[0, stats["TECH"]],
    "Evasion":                  [0, stats["DEX"]],
    "First Aid":                [0, stats["TECH"]],
    "Forgery":                  [0, stats["TECH"]],
    "Handgun":                  [0, stats["REF"]],
    "Human Perception":         [0, stats["EMP"]],
    "Interrogation":            [0, stats["COOL"]],
    "Library Search":           [0, stats["INT"]],
    "Local Expert":             [0, stats["INT"]],
    "Melee Weapon":             [0, stats["DEX"]],
    "Paramedic":                [0, stats["TECH"]],
    "Perception":               [0, stats["INT"]],
    "Persuation":               [0, stats["COOL"]],
    "Photography/Film":         [0, stats["TECH"]],
    "Pick Lock":                [0, stats["TECH"]],
    "Pick Pocket":              [0, stats["TECH"]],
    "Play Instrument":          [0, stats["TECH"]],
    "Resist Torture/Drugs":     [0, stats["WILL"]],
    "Shoulder Arms":            [0, stats["REF"]],
    "Stealth":                  [0, stats["DEX"]],
    "Streetwise":               [0, stats["COOL"]],
    "Tactics":                  [0, stats["INT"]],
    "Tracking":                 [0, stats["INT"]],
    "Trading":                  [0, stats["COOL"]],
    "Wardrobe & Style":         [0, stats["COOL"]]
}


class Character:
    def __init__(self):
        self.name = None
        self.stats = None
        self.skills = None

    def set_name(self, name):
        self.name = name
        return self
    
    def set_stats(self, stats):
        self.stats = stats
        return self
    
    def set_skills(self, skills):
        self.skills = skills
        return self
    
   # def take_psychological_damage(self, amount):
   #     self.mental_health -= amount
        
    # def use_skill(self, skill):
     #   if skill in self.skills:
            # code for using the skill goes here
     #       pass
     #   else:
     #       print(f"{self.name} does not have the {skill} skill.")

class NPC(Character):
    def __init__(self):
        super().__init__()
        self.dialogue = None

    def set_dialogue(self, dialogue):
        self.dialogue = dialogue
        return self
        
    def speak(self):
        print(self.dialogue)

class CharacterBuilder:
    def __init__(self):
        self.character = None

    def create_new_character(self):
        self.character = Character()
        return self.character

    def create_new_npc(self):
        self.character = NPC()
        return self.character

# Now we can use the CharacterBuilder to create instances of the Character and NPC classes:
builder = CharacterBuilder()

player = builder.create_new_character().set_name("John").set_stats(stats).set_skills(skills)
#print(player.__dict__)
print(player.name)
player1 = builder.create_new_character().set_name("Jim").set_stats(stats).set_skills(skills)
print(player1.name)
print(player.name)

npc1 = builder.create_new_npc().set_name("Bob").set_stats(stats).set_skills(skills).set_dialogue("Hello, how are you?")
#print(npc1.__dict__)
print(npc1.dialogue)

npc2 = builder.create_new_npc().set_name("Sue").set_stats(stats).set_skills(skills).set_dialogue("Nice to meet you.")
#print(npc2.__dict__)
print(npc2.dialogue)

npc3 = builder.create_new_npc().set_name("Tom").set_stats(stats).set_skills(skills).set_dialogue("How's it going?")
#print(npc3.__dict__)
print(npc3.dialogue)