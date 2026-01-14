from ..managers.story_manager import Story
import asyncio
import uuid
from ..game_mechanics.combat_system import CombatEncounter
from ..managers.character import Character

class HeywoodAmbush(Story):
    def __init__(self):
        super().__init__("heywood_ambush")
        self.state = "start"

    async def start(self, game_context):
        """
        Called when the story begins (likely after Phone Call ends).
        We wait for the player to travel to the location.
        """
        self.state = "waiting_for_arrival"
        
        # Move Lenard to location immediately (He is waiting for you)
        lenard = game_context.npc_manager.get_npc("Lenard")
        if lenard:
            lenard.location = "heywood_alley"
            
        # Immediate check in case we are already there (e.g. arrived via move)
        await self.update(game_context)

    async def update(self, game_context):
        world = game_context.world
        player = game_context.char_mngr.player

        if not player:
            return

        # Trigger 1: Arriving at Heywood Alley
        if self.state == "waiting_for_arrival":
            if world.player_position == "heywood_alley":
                self.state = "scene_start"
                await self._run_intro_scene(game_context)
                
        # Trigger 2: Scene Interaction flow
        # This could be handled by do_say hooks if we wire them up, 
        # but for now we might simple push the narrative after the intro.

    async def _run_intro_scene(self, game_context):
        io = game_context.io
        world = game_context.world
        
        # Signal that we are handling the output
        game_context.story_manager.scene_triggered = True
        
        # 1. Show Room Description (With Lenard visible)
        await world.do_look("")
        
        # 2. Show Scene Intro
        await io.send("\n\033[1;33m[SCENE START]\033[0m")
        await io.send("The alley is tight. Steam vents hiss above you.")
        await io.send("Ahead, Lenard stands nervously. He clutches a briefcase to his chest.")
        


        await asyncio.sleep(1)
        await io.send("\n\033[1;36mLENARD:\033[0m \"Did... did anyone follow you?\"")
        await io.send("(He looks past you, eyes darting to the shadows.)")
        
        self.state = "negotiation"

    async def handle_say(self, game_context, message):
        """
        Called by ActionManager.do_say if story is active.
        """
        if self.state == "negotiation":
            await game_context.io.send(f"\n\033[1;36mLENARD:\033[0m \"Just take it. Lazlo said give it to you.\"")
            await game_context.io.send("(He fumbles with a key card attached to his wrist.)")
            await asyncio.sleep(1)
            await game_context.io.send("\033[1;31m*CLATTER*\033[0m")
            await game_context.io.send("The briefcase hits the wet pavement.")
            
            await self._trigger_ambush(game_context)
            return True
        return False

    async def _trigger_ambush(self, game_context):
        io = game_context.io
        world = game_context.world
        db = world.db
        
        self.state = "ambush"
        await asyncio.sleep(1)
        
        await io.send("\n\033[1;31m\"DROP IT! NCPD!\"\033[0m")
        await io.send("Identify Friend Foe overlay flashes: \033[1;31mHOSTILE DETECTED\033[0m.")
        
        # Spawn Dirty Cop
        cop_handle = "Dirty Cop"
        # Check if he's already there (from npcs.json)
        # If not, spawn him at 'heywood_alley'
        # Assuming he is there from previous steps.
        
        await io.send("A figure steps out from behind a pile of crates. Lawman uniform. Badge taped over.")
        await io.send("It's a setup.")
        
        # --- AMBUSH LOGIC ---
        # 1. Identify Enemies
        enemies = []
        
        # Lenard (He is part of the ambush now?)
        # Rules imply he is one of the enemies? "Dirty cops equal to PCs + 2, including Lenard".
        # Yes, Lenard betrays you.
        lenard = game_context.npc_manager.get_npc("Lenard")
        if lenard:
             enemies.append(lenard)
        
        # 2. Spawn Dirty Cops (2 more)
        for i in range(1, 3):
            cop = Character(
                char_id=uuid.uuid4(),
                handle=f"Dirty Cop {i}",
                role="Lawman",
                stats={"ref": 8, "dex": 6, "body": 6, "luck": 0},
                combat={"hp": 35},
                skills={"handgun": {"stat": "ref", "lvl": 6}, "evasion": {"stat": "dex", "lvl": 4}},
                defence={"sp": 7},
                weapons=[{"name": "Heavy Pistol", "dmg": "4d6"}],
                cyberware=[],
                gear=[],
                ascii_art="No Art"
            )
            # Add implicit weapon damage attribute used by CombatSystem fallback
            cop.weapon_dmg = 4 
            enemies.append(cop)
            
        # 3. Start Combat
        player = game_context.char_mngr.player
        combat_encounter = CombatEncounter(player, enemies, io)
        
        # Transfer control to Combat Shell
        await combat_encounter.start_combat()
        
        # 4. Handle Outcome
        if combat_encounter.combat_over: # Escaped
             self.state = "escaped"
        elif not enemies: # Victory
             self.state = "victory"
             await io.send("\n\033[1;32m[SCENE END] The alley is silent. You survived the setup.\033[0m")
        elif player.combat["hp"] <= 0:
             self.state = "dead"
             # Game Over logic handled largely by combat shell print, but we could enforce it here.

    async def end(self, game_context):
        pass
