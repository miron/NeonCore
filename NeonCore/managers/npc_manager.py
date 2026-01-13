from typing import List, Optional
import copy
from .character import Character

class NPCManager:
    def __init__(self, char_mngr):
        self.char_mngr = char_mngr
        # We no longer store npcs locally; we use char_mngr as the source of truth

    def get_npc(self, name: str) -> Optional[Character]:
        return self.char_mngr.get_npc(name)

    def get_npcs_in_location(self, location: str) -> List[Character]:
        """Return list of NPCs in a specific location string."""
        # Using char_mngr.npcs which is a list of Character objects
        return [
            npc for npc in self.char_mngr.npcs 
            if getattr(npc, 'location', '') == location
        ]

    def create_dirty_cop_squad(self, count=3) -> List[Character]:
        """Spawn a squad of dirty cops for combat by cloning the template"""
        # Find template
        template = self.get_npc("Lenard") or self.get_npc("Dirty Cop")
        if not template:
            # Fallback (Should not happen if npcs.json is correct)
            return []

        squad = []
        for i in range(count):
            # Deep copy to ensure unique HP/Stats state
            cop = copy.deepcopy(template)
            cop.handle = f"Dirty Cop #{i+1}"
            cop.char_id = f"cop_{i}" # distinct ID
            cop.dialogue_context = "One of the squad."
            squad.append(cop)
            
        return squad
