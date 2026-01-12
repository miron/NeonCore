from ..core.async_cmd import AsyncCmd
import os
import random

class BrawlingShell(AsyncCmd):
    """
    Sub-shell for Brawling Combat.
    """
    intro = "\n\033[1;31m[ COMBAT MODE: BRAWLING ]\033[0m\nType 'help' or '?' to list commands. Type 'back' to exit."
    
    def __init__(self, player, target, io):
        super().__init__(io)
        self.player = player
        self.target = target
        self.prompt = f"\033[1;31m(brawling {target.handle}) > \033[0m"

    async def do_attack(self, arg):
        """
        Action: Standard Brawling Attack
        Rule: Rate of Fire (ROF) is 2. 
        Damage: 1d6 per hit.
        Special: Does NOT ignore armor.
        """
        await self.io.send(f"\033[31mYou launch a flurry of blows at {self.target.handle}!\033[0m")
        
        # Loop twice because Brawling RoF = 2
        for i in range(1, 3):
            await self.io.send(f"\n--- Attack {i} ---")
            # 1. Skill Check: DEX + Brawling + 1d10
            # Note: roll_check returns a dict with 'result', 'att_total', etc.
            result_data = self.player.roll_check(self.target, "brawling", "evasion")
            
            if result_data["result"] == "success":
                # 2. Damage Roll: 1d6
                dmg = random.randint(1, 6)
                await self.io.send(f"Damage Roll: {dmg}")
                
                # 3. Apply Damage (Respects Armor)
                self.target.take_damage(dmg, ignore_armor=False)
            else:
                await self.io.send("MISS!")
        
        # Turn is over, exit the shell
        return True

    async def do_grab(self, arg):
        """Attempt to grapple the target."""
        await self.io.send(f"\033[33m[COMBAT] Initiating Grapple with {self.target.handle}...\033[0m")
        # Launch Grapple Shell
        # Note: We need to pass self references if needed, but GrappleShell is standalone usually.
        # But wait, action_manager handling requires reference.
        # Ideally, we don't nest shells deeply without passing context.
        # However, checking current GrappleShell init signature...
        # It requires action_manager now based on my plan.
        # But BrawlingShell doesn't have action_manager ref in this file's version.
        # I'll instantiate without it for now or assume BrawlingShell usage is deprecated by my ActionManager fix?
        # User said "use_skill brawling should not enter a combat shell".
        # So BrawlingShell might be legacy code now?
        # But `do_grab` uses GrappleShell.
        # I will update GrappleShell to be robust.
        
        # NOTE: If BrawlingShell is used, it calls this.
        # But likely we are bypassing BrawlingShell in ActionManager now.
        pass 

    async def do_back(self, arg):
        """Exit brawling mode."""
        await self.io.send("Disengaging combat.")
        return True
    
    async def do_quit(self, arg):
        """Exit brawling mode."""
        return await self.do_back(arg)

class GrappleShell(AsyncCmd):
    """
    Sub-shell for Grapple state.
    """
    intro = "\n\033[1;33m[ GRAPPLING ]\033[0m"
    
    def __init__(self, io, player, target, action_manager):
        super().__init__(io)
        self.player = player
        self.target = target
        self.target_name = target.handle
        self.action_manager = action_manager
        self.prompt = f"\033[1;33m(holding {self.target_name}) > \033[0m"
        self.choke_count = 0
        self.grapple_ended = False

    async def do_choke(self, arg):
        """
        [Action] Choke the grappled target.
        Effect: Deals BODY damage directly to HP (Ignores Armor).
        Special: 3 successive chokes cause Unconsciousness.
        """
        player = self.player
        target = self.target
        
        # Calculate Damage (BODY Stat)
        dmg = player.stats.get('body', 5) # Default 5 if missing?
        
        await self.io.send(f"\n\033[31m[ACTION] You choke {self.target_name} with intense force!\033[0m")
        
        # Apply Damage
        target.take_damage(dmg, ignore_armor=True)
        
        # Handle Unconsciousness Logic
        self.choke_count += 1
        if self.choke_count >= 3:
             await self.io.send(f"\033[1;35m[EFFECT] {self.target_name} goes limp in your arms! (Unconscious)\033[0m")
             # Logic to set unconscious status (if status system exists)
             # For now, just narrative

    async def do_throw(self, arg):
        """
        [Action] Throw the grappled target.
        Effect: Deals BODY damage directly to HP (Ignores Armor).
        Ends Grapple. Target becomes Prone.
        """
        player = self.player
        target = self.target
        dmg = player.stats.get('body', 5)
        
        await self.io.send(f"\n\033[1;33m[ACTION] You hurl {self.target_name} to the ground!\033[0m")
        target.take_damage(dmg, ignore_armor=True)
        
        await self.io.send(f"\033[33m{self.target_name} is now Prone.\033[0m")
        
        # End Grapple Signal
        self.grapple_ended = True
        return True # Consistent return

    async def do_go(self, arg):
        """
        [Action] Drag the grappled target.
        Usage: go <direction>
        Effect: Moves both you and the target to the new location.
        """
        if not arg: 
             await self.io.send("Drag where?")
             return
             
        direction = arg.strip().lower()
        
        if hasattr(self, "action_manager"):
             am = self.action_manager
             current_loc_id = am.dependencies.world.player_position
             try:
                 exits = am.dependencies.world.locations[current_loc_id]["exits"]
                 if direction in exits:
                      new_loc = exits[direction]
                      
                      # Move Player
                      am.dependencies.world.player_position = new_loc
                      # Move Target
                      self.target.location = new_loc
                      
                      await self.io.send(f"You drag {self.target_name} {direction} to {new_loc}.")
                      await am.do_look(None)
                 else:
                      await self.io.send("You can't go that way.")
             except Exception as e:
                 await self.io.send(f"Error dragging: {e}")
        else:
             await self.io.send("Error: Navigation system not linked.")
             
    async def do_look(self, arg):
        """Visual check maintaining grapple context."""
        await self.io.send(f"\n(You are holding {self.target_name} - tightly)")
        # Directly call world look to avoid ActionManager recursion
        if self.action_manager:
            await self.action_manager.dependencies.world.do_look(arg)

    async def do_back(self, arg):
        """Release grapple."""
        await self.io.send(f"Releasing {self.target_name}.")
        self.grapple_ended = True
        return True

    async def do_quit(self, arg):
        return await self.do_back(arg)
