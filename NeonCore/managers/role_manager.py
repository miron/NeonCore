from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Dict, Any, Optional

@dataclass
class RoleDisplayData:
    name: str
    description: str

class RoleAbility(ABC):
    def __init__(self, rank: int = 4):
        self.rank = rank

    def get_display_data(self) -> RoleDisplayData:
        return RoleDisplayData(name="Generic Role", description="No special abilities.")

    def get_passive_bonuses(self) -> Dict[str, Any]:
        """Return static bonuses like {'initiative': 4}"""
        return {}

    def get_social_context(self, relationship: str) -> str:
        """Return AI context string based on relationship"""
        return ""

class RockerboyAbility(RoleAbility):
    def get_display_data(self) -> RoleDisplayData:
        return RoleDisplayData(
            name="Charismatic Impact",
            description=(
                "You know when someone is a fan and receive a +2 to any EMP or COOL "
                "based Skill Check made against them, including Facedowns. "
                "Use `look` to spot fans. `talk` to influence them."
            )
        )

    def get_social_context(self, relationship: str) -> str:
        if relationship and relationship.lower() == "fan":
            return (
                f"[SYSTEM] TARGET IS A FAN (Charismatic Impact Rank {self.rank}). "
                "They are eager to impress the player. "
                "Player has significant social leverage (+2 equivalent)."
            )
        return ""

class SoloAbility(RoleAbility):
    def get_display_data(self) -> RoleDisplayData:
        return RoleDisplayData(
            name="Combat Awareness",
            description=f"Add +{self.rank} to any Initiative roll you make."
        )

    def get_passive_bonuses(self) -> Dict[str, Any]:
        return {"initiative": self.rank}

class TechAbility(RoleAbility):
    def get_display_data(self) -> RoleDisplayData:
        return RoleDisplayData(
            name="Maker",
            description=f"Field expertise. Your Electronics/Security Tech Skill is boosted by +{self.rank} (already included above)."
        )
    
    def get_passive_bonuses(self) -> Dict[str, Any]:
         return {"electronics_security_tech": self.rank}

class MedtechAbility(RoleAbility):
    def get_display_data(self) -> RoleDisplayData:
        return RoleDisplayData(
            name="Medicine",
            description="You have access to the Surgery Skill (already included above)."
        )

class MediaAbility(RoleAbility):
    def get_display_data(self) -> RoleDisplayData:
        return RoleDisplayData(
            name="Credibility",
            description=(
                "Once per hour, you may roll a 1d10. "
                "If you roll higher than 4, you learn a rumor pertinent to your current situation."
            )
        )

# Placeholders for other core roles to avoid "Generic" fallback
class NomadAbility(RoleAbility):
    def get_display_data(self) -> RoleDisplayData:
        return RoleDisplayData(name="Moto", description="Vehicle expertise and family status.")

class NetrunnerAbility(RoleAbility):
    def get_display_data(self) -> RoleDisplayData:
        return RoleDisplayData(name="Interface", description="Cyberdeck network operations.")

class FixerAbility(RoleAbility):
    def get_display_data(self) -> RoleDisplayData:
        return RoleDisplayData(name="Operator", description="Street deal making and sourcing.")

class LawmanAbility(RoleAbility):
    def get_display_data(self) -> RoleDisplayData:
        return RoleDisplayData(name="Backup", description="Call upon police backup.")

class ExecAbility(RoleAbility):
    def get_display_data(self) -> RoleDisplayData:
        return RoleDisplayData(name="Teamwork", description="Corporate resource management.")

class RoleManager:
    @staticmethod
    def get_ability(role_name: str, rank: int = 4) -> RoleAbility:
        role_map = {
            "Rockerboy": RockerboyAbility,
            "Solo": SoloAbility,
            "Tech": TechAbility,
            "Medtech": MedtechAbility,
            "Media": MediaAbility,
            "Nomad": NomadAbility,
            "Netrunner": NetrunnerAbility,
            "Fixer": FixerAbility,
            "Lawman": LawmanAbility,
            "Exec": ExecAbility
        }
        t = role_map.get(role_name)
        if t:
            return t(rank)
        # Fallback for undefined roles
        return RoleAbility(rank)
