import random
from ..utils.utils import wprint
from abc import ABC, abstractmethod


class Command(ABC):
    @abstractmethod
    def execute(self):
        pass


class SkillCheckCommand(Command):
    """
    Attacker vs Defender
    Trying Again:
      only if chances of success have improved

      - you took longer
      - used better tool
      - you or friends made Complementary Skill Check
    Complementary Skill Check
      Single +1 bonus for subsequent similar skill
    Taking Extra Time
      Single +1 bonus when taking four times longer
    """
    def __init__(self, character):
        self.character = character
    
    def set_difficulty(self, difficulty_level: str) -> int:
        """
        Returns the difficulty value for the specified difficulty level.
        """
        # Determine the difficulty value according to the task at hand
        # and return the value
        if difficulty_level == 'Everyday':
            return 13
        elif difficulty_level == 'Diffucult':
            return 15
        elif difficulty_level == 'Professional':
            return 17
        elif difficulty_level == 'Heroic':
            return 21
        elif difficulty_level == 'Incredible':
            return 24

    def execute(self, skill_name: str, difficulty_level: str) -> None:
        """
        Perform a skill check using a specified skill and difficulty
        level.

        Args:
        luck_points (int): The number of luck points to use for the
        check.
        """
        while True:
            luck_points = int(
                input(
                      f'Use LUCK {self.character.lucky_pool}'
                      f'/{self.character.stats["luck"]} '
                      )
            )
            if luck_points > self.character.lucky_pool:
                print("Not enough luck points!")
            else:
                self.character.lucky_pool -= luck_points
                print(f"Lucky Pool: {self.character.lucky_pool}")
                break
        d10_roll = random.randint(1, 10)
        skill_check_total = (self.character.skill_total(skill_name)
                             + d10_roll + luck_points)
        if d10_roll == 10:
            print("Critical Success! Rolling another one")
            skill_check_total += random.randint(1,10)
        elif d10_roll == 1:
            print("Critical Failure! Rolling another one")
            skill_check_total -= random.randint(1,10)
        difficulty_value = self.set_difficulty(difficulty_level)
        if skill_check_total > difficulty_value:
            print(f"Success! Attacker roll: {skill_check_total}, "
                  f"Defender DV: {difficulty_value}")
        elif skill_check_total < difficulty_value:
            print(f"Failure! Attacker roll: {skill_check_total}, "
                  f"Defender DV: {difficulty_value}")
        else:
            wprint(f"Tie! Attacker roll: {skill_check_total}, "
                   f"Defender DV: {difficulty_value}")
            print("Attacker loses.")

    def do_use_skill(self, skill_name):
        if skill_name not in self.character.get_skills():
            wprint("invalid skill name.")
            return
        difficulty_value = self.set_difficulty(skill_name)
        luck_points = self.get_luck_points() 
        skill_command = self.get_skill_command(skill_name)
        skill_command.execute(difficulty_value, luck_points)
        
    #def complete_use_skill(self, text, line, begidx, endidx):
    #    skills = self.character.get_skills()
    #    return [s for s in skills if s.startswith(text)]
    
    def complete_use_skill(self, text, line, begidx, endidx):
        skills = self.player.get_skills()
        return [
                skill for skill in 
                skills if 
                skill.startswith(text)]


class HumanPerceptionCheckCommand(SkillCheckCommand):
    def __init__(self, character):
        super().__init__(character)

    def set_difficulty(self, task):
        if task == "lazlo":
            self.difficulty_level = "Professional"
        elif task == "spotting a hidden object":
            self.difficulty_level = "Difficult"
        elif task == "detecting a lie":
            self.difficulty_level = "Professional"

    def execute(self):
        wprint("Yo chummer, you wanna roll for human perception check? ")
        roll = random.randint(1, 10)
        human_perception = self.characters_manager.get_character_by_id(
            self.character.char_id).skill_total("human_perception")
        difficulty_value = self.set_difficulty("lazlo")
        if roll + human_perception > difficulty_value:
            wprint("Yo, you're suspecting something's off. You're right, "
                   "Lazlo's being held at gunpoint and is being forced to "
                   "lure you into a trap.")
        else:
            print(
                    "You didn't suspect anything unusual with the phone call.")
        print("Alright, play it cool.")
        print("Lazlo hangs up before you can ask any more questions.")


