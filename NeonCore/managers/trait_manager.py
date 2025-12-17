import json
from dataclasses import dataclass, field
from typing import Dict, List, Optional


@dataclass
class Big5Traits:
    openness: int = 50
    conscientiousness: int = 50
    extraversion: int = 50
    agreeableness: int = 50
    neuroticism: int = 50


@dataclass
class DigitalSoul:
    big5: Big5Traits = field(default_factory=Big5Traits)
    skills: Dict[str, str] = field(default_factory=dict)
    traits: List[str] = field(default_factory=list)
    memories: List[str] = field(default_factory=list)
    recent_events: List[str] = field(default_factory=list)  # Buffer for Reflection
    stress: int = 0  # 0-100, where 100 is psychotic break

    def to_dict(self):
        return {
            "big5": self.big5.__dict__,
            "skills": self.skills,
            "traits": self.traits,
            "memories": self.memories,
            "recent_events": self.recent_events,
            "stress": self.stress,
        }

    @classmethod
    def from_dict(cls, data):
        soul = cls()
        if "big5" in data:
            soul.big5 = Big5Traits(**data["big5"])
        soul.skills = data.get("skills", {})
        soul.traits = data.get("traits", [])
        soul.memories = data.get("memories", [])
        soul.recent_events = data.get("recent_events", [])
        soul.stress = data.get("stress", 0)
        return soul


class TraitManager:
    def __init__(self):
        pass

    def generate_random_soul(self) -> DigitalSoul:
        # Placeholder for random generation or Gemini generation
        import random

        return DigitalSoul(
            big5=Big5Traits(
                openness=random.randint(1, 100),
                conscientiousness=random.randint(1, 100),
                extraversion=random.randint(1, 100),
                agreeableness=random.randint(1, 100),
                neuroticism=random.randint(1, 100),
            ),
            skills={},  # Tabula Rasa: You learn by doing
            traits=[],  # Tabula Rasa: You develop traits by Reflecting
        )
