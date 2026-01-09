import textwrap
from itertools import zip_longest

class ConsoleRenderer:
    """Handles converting structured data into formatted console text."""

    @staticmethod
    def render_character_sheet(data: dict) -> str:
        """Renders the full character sheet."""
        lines = []

        # 1. Header (Box Style)
        # ┌────────────────────────────────────────────────────────┐
        # │ HANDLE: Mover                         ROLE: Solo       │
        # └────────────────────────────────────────────────────────┘
        width = 80
        lines.append(f"┌{'─' * (width - 2)}┐")
        header_content = f" HANDLE: {data['handle']} ({data['role']}) "
        lines.append(f"│{header_content:^{width - 2}}│")
        lines.append(f"└{'─' * (width - 2)}┘")

        # 2. Stats Row (Grid)
        # INT: 7 | REF: 7 | ...
        stats = data.get("stats", {})
        stat_items = [f"{k.upper()}: {v}" for k, v in stats.items()]
        # Group into rows of 4
        rows = [stat_items[i:i + 5] for i in range(0, len(stat_items), 5)] 
        for row in rows:
            line = " | ".join(row)
            lines.append(f" {line} ")
        lines.append("")

        # 3. Main Content: Skills + Art (Side-by-Side)
        skills = data.get("skills", {})
        ascii_art = data.get("ascii_art", "")
        
        # Prepare Skill List
        # Box Width Calculation:
        # │ (1) +   (1) + Name (22) +   (1) + Lvl (2) +   (1) + │ (1) = 29 chars
        # content_width = 29
        # Header: ┌───────── SKILLS ─────────┐ (29 chars)
        # Pad: (29 - 8 ( SKILLS )) / 2 = 10.5 -> 10 and 11 dashes?
        # Let's use 30 chars width for symmetry.
        # │ (1) +   (1) + Name (22) +   (1) + Lvl (2) +   (1) +   (1) + │ (1) = 30? No, just add space to name.
        # Name 23 chars. 
        # │ (1) +   (1) + Name (23) +   (1) + Lvl (2) +   (1) + │ (1) = 30.
        
        skill_col_width = 30
        skill_lines = []
        # Header: ┌ + 10 dashes +  SKILLS  (8) + 10 dashes + ┐ = 1+10+8+10+1 = 30
        skill_lines.append(f"┌{'─'*10} SKILLS {'─'*10}┐")
        for skill, info in skills.items():
            lvl = info.get("lvl", 0)
            if lvl > 0:
                # Name truncated to 23 chars
                skill_lines.append(f"│ {skill[:23]:<23} {lvl:>2} │")
        skill_lines.append(f"└{'─'*(skill_col_width - 2)}┘")

        # Prepare Art Lines
        art_lines = ascii_art.splitlines()

        # Merge Side-by-Side
        lines.append("─" * width)
        for s_line, a_line in zip_longest(skill_lines, art_lines, fillvalue=""):
            # Use exact width of skill box for padding
            s_part = f"{s_line:<{skill_col_width}}" if s_line else " " * skill_col_width
            a_part = a_line if a_line else ""
            lines.append(f" {s_part}   {a_part}")
        lines.append("─" * width)

        # 4. Combat Stats (Simple Table)
        combat = data.get("combat", {})
        lines.append(f" HP: {combat.get('hp')} | Serious: {combat.get('seriously_wounded')} | Death Save: {combat.get('death_save')}")
        lines.append("─" * width)

        # 5. Weapons & Armor 
        lines.append(" [ WEAPONS & ARMOR ]")
        defence = data.get("defence", {})
        lines.append(f" Armor: {defence.get('armor', 'None')} (SP: {defence.get('sp', 0)})")
        
        weapons = data.get("weapons", [])
        if weapons:
             # Header
            lines.append(f" {'Name':<25} {'Dmg':<5} {'Ammo':<5} {'ROF':<3} {'Notes'}")
            for w in weapons:
                name = w.get("name", "Weapon")
                dmg = w.get("dmg", "-")
                ammo = w.get("ammo", "-")
                rof = w.get("rof", "-")
                notes = w.get("notes", "")
                lines.append(f" {name:<25} {dmg:<5} {ammo:<5} {rof:<3} {notes}")
        lines.append("─" * width)

        # 6. Abilities & Cyberware
        # Helper for sections
        def render_section(title, items):
            if not items: return
            lines.append(f" [ {title} ]")
            for item in items:
                if isinstance(item, dict):
                    name = item.get("name", "Unknown")
                    notes = item.get("notes", "")
                    lines.append(f" • {name}")
                    if notes:
                        # Wrap notes with indentation
                        wrapped = textwrap.wrap(notes, width=70, initial_indent="    ", subsequent_indent="    ")
                        lines.extend(wrapped)
                else:
                    lines.append(f" • {item}")

        # Ability
        ra = data.get("role_ability", {})
        if ra:
            render_section("ROLE ABILITY", [ra])
        
        # Cyberware
        render_section("CYBERWARE", data.get("cyberware", []))
        
        lines.append("═" * width)

        return "\n".join(lines)
