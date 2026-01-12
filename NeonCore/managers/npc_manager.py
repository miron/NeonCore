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
    # Combat Attributes
    relationships: Dict[str, str] = field(default_factory=dict)
    skills: Dict[str, int] = field(default_factory=dict)
    combat_stats: Dict[str, int] = field(default_factory=lambda: {"hp": 20, "max_hp": 20})
    sp: int = 0
    max_sp: int = 0
    inventory: List[str] = field(default_factory=list)

    @property
    def handle(self):
        return self.name

    def skill_total(self, skill_name):
        return self.skills.get(skill_name, 0)
        
    def roll_check(self, skill_name, def_skill_name=None):
         # Simplistic roll check for NPC (Attacker or Defender)
         # If acting as defender, 'def_skill_name' logic might be handled by caller expecting 
         # this to be 'roll_check(defender, skill, def_skill)' but here we might just need base roll.
         # Wait, Character.roll_check signature is (defender, skill, def_skill).
         # But sometimes we might call npc.roll_check separately?
         # For BrawlingShell: player.roll_check(target, "brawling", "evasion") calls target.skill_total("evasion").
         # So providing skill_total is enough for NPC as DEFENDER.
         # If NPC is ATTACKER, it needs a full roll_check method.
         # For now, let's implement basic skill_total which solves the immediate need.
         pass

    def take_damage(self, amount: int, ignore_armor: bool = False, verbose: bool = True) -> int:
        effective_dmg = amount
        if not ignore_armor:
            if effective_dmg <= self.sp:
                if verbose:
                    print(f"{self.name}'s armor absorbed the hit!")
                return 0
            effective_dmg -= self.sp
        
        self.combat_stats["hp"] -= effective_dmg
        if verbose:
            print(f"{self.name} took {effective_dmg} damage! HP: {self.combat_stats['hp']}")
        return effective_dmg


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
        dirty_cop_stats_block = """
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
            stats_block=dirty_cop_stats_block,
            skills={"handgun": 12, "brawling": 11, "perception": 9, "persuasion": 10, "evasion": 4}, # defaulting evasion to base cool/dex if not listed? Dex is 5. using conservative guess or just brawling/athletics? Added evasion
            combat_stats={"hp": 35, "max_hp": 35},
            sp=7,
            max_sp=7,
            inventory=["Briefcase (Locked)"]
        )
        # Evasion typically uses Evasion skill + DEX. If skill not listed, just Stat?
        # Added evasion: 4 (just a guess to make him fightable)
        
        # We can alias 'dirty_cop' to Lenard for 'look dirty_cop'
        self.npcs["lenard"] = lenard
        self.npcs["dirty_cop"] = lenard

    def get_npc(self, name: str) -> Optional[NPC]:
        return self.npcs.get(name.lower())

    def get_npcs_in_location(self, location: str) -> List[NPC]:
        seen = set()
        unique_npcs = []
        for npc in self.npcs.values():
            if npc.location == location and id(npc) not in seen:
                unique_npcs.append(npc)
                seen.add(id(npc))
        return unique_npcs

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
            # dirty_cop.handle is a property returning name, so no assignment needed
            dirty_cop.hp = 35
            dirty_cop.sp = 7
            dirty_cop.weapon_dmg = 4
            squad.append(dirty_cop)
        return squad
