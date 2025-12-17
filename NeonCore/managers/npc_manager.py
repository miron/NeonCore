from dataclasses import dataclass, field
from typing import List, Dict, Optional


@dataclass
class NPC:
    name: str
    role: str
    location: str
    description: str
    dialogue_context: str = ""
    stats_block: str = ""


class NPCManager:
    def __init__(self):
        self.npcs: Dict[str, NPC] = {}
        self._initialize_story_npcs()

    def _initialize_story_npcs(self):
        """Seed the game with initial story NPCs"""
        # Lazlo - The Fixer from 'Getting Paid'
        lazlo = NPC(
            name="Lazlo",
            role="Fixer",
            location="industrial_zone",
            description="A middle-aged Fixer with a cybernetic eye and a nervous twitch. He looks uncharacteristically rattled.",
            dialogue_context="Lazlo is currently being held hostage by dirty cops in the Heywood Industrial Zone. He is desperate but trying to maintain his cool.",
        )
        self.npcs["lazlo"] = lazlo

        # Dirty Cop (Undercover) - Lenard Houston
        dirty_cop_stats = """
        [ DIRTY COP STATS ]
        INT 3 | REF 6 | DEX 5 | TECH 2 | COOL 4
        WILL 4| LUCK -| MOVE 4| BODY 6 | EMP 3
        HP: 35 | SP: 7 (Kevlar)
        Weapons: Very Heavy Pistol (4d6)
        Skills: Handgun 12, Brawling 11, Perception 9, Persuasion 10
        """
        lenard = NPC(
            name="Lenard",
            role="Dirty Cop",
            location="industrial_zone",
            description="A hooded man in dark clothes. He keeps looking over his shoulder.",
            dialogue_context="Undercover cop posing as a contact. Holding a briefcase. Nervous.",
            stats_block=dirty_cop_stats,
        )
        # We can alias 'dirty_cop' to Lenard for 'look dirty_cop'
        self.npcs["lenard"] = lenard
        self.npcs["dirty_cop"] = lenard

    def get_npc(self, name: str) -> Optional[NPC]:
        return self.npcs.get(name.lower())

    def get_npcs_in_location(self, location: str) -> List[NPC]:
        return [npc for npc in self.npcs.values() if npc.location == location]

    def create_dirty_cop_squad(self, count=3) -> list:
        """Spawn a squad of dirty cops for combat"""
        squad = []
        for i in range(count):
            # Create an object that looks like a Character but for combat
            dirty_cop = NPC(
                name=f"Dirty Cop #{i+1}",
                role="Solo",
                location="combat",
                description="Corrupt NCPD officer.",
                # handle argument removed as it's not in dataclass
            )
            # Inject combat stats/attributes directly
            dirty_cop.handle = dirty_cop.name
            dirty_cop.hp = 35
            dirty_cop.sp = 7
            dirty_cop.weapon_dmg = 4
            squad.append(dirty_cop)
        return squad
