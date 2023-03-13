from __future__ import annotations
import random
from ..utils import wprint


class DiceRoller:
    @staticmethod 
    def d6(num_of_dice: int) -> int:
        """Return the sum of rolls of specified number of d6 dice."""
        return sum(random.randint(1, 6) for _ in range(num_of_dice))

    @staticmethod
    def d10() -> int:
        """Return the sum of rolls of specified number of d6 dice."""
        return random.randint(1, 10)


class Singleton:
    _singletons = {}
    def __new__(cls, *args, **kwds):
        if cls not in cls._singletons:
            cls._singletons[cls] = obj = super().__new__(cls)
            obj._initialized = False
        return cls._singletons[cls]


class SkillCheckCommand(Singleton):
    """Attacker vs Defender
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
    def __init__(
        self,
        player: Character=None,
        npc=None
    ):
        if not self._initialized:
            self.player = player
            self.npc = npc
            self._skillchecks: list[SkillCheckCommand] = []
            self._initialized = True

    def register(self, skillcheck): 
        self._skillchecks.append(skillcheck)
    
    def execute(self, skillcheck):
        [s.check_skill() for s in self._skillchecks if 
            isinstance(s, HumanPerceptionCheckCommand)]
        [s.check_skill(
            "brawling", 
            self.npc.skill_total('brawling'), 
            self.player) for s in self._skillchecks if 
                isinstance(s, SkillCheckCommand)]

    def set_difficulty(self, difficulty_level: str) -> int:
        """
        Returns the difficulty value for the specified difficulty level.
        """
        difficulties = {
                'Simple': 9,
                'Everyday': 13,
                'Difficult': 15,
                'Professional': 17,
                'Heroic': 21,
                'Incredible': 24,
                'Legendary': 29
        }
        if difficulty_level in difficulties:
            return difficulties[difficulty_level]
        else:
            raise ValueError(f"Unknown difficulty level: {difficulty_level}")

    def check_skill(self, 
                    skill_name: str, 
                    skill_or_difficulty_value: int,
                    player: Character) -> int:
        """Perform a skill check using a specified skill and difficulty
           level.

           Args:
           luck_points (int): The number of luck points to use for the
           check.
        """
        while True:
            luck_points = int(
                input(
                      f'Use LUCK {player.lucky_pool}'
                      f'/{player.stats["luck"]} '
                      )
            )
            if luck_points > player.lucky_pool:
                print("Not enough luck points!")
            else:
                player.lucky_pool -= luck_points
                print(f"Lucky Pool: {player.lucky_pool}")
                break
        d10_roll = DiceRoller.d10()
        skill_check_total = (player.skill_total(skill_name)
                             + d10_roll + luck_points)
        if d10_roll == 10:
            print("Critical Success! Rolling another one")
            skill_check_total += DiceRoller.d10()
        elif d10_roll == 1:
            print("Critical Failure! Rolling another one")
            skill_check_total -= DiceRoller.d10() 
        if skill_check_total > skill_or_difficulty_value:
            print(f"Success! Attacker roll: {skill_check_total}, "
                  f"Defender DV: {skill_or_difficulty_value}")
        elif skill_check_total < skill_or_difficulty_value:
            print(f"Failure! Attacker roll: {skill_check_total}, "
                  f"Defender DV: {skill_or_difficulty_value}")
        else:
            wprint(f"Tie! Attacker roll: {skill_check_total}, "
                   f"Defender DV: {skill_or_difficulty_value}")
            print("Attacker loses.")
        return skill_check_total

    def do_use_skill(self, skill_name: str) -> None:
        skill_commands: dict[str, type[Command]] = {
            "human_perception": HumanPerceptionCheckCommand,
            "brawling": SkillCheckCommand,
        }
        if skill_name not in self.char_mngr.player.get_skills():
            print("invalid skill name.")
            return
        command_class = skill_commands.get(skill_name)
        if command_class is not None:
            skcc = SkillCheckCommand()
            command = command_class(self.char_mngr.player)
            skcc.register(command) 
            skcc.execute(command)
        
    def complete_use_skill(self, text, line, begidx, endidx):
        skills = self.char_mngr.player.get_skills()
        return [skill for skill in skills if skill.startswith(text)]


class HumanPerceptionCheckCommand(SkillCheckCommand):
    def check_difficulty(self, task):
        if task == "lazlo":
            return self.set_difficulty("Professional")
        elif task == "spotting a hidden object":
            return self.set_difficulty("Difficult")
        elif task == "detecting a lie":
            return self.set_difficulty("Professional")

    # TODO: Move prints to story, use superclass template where applicable
    def check_skill(self):
        difficulty_value = self.check_difficulty("lazlo")
        human_perception = super().check_skill(
            'human_perception', difficulty_value, self.player)
        if human_perception > difficulty_value:
            wprint("Yo, you're suspecting something's off. You're right, "
                   "Lazlo's being held at gunpoint and is being forced to "
                   "lure you into a trap.")
        else:
            print("You didn't suspect anything unusual with the phone call.")
        print("Lazlo hangs up before you can ask any more questions.")


class NPCEncounterCommand(SkillCheckCommand):
    """Class for handling NPC encounters."""
    def do_encounter(self, arg):
        """Handles the NPC encounter"""
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
        """Handles an NPC attack."""
        self.perform_check('brawling', 'Professional', 0)

    def handle_npc_negotiation(self):
        """Handles negotiating with an NPC."""
        self.perform_check('negotiation', 'Average', 0)

    def handle_npc_escape(self):
        """Handles escaping from an NPC."""
        self.perform_check('athletics', 'Easy', 0)

    def get_random_npc(self):
        """Returns a random NPC."""

    def do_encounter_npc(self, arg):
        """Encounter an NPC and assign the selected NPC
           to self.current_npc
        """
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
                else:
                    print("Invalid choice. Please choose a number between 1 and",
                    len(self.npcs))
            except ValueError:
                print("Invalid input. Please enter a number.")


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
        d10_roll = DiceRoller.d10()
        # add the roll to the total skill level and luck points
        skill_check_total = (self.character.skill_total("ranged_combat")
                             + d10_roll + luck_points)
        if d10_roll == 10:
            print("Critical Success! Rolling another one")
            # generate another random number from 1 to 10
            skill_check_total += DiceRoller.d10()

