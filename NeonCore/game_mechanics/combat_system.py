import random
import sys
import cmd
from typing import List, Optional
from ..utils import wprint
from ..managers.character_manager import Character
from .skill_check import DiceRoller
import sys # ensure sys is imported

# Try to get readline for forcing
try:
    import readline
except ImportError:
    readline = None


from ..core.async_cmd import AsyncCmd

class CombatEncounter(AsyncCmd):
    intro = "\n\033[1;31m[COMBAT INITIATED] CORPO SQUAD AMBUSH!\033[0m\nDirty Cops emerge from the shadows! 'NCPD! Drop the case!'\n"
    prompt = "\033[1;31mCOMBAT > \033[0m"

    def __init__(self, player: Character, enemies: List[Character], io):
        super().__init__(io)
        self.player = player
        self.enemies = enemies
        self.turn_count = 0
        self.cover_bonus = 0  # 0 or 4 (standard cover)
        self.combat_over = False

        # Initialize HP for enemies if not present (Dirty Cops have 'HP: 35' in description but maybe not in object)
        for enemy in self.enemies:
            if not hasattr(enemy, "hp"):
                enemy.hp = 35
            if not hasattr(enemy, "sp"):
                enemy.sp = 7  # Kevlar
            # Ensure enemy has a weapon (Heavy Pistol 3d6)
            if not hasattr(enemy, "weapon_dmg"):
                enemy.weapon_dmg = 4  # 4d6

        # Initialize Player Combat Stats if missing (fallback)
        if "hp" in self.player.combat:
            self.player_hp = int(self.player.combat["hp"])
            self.player_max_hp = self.player_hp
        else:
            self.player_hp = 30  # Default safety
            self.player_max_hp = 30

    def get_names(self):
        """Override to strictly control available commands in Combat Shell."""
        return ["do_shoot", "do_cover", "do_flee", "do_take", "do_look", "do_help", "do_quit"]

    def completenames(self, text, *ignored):
        """Force clean completion list, ignoring parent leakage."""
        dotext = 'do_' + text
        dotext = 'do_' + text
        return [a[3:] + ' ' for a in self.get_names() if a.startswith(dotext)]

    def complete_shoot(self, text, line, begidx, endidx):
        """Complete shoot targets by handle."""
        if not text:
            completions = [e.handle for e in self.enemies]
        else:
            completions = [e.handle for e in self.enemies if e.handle.lower().startswith(text.lower())]
        return completions

    async def do_help(self, arg):
        """Show available combat commands."""
        await self.io.send("\n\033[1;33m[ COMBAT COMMANDS ]\033[0m")
        await self.io.send("  shoot <#>   - Fire at target # (or default).")
        await self.io.send("  cover       - Take cover (+4 DV defense).")
        await self.io.send("  flee        - Attempt to escape (Athletics check).")
        await self.io.send("  take <item> - Equip a weapon from inventory.")
        await self.io.send("  look        - Check situational status.")
        await self.io.send("  quit        - Rage quit (Exit Game).")

    async def do_look(self, arg):
        """Assess the combat situation."""
        await self.display_status()
        if self.cover_bonus > 0:
             await self.io.send(f"\033[1;32m[STATUS] You are in cover (+4 DV).\033[0m")
        else:
             await self.io.send(f"\033[1;31m[STATUS] You are exposed.\033[0m")

    async def do_take(self, arg):
        """Equip an item from inventory."""
        if not arg:
             await self.io.send("Equip what?")
             return
        
        arg_lower = arg.lower()
        found_item = None
        
        for item in self.player.inventory:
            name = item.get('name') if isinstance(item, dict) else item
            if arg_lower in name.lower():
                found_item = item
                break
        
        if found_item:
             self.player.inventory.remove(found_item)
             self.player.weapons.append(found_item)
             name = found_item.get('name', found_item)
             await self.io.send(f"You equip the \033[1m{name}\033[0m.")
        else:
             await self.io.send("You don't have that in your gear.")

    def complete_take(self, text, line, begidx, endidx):
        """Autocomplete for take command (Inventory -> Hand)"""
        if not self.player:
            return []
            
        items = []
        for item in self.player.inventory:
             name = item.get('name') if isinstance(item, dict) else item
             items.append(name)
             
        return [i + " " for i in items if i.lower().startswith(text.lower())]

    async def do_quit(self, arg):
        """Exit the game."""
        await self.io.send("You give up the ghost.")
        return True

    async def start_combat(self):
        """Starts the combat loop."""
        self.turn_count = 1
        await self.io.send(f"\n\033[1;33m--- TURN {self.turn_count} ---\033[0m")
        await self.display_status()
        
        # Force Readline Re-bind if available
        # Check system modules for readline if local import failed (Windows fix)
        rl = None
        if 'readline' in sys.modules:
             rl = sys.modules['readline']
        elif readline:
             rl = readline

        if rl:
             # Force the completer to point to THIS instance's complete method
             rl.set_completer(self.complete)
             rl.parse_and_bind("tab: complete")
             
        await self.cmdloop()
        return (
            "victory"
            if not self.enemies
            else "dead" if self.player_hp <= 0 else "escaped"
        )

    async def display_status(self):
        # Health Bar
        await self.io.send(f"\033[1;36mPLAYER HP: {self.player_hp}/{self.player_max_hp}\033[0m")
        await self.io.send(f"ENEMIES: {len(self.enemies)} active")
        for i, enemy in enumerate(self.enemies):
            await self.io.send(f"  {i+1}. {enemy.handle} (HP: {enemy.hp})")

    async def do_shoot(self, arg):
        """Shoot at an enemy. Usage: shoot [target_number]"""
        target = await self._select_target(arg)
        if not target:
            return

        # Roll to Hit (Reflex + Handgun/Shoulder Arms)
        skill = self.player.skill_total("handgun")
        roll = DiceRoller.d10() + skill
        dv = 15  # Standard DV for medium range

        await self.io.send(f"Firing at {target.handle}... (Rolled {roll} vs DV {dv})")

        if roll >= dv:
            # Hit!
            dmg_roll = sum(random.randint(1, 6) for _ in range(3))  # 3d6 dmg
            final_dmg = max(0, dmg_roll - target.sp)
            target.hp -= final_dmg
            await self.io.send(
                f"\033[1;32m[HIT] You tagged 'em for {final_dmg} dmg! (Armor soaked {target.sp})\033[0m"
            )

            if target.hp <= 0:
                await self.io.send(f"\033[1;33m{target.handle} goes down!\033[0m")
                self.enemies.remove(target)
        else:
            await self.io.send("\033[1;31m[MISS] Shots sparked off the cover!\033[0m")

        self.cover_bonus = 0  # Lost cover if you shoot (simplified mechanic or optional?) - keeping it simple: shooting exposes you slightly but let's say cover lasts 1 turn.
        # Actually standard logic: Action is shoot OR cover. So doing shoot means no cover bonus this turn unless previously established and held?
        # Resetting cover bonus at start of turn is cleaner, but here we set it in do_cover.
        # Let's say Cover action gives bonus for ENEMY turn. Shoot action gives NO bonus.
        self.cover_bonus = 0

    async def do_cover(self, arg):
        """Take cover to increase defense."""
        await self.io.send("You slide behind a concrete barrier. Cover +4 DV to hit you.")
        self.cover_bonus = 4

    async def do_flee(self, arg):
        """Attempt to escape the combat."""
        # Athletics Check vs DV 15
        athletics = self.player.skill_total("athletics")
        roll = DiceRoller.d10() + athletics
        await self.io.send(f"Athletics Check (DV15): Rolled {roll}")

        if roll >= 15:
            await self.io.send(
                "\n\033[1;32m[ESCAPED] You dive into a side alley, losing the squad in the maze of pipes!\033[0m"
            )
            self.combat_over = True
            return True  # Stop loop
        else:
            await self.io.send(
                "\033[1;31m[BLOCKED] You try to run, but they cut you off! You're exposed!\033[0m"
            )
            self.cover_bonus = 0

    async def postcmd(self, stop, line):
        """Run enemy turn after player action."""
        if stop:  # If player escaped or combat ended
            return True

        # FREE ACTIONS: Don't advance turn
        # line is the command line string
        # simple check:
        cmd_name = line.strip().split()[0].lower() if line else ""
        if cmd_name in ["look", "help", "quit"]:
            return False

        # Check Win
        if not self.enemies:
            await self.io.send(
                "\n\033[1;32m[VICTORY] The last corrupt cop falls. The path is clear.\033[0m"
            )
            return True

        # Enemy Turn
        await self._enemy_turn()

        # Check Loss
        if self.player_hp <= 0:
            await self.io.send(
                "\n\033[1;31m[FLATLINED] You take one too many rounds. The city doesn't mourn.\033[0m"
            )
            return True

        # Prepare next turn
        self.turn_count += 1
        await self.io.send(f"\n\033[1;33m--- TURN {self.turn_count} ---\033[0m")
        await self.display_status()
        return False

    async def _enemy_turn(self):
        await self.io.send("\n\033[1;31m[ENEMY TURN]\033[0m")
        for enemy in self.enemies:
            # 50% chance to move closer (flavor) or shoot
            action_roll = random.random()

            if action_roll < 0.2:
                await self.io.send(f"{enemy.handle} shouts orders and advances!")
            else:
                # Shoot
                dv = 15 + self.cover_bonus
                attack_roll = 10 + DiceRoller.d10()
                await self.io.send(f"{enemy.handle} fires! (Rolled {attack_roll} vs DV {dv})")

                if attack_roll >= dv:
                    dmg = sum(
                        random.randint(1, 6) for _ in range(4)
                    )  # 4d6 Heavy Pistol
                    sp = 7  # default fallback SP
                    final_dmg = max(0, dmg - sp)
                    self.player_hp -= final_dmg
                    await self.io.send(
                        f"\033[1;31m[HIT] You took a slug! {final_dmg} dmg taken!\033[0m"
                    )
                else:
                    await self.io.send("Bullets whiz past you!")

    async def _select_target(self, arg):
        if not self.enemies:
            return None
        if len(self.enemies) == 1:
            return self.enemies[0]

        try:
            # Try parsing as index (1-based)
            idx = int(arg.strip()) - 1
            if 0 <= idx < len(self.enemies):
                return self.enemies[idx]
        except ValueError:
            # Try parsing as Name/Handle
            arg_lower = arg.lower().strip()
            for enemy in self.enemies:
                 if arg_lower in enemy.handle.lower():
                      return enemy
            pass

        await self.io.send("Invalid target. Usage: shoot <number>")
        await self.io.send("Targets:")
        for i, enemy in enumerate(self.enemies):
            await self.io.send(f"  {i+1}. {enemy.handle}")
        return None

    async def emptyline(self):
        """Do nothing on empty line"""
        pass

    async def default(self, line):
        await self.io.send("Invalid combat command. Options: shoot, cover, flee")
