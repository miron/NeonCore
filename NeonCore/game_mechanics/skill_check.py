from __future__ import annotations
import random
from typing import Optional
from ..utils import wprint
from ..managers.character_manager import Character # Type hint only, circular dependency risk handled at runtime

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
    """Attacker vs Defender"""

    def __init__(self, player = None, npc=None):
        if not self._initialized:
            self.player = player
            self.npc = npc
            self.char_mngr = None
            self._skillchecks: list[SkillCheckCommand] = []
            self._initialized = True

    def register(self, skillcheck):
        self._skillchecks.append(skillcheck)

    def execute(self, skillcheck):
        # Special handling for human perception checks
        for s in self._skillchecks:
            if isinstance(s, HumanPerceptionCheckCommand):
                s.check_skill()
                
        # Handle other skill checks only if NPC is available
        if self.npc:
            for s in self._skillchecks:
                if isinstance(s, SkillCheckCommand) and not isinstance(s, HumanPerceptionCheckCommand):
                    # Default brawling check if no specific skill method called
                    # But now we usually call check_skill directly
                    pass
        else:
             pass

    def set_difficulty(self, difficulty_level: str) -> int:
        difficulties = {
            "Simple": 9,
            "Everyday": 13,
            "Difficult": 15,
            "Professional": 17,
            "Heroic": 21,
            "Incredible": 24,
            "Legendary": 29,
        }
        if difficulty_level in difficulties:
            return difficulties[difficulty_level]
        else:
            raise ValueError(f"Unknown difficulty level: {difficulty_level}")

    def check_skill(
        self,
        skill_name: str,
        skill_or_difficulty_value: int,
        player: Character,
    ) -> int:
        """Perform a skill check using a specified skill and difficulty level."""
        luck_points = 0
        if player.lucky_pool > 0:
            while True:
                try:
                    prompt = f"Use LUCK ({player.lucky_pool}/{player.stats['luck']}): "
                    user_in = input(prompt).strip()
                    if not user_in:
                        luck_points = 0
                        break
                    val = int(user_in)
                    if 0 <= val <= player.lucky_pool:
                        luck_points = val
                        player.lucky_pool -= luck_points
                        print(f"Lucky Pool: {player.lucky_pool}")
                        break
                    print("Not enough luck points or invalid amount!")
                except ValueError:
                    print("Please enter a valid number.")
        
        d10_roll = DiceRoller.d10()
        skill_check_total = player.skill_total(skill_name) + d10_roll + luck_points
        if d10_roll == 10:
            print("Critical Success! Rolling another one")
            skill_check_total += DiceRoller.d10()
        elif d10_roll == 1:
            print("Critical Failure! Rolling another one")
            skill_check_total -= DiceRoller.d10()
            
        if skill_check_total > skill_or_difficulty_value:
            print(f"Success! Attacker roll: {skill_check_total}, Defender DV: {skill_or_difficulty_value}")
        elif skill_check_total < skill_or_difficulty_value:
            print(f"Failure! Attacker roll: {skill_check_total}, Defender DV: {skill_or_difficulty_value}")
        else:
            wprint(f"Tie! Attacker roll: {skill_check_total}, Defender DV: {skill_or_difficulty_value}")
            print("Attacker loses.")
        return skill_check_total

    def do_use_skill(self, skill_name, target_name=None) -> Optional[str]:
        skill_commands = {
            "human_perception": HumanPerceptionCheckCommand,
            "brawling": BrawlingCheckCommand,
            "pick_pocket": PickPocketCheckCommand,
        }
        
        if not self.char_mngr or not self.char_mngr.player:
            print("No active character. Please choose a character first.")
            return
            
        if skill_name not in self.char_mngr.player.get_skills():
            print(f"Invalid skill name: {skill_name}")
            print(f"Available skills: {', '.join(self.char_mngr.player.get_skills())}")
            return
            
        command_class = skill_commands.get(skill_name)
        if command_class is not None:
            self._skillchecks = []
            command = command_class(self.char_mngr.player)
            command.char_mngr = self.char_mngr
            self.register(command)
            
            # Direct call for mission logic
            if hasattr(command, 'check_skill') and target_name:
                 try:
                     return command.check_skill(target_name)
                 except TypeError:
                     command.check_skill()
            else:
                 command.check_skill()
        else:
            print(f"No command handler for skill: {skill_name}")
            print(f"Supported skills: {', '.join(skill_commands.keys())}")

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

    def check_skill(self):
        # Prevent repetitive checks
        history_key = "Checked Lazlo Call"
        if getattr(self.player, 'digital_soul', None) and any(history_key in e for e in self.player.digital_soul.recent_events):
             wprint("\nYou scan your surroundings, attempting to catch a vibe. Just the hum of neon and the distant wail of sirens. Nothing out of the ordinary right now.")
             return

        difficulty_value = self.check_difficulty("lazlo")
        human_perception = super().check_skill(
            "human_perception", difficulty_value, self.player
        )
        
        msg = ""
        if human_perception > difficulty_value:
            msg = "Suspects foul play regarding Lazlo."
            wprint(
                "Yo, you're suspecting something's off. You're right, "
                "Lazlo's being held at gunpoint and is being forced to "
                "lure you into a trap."
            )
        else:
            msg = "Missed cues on Lazlo call."
            print("You didn't suspect anything unusual with the phone call.")
        print("Lazlo hangs up before you can ask any more questions.")
        
        if getattr(self.player, 'digital_soul', None):
             self.player.digital_soul.recent_events.append(f"{history_key}: {msg}")