class NPCEncounterCommand(SkillCheckCommand):
    """
    Class for handling NPC encounters. Inherits from SkillCheckCommand
    """
    def __init__(self, character):
        super().__init__(character)
        self.npc = None

    def handle_npc_encounter(self, npc):
        """
        Spends a specified number of luck points on a skill check.

        Parameters:
        luck_points (int): 
        The number of luck points to spend on the skill check.
        """
        self.execute('brawling', 'Professional')

    def do_encounter(self, arg):
        """
        Handles the NPC encounter.
        """
        self.npc = self.get_random_npc()
        print(f"You have encountered an NPC: {self.npc.name}")
        while True:
            action = input(
                "What would you like to do? (attack/negotiate/run): ")
            if action == "attack":
                self.handle_npc_attack()
                break
            elif action == "negotiate":
                self.handle_npc_negotiation()
                break
            elif action == "run":
                self.handle_npc_escape()
                break
            else:
                wprint("Invalid action. Please choose 'attack', 'negotiate', "
                       "or 'run'.")

    def handle_npc_attack(self):
        """
        Handles an NPC attack.
        """
        self.perform_check('brawling', 'Professional', 0)

    def handle_npc_negotiation(self):
        """
        Handles negotiating with an NPC.
        """
        self.perform_check('negotiation', 'Average', 0)

    def handle_npc_escape(self):
        """
        Handles escaping from an NPC.
        """
        self.perform_check('athletics', 'Easy', 0)

    def get_random_npc(self):
        """
        Returns a random NPC.
        """
        # Code for getting a random NPC goes here
        pass

    def do_encounter_npc(self, arg):
        """Encounter an NPC and assign the selected NPC to self.current_npc"""
        print("Select an NPC:")
        for i, npc in enumerate(self.npcs):
            print(f"{i+1}. {npc.handle}")
        while True:
            try:
                npc_index = int(input()) - 1
                if 0 <= npc_index < len(self.npcs):
                    self.current_npc = self.npcs[npc_index]
                    self.skill_check = SkillCheckCommand(self.current_npc)
                    return
            except ValueError:
                pass
            print("Invalid choice. Please choose a number between 0 and",
                  len(self.npcs)-1)



class RangedCombatCommand:
    def __init__(self, character):
        self.character = character
        self.DVs = {
            "pistol": {
                "0-6": 13,
                "7-12": 15,
                "13-25": 20,
                "26-50": 25,
                "51-100": 30,
                "101-200": 30,
                "201-400": None,
                "401-800": None
            },
            "shotgun": {
                "0-6": 13,
                "7-12": 15,
                "13-25": 20,
                "26-50": 25,
                "51-100": 30,
                "101-200": 35,
                "201-400": None,
                "401-800": None
            },
            "assault_rifle": {
                "0-6": 17,
                "7-12": 16,
                "13-25": 15,
                "26-50": 13,
                "51-100": 15,
                "101-200": 20,
                "201-400": 25,
                "401-800": 30
            }
        }

    def get_dv(self, weapon_type, distance):
        distance_range = None
        if distance <= 6:
            distance_range = "0-6"
        elif distance <= 12:
            distance_range = "7-12"
        elif distance <= 25:
            distance_range = "13-25"
        elif distance <= 50:
            distance_range = "26-50"
        elif distance <= 100:
            distance_range = "51-100"
        elif distance <= 200:
            distance_range = "101-200"
        elif distance <= 400:
            distance_range = "201-400"
        elif distance <= 800:
            distance_range = "401-800"
        return self.DVs[weapon_type][distance_range]

    def distance_to_dv(self, weapon, distance):
        """calculate the DV based on the weapon type and distance"""
        for key in self.DVs[weapon]:
            if "-" not in key:
                continue
            min_dist, max_dist = map(int, key.split("-"))
            if min_dist <= distance <= max_dist:
                return self.DVs[weapon][key]
        return None

    def perform_check(self, weapon, distance, luck_points):
        """perform the ranged combat skill check"""
        dv = self.distance_to_dv(weapon, distance)
        if dv is None:
            print(f"Invalid distance for {weapon}")
            return
        # generate a random number from 1 to 10
        d10_roll = random.randint(1, 10)
        # add the roll to the total skill level and luck points
        skill_check_total = (self.character.skill_total("ranged_combat")
                             + d10_roll + luck_points)
        if d10_roll == 10:
            print("Critical Success! Rolling another one")
            # generate another random number from 1 to 10
            skill_check_total += random.randint

