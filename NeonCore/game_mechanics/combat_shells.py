from cmd import Cmd
import os
import random

class BrawlingShell(Cmd):
    """
    Sub-shell for Brawling Combat.
    """
    intro = "\n\033[1;31m[ COMBAT MODE: BRAWLING ]\033[0m\nType 'help' or '?' to list commands. Type 'back' to exit."
    
    def __init__(self, player, target):
        super().__init__()
        self.player = player
        self.target = target
        self.prompt = f"\033[1;31m(brawling {target.handle}) > \033[0m"

    def do_attack(self, arg):
        """
        Action: Standard Brawling Attack
        Rule: Rate of Fire (ROF) is 2. 
        Damage: 1d6 per hit.
        Special: Does NOT ignore armor.
        """
        print(f"\033[31mYou launch a flurry of blows at {self.target.handle}!\033[0m")
        
        # Loop twice because Brawling RoF = 2
        for i in range(1, 3):
            print(f"\n--- Attack {i} ---")
            # 1. Skill Check: DEX + Brawling + 1d10
            # Note: roll_check returns a dict with 'result', 'att_total', etc.
            result_data = self.player.roll_check(self.target, "brawling", "evasion")
            
            if result_data["result"] == "success":
                # 2. Damage Roll: 1d6
                dmg = random.randint(1, 6)
                print(f"Damage Roll: {dmg}")
                
                # 3. Apply Damage (Respects Armor)
                self.target.take_damage(dmg, ignore_armor=False)
            else:
                print("MISS!")
        
        # Turn is over, exit the shell
        return True

    def do_grab(self, arg):
        """Attempt to grapple the target."""
        print(f"\033[33m[COMBAT] Initiating Grapple with {self.target.handle}...\033[0m")
        # Launch Grapple Shell
        grapple = GrappleShell(self.player, self.target.handle)
        grapple.cmdloop()
        return True # Exit brawling shell after grapple finishes (or stay? usually grapple ends with throw/release)

    def do_back(self, arg):
        """Exit brawling mode."""
        print("Disengaging combat.")
        return True
    
    def do_quit(self, arg):
        """Exit brawling mode."""
        return self.do_back(arg)

class GrappleShell(Cmd):
    """
    Sub-shell for Grapple state.
    """
    intro = "\n\033[1;33m[ GRAPPLING ]\033[0m"
    
    def __init__(self, player, target_name):
        super().__init__()
        self.player = player
        self.target_name = target_name
        self.prompt = f"\033[1;33m(holding {target_name}) > \033[0m"

    def do_choke(self, arg):
        """Choke the grappled target."""
        print(f"\033[31m[PLACEHOLDER] Choking {self.target_name}...\033[0m")
        # Logic might keep us in shell, but for now dummy placeholders usually imply checking flow. 
        # User didn't specify return behavior for Grapple, but Brawling returns. 
        # I'll let it stay in shell for Grapple until explicitly told otherwise, or return True to be safe for "skeleton" check.
        # Actually, let's keep it consistent: single action then potential state change or exit. 
        # But for skeleton, let's just print and return True to avoid getting stuck if logic isn't there.
        return True

    def do_throw(self, arg):
        """Throw the grappled target."""
        print(f"\033[31m[PLACEHOLDER] Throwing {self.target_name}!\033[0m")
        return True

    def do_back(self, arg):
        """Release grapple."""
        print(f"Releasing {self.target_name}.")
        return True

    def do_quit(self, arg):
        return self.do_back(arg)