class NPCEncounterCommand(SkillCheckCommand):
    """Class for handling NPC encounters."""

    def do_encounter(self, arg):
        """Handles the NPC encounter"""
        self.npc = self.get_random_npc()
        print(f"You have encountered an NPC: {self.npc.name}")
        while True:
            action = input("What would you like to do? (attack/negotiate/run): ")
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
                wprint("Invalid action. Please choose 'attack', 'negotiate', or 'run'.")

    def handle_npc_attack(self):
        self.perform_check("brawling", "Professional", 0)

    def handle_npc_negotiation(self):
        self.perform_check("negotiation", "Average", 0)

    def handle_npc_escape(self):
        self.perform_check("athletics", "Easy", 0)

    def get_random_npc(self):
        """Returns a random NPC (placeholder)."""
        pass

    def do_encounter_npc(self, arg):
        """Encounter an NPC."""
        pass


class PickPocketCheckCommand(SkillCheckCommand):
    def check_skill(self, target_name):
        # Mission Logic: Briefcase is too big
        if "lenard" in target_name.lower():
            wprint("\nYou slide your hand towards the briefcase... but it's massive. And handcuffed to his wrist.")
            wprint("No way you're lifting that without him noticing. Pick Pocket impossible on this target.")
            return

        # Standard logic
        self.perform_check("pick_pocket", "Difficult", 0)

    def perform_check(self, skill, difficulty, modifier):
        wprint("You don't see anything else worth swiping.")


class BrawlingCheckCommand(SkillCheckCommand):
    def check_skill(self, target_name):
        # Mission Logic: Grab Briefcase
        if "lenard" in target_name.lower():
             print(f"Attempting to grab the briefcase from {target_name}...")
             
             # Difficulty Check
             # Use base skill + d10
             roll = self.player.skill_total("brawling") + DiceRoller.d10()
             dv = 13 # Standard Brawling defense
             
             print(f"Brawling Check (Rolled {roll} vs DV {dv})")
             if roll >= dv:
                 wprint("\n\033[1;32m[SUCCESS] You lunge forward, twisting Lenard's arm and snapping the cord!\033[0m")
                 wprint("The briefcase is yours!")
                 self.char_mngr.player.inventory.append("Briefcase (Locked)")
                 return "ambush_trigger"
             else:
                 wprint("\n\033[1;31m[FAILURE] Lenard jerks back. 'Hey! What gives?!'\033[0m")
                 return "failed"
        
        # Standard brawling
        print("You assume a fighting stance.")


class RangedCombatCommand:
    def __init__(self, character):
        self.character = character
        self.DVs = {
            "pistol": {
                "0-6": 13, "7-12": 15, "13-25": 20, "26-50": 25,
                "51-100": 30, "101-200": 30, "201-400": None, "401-800": None,
            },
            "shotgun": {
                "0-6": 13, "7-12": 15, "13-25": 20, "26-50": 25,
                "51-100": 30, "101-200": 35, "201-400": None, "401-800": None,
            },
            "assault_rifle": {
                "0-6": 17, "7-12": 16, "13-25": 15, "26-50": 13,
                "51-100": 15, "101-200": 20, "201-400": 25, "401-800": 30,
            },
        }

    def get_dv(self, weapon_type, distance):
        distance_range = None
        if distance <= 6: distance_range = "0-6"
        elif distance <= 12: distance_range = "7-12"
        elif distance <= 25: distance_range = "13-25"
        elif distance <= 50: distance_range = "26-50"
        elif distance <= 100: distance_range = "51-100"
        elif distance <= 200: distance_range = "101-200"
        elif distance <= 400: distance_range = "201-400"
        elif distance <= 800: distance_range = "401-800"
        return self.DVs[weapon_type][distance_range]

    def distance_to_dv(self, weapon, distance):
        """calculate the DV based on the weapon type and distance"""
        for key in self.DVs[weapon]:
            if "-" not in key: continue
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
        d10_roll = DiceRoller.d10()
        skill_check_total = (
            self.character.skill_total("ranged_combat") + d10_roll + luck_points
        )
        if d10_roll == 10:
            print("Critical Success! Rolling another one")
            skill_check_total += DiceRoller.d10()
