from cmd import Cmd
import os

class BrawlingShell(Cmd):
    """
    Sub-shell for Brawling Combat.
    """
    intro = "\n\033[1;31m[ COMBAT MODE: BRAWLING ]\033[0m\nType 'help' or '?' to list commands. Type 'back' to exit."
    
    def __init__(self, player, target_name):
        super().__init__()
        self.player = player
        self.target_name = target_name
        self.prompt = f"\033[1;31m(brawling {target_name}) > \033[0m"

    def do_attack(self, arg):
        """Standard brawling attack."""
        print(f"\033[31m[PLACEHOLDER] Reducing teeth count on {self.target_name}...\033[0m")
        return True  # Exit shell after action? Or stay in combat? 
        # User requested: "Ensure it prints the placeholder and returns you to the main game prompt." -> So return True.

    def do_grab(self, arg):
        """Attempt to grapple the target."""
        print(f"\033[33m[COMBAT] Initiating Grapple with {self.target_name}...\033[0m")
        # Launch Grapple Shell
        grapple = GrappleShell(self.player, self.target_name)
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
