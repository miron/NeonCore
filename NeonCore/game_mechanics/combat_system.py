
import random
import sys
import cmd
from typing import List, Optional
from ..utils import wprint
from ..managers.character_manager import Character
from .skill_check import DiceRoller

class CombatEncounter(cmd.Cmd):
    intro = "\n\033[1;31m[COMBAT INITIATED] CORPO SQUAD AMBUSH!\033[0m\nDirty Cops emerge from the shadows! 'NCPD! Drop the case!'\n"
    prompt = "\033[1;31mCOMBAT > \033[0m"

    def __init__(self, player: Character, enemies: List[Character]):
        super().__init__()
        self.player = player
        self.enemies = enemies
        self.turn_count = 0
        self.cover_bonus = 0  # 0 or 4 (standard cover)
        self.combat_over = False

        # Initialize HP for enemies if not present (Dirty Cops have 'HP: 35' in description but maybe not in object)
        for enemy in self.enemies:
            if not hasattr(enemy, 'hp'):
                enemy.hp = 35
            if not hasattr(enemy, 'sp'):
                enemy.sp = 7 # Kevlar
            # Ensure enemy has a weapon (Heavy Pistol 3d6)
            if not hasattr(enemy, 'weapon_dmg'):
                enemy.weapon_dmg = 4 # 4d6
                
        # Initialize Player Combat Stats if missing (fallback)
        if 'hp' in self.player.combat:
             self.player_hp = int(self.player.combat['hp'])
             self.player_max_hp = self.player_hp
        else:
             self.player_hp = 30 # Default safety
             self.player_max_hp = 30

    def start_combat(self):
        """Starts the combat loop."""
        self.turn_count = 1
        print(f"\n\033[1;33m--- TURN {self.turn_count} ---\033[0m")
        self.display_status()
        self.cmdloop()
        return "victory" if not self.enemies else "dead" if self.player_hp <= 0 else "escaped"

    def display_status(self):
        # Health Bar
        print(f"\033[1;36mPLAYER HP: {self.player_hp}/{self.player_max_hp}\033[0m")
        print(f"ENEMIES: {len(self.enemies)} active")
        for i, enemy in enumerate(self.enemies):
            print(f"  {i+1}. {enemy.handle} (HP: {enemy.hp})")

    def do_shoot(self, arg):
        """Shoot at an enemy. Usage: shoot [target_number]"""
        target = self._select_target(arg)
        if not target:
            return

        # Roll to Hit (Reflex + Handgun/Shoulder Arms)
        skill = self.player.skill_total("handgun")
        roll = DiceRoller.d10() + skill
        dv = 15 # Standard DV for medium range
        
        print(f"Firing at {target.handle}... (Rolled {roll} vs DV {dv})")
        
        if roll >= dv:
            # Hit!
            dmg_roll = sum(random.randint(1, 6) for _ in range(3)) # 3d6 dmg
            final_dmg = max(0, dmg_roll - target.sp)
            target.hp -= final_dmg
            print(f"\033[1;32m[HIT] You tagged 'em for {final_dmg} dmg! (Armor soaked {target.sp})\033[0m")
            
            if target.hp <= 0:
                print(f"\033[1;33m{target.handle} goes down!\033[0m")
                self.enemies.remove(target)
        else:
            print("\033[1;31m[MISS] Shots sparked off the cover!\033[0m")
            
        self.cover_bonus = 0 # Lost cover if you shoot (simplified mechanic or optional?) - keeping it simple: shooting exposes you slightly but let's say cover lasts 1 turn.
        # Actually standard logic: Action is shoot OR cover. So doing shoot means no cover bonus this turn unless previously established and held? 
        # Resetting cover bonus at start of turn is cleaner, but here we set it in do_cover.
        # Let's say Cover action gives bonus for ENEMY turn. Shoot action gives NO bonus.
        self.cover_bonus = 0 

    def do_cover(self, arg):
        """Take cover to increase defense."""
        wprint("You slide behind a concrete barrier. Cover +4 DV to hit you.")
        self.cover_bonus = 4

    def do_flee(self, arg):
        """Attempt to escape the combat."""
        # Athletics Check vs DV 15
        athletics = self.player.skill_total("athletics")
        roll = DiceRoller.d10() + athletics
        print(f"Athletics Check (DV15): Rolled {roll}")
        
        if roll >= 15:
            wprint("\n\033[1;32m[ESCAPED] You dive into a side alley, losing the squad in the maze of pipes!\033[0m")
            self.combat_over = True
            return True # Stop loop
        else:
            wprint("\033[1;31m[BLOCKED] You try to run, but they cut you off! You're exposed!\033[0m")
            self.cover_bonus = 0

    def postcmd(self, stop, line):
        """Run enemy turn after player action."""
        if stop: # If player escaped or combat ended
            return True

        # Check Win
        if not self.enemies:
            wprint("\n\033[1;32m[VICTORY] The last corrupt cop falls. The path is clear.\033[0m")
            return True

        # Enemy Turn
        self._enemy_turn()

        # Check Loss
        if self.player_hp <= 0:
            wprint("\n\033[1;31m[FLATLINED] You take one too many rounds. The city doesn't mourn.\033[0m")
            return True
            
        # Prepare next turn
        self.turn_count += 1
        print(f"\n\033[1;33m--- TURN {self.turn_count} ---\033[0m")
        self.display_status()
        return False

    def _enemy_turn(self):
        wprint("\n\033[1;31m[ENEMY TURN]\033[0m")
        for enemy in self.enemies:
            # 50% chance to move closer (flavor) or shoot
            action_roll = random.random()
            
            if action_roll < 0.2:
                print(f"{enemy.handle} shouts orders and advances!")
            else:
                # Shoot
                dv = 15 + self.cover_bonus
                attack_roll = 10 + DiceRoller.d10()
                print(f"{enemy.handle} fires! (Rolled {attack_roll} vs DV {dv})")
                
                if attack_roll >= dv:
                    dmg = sum(random.randint(1, 6) for _ in range(4)) # 4d6 Heavy Pistol
                    sp = 7 # default fallback SP
                    final_dmg = max(0, dmg - sp)
                    self.player_hp -= final_dmg
                    print(f"\033[1;31m[HIT] You took a slug! {final_dmg} dmg taken!\033[0m")
                else:
                    print("Bulleted whiz past you!")

    def _select_target(self, arg):
        if not self.enemies:
            return None
        if len(self.enemies) == 1:
            return self.enemies[0]
        
        try:
            idx = int(arg.strip()) - 1
            if 0 <= idx < len(self.enemies):
                return self.enemies[idx]
        except ValueError:
            pass
        
        print("Invalid target. Usage: shoot <number>")
        print("Targets:")
        for i, enemy in enumerate(self.enemies):
            print(f"  {i+1}. {enemy.handle}")
        return None

    def emptyline(self):
        """Do nothing on empty line"""
        pass
    
    def default(self, line):
        print("Invalid combat command. Options: shoot, cover, flee")

