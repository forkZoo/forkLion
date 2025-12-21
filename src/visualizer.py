"""
ForkMonkey Visualizer - Lion Edition
"""

import math
from typing import Dict, List
from src.genetics import MonkeyDNA, TraitCategory, Rarity

class MonkeyVisualizer:
    """Generates generic SVG lion art from DNA"""

    BODY_COLORS = {
        "brown": {"main": "#CD853F", "shadow": "#8B4513", "highlight": "#DEB887"},
        "tan": {"main": "#D2B48C", "shadow": "#B8956E", "highlight": "#F4A460"},
        "beige": {"main": "#F5F5DC", "shadow": "#D4D4B8", "highlight": "#FFFFF0"},
        "golden": {"main": "#DAA520", "shadow": "#B8860B", "highlight": "#FFD700"},
        "white": {"main": "#FFFFFF", "shadow": "#E0E0E0", "highlight": "#FFFFFF"},
        "black": {"main": "#2F2F2F", "shadow": "#000000", "highlight": "#4F4F4F"},
    }

    BACKGROUNDS = {
        "white": {"type": "solid", "color": "#FFF5E6"},
        "blue_sky": {"type": "gradient", "id": "sky-gradient"},
        "sunset": {"type": "gradient", "id": "sunset-gradient"},
        "savanna": {"type": "scene", "base": "#F4A460", "elements": "trees"},
    }

    @classmethod
    def generate_svg(cls, dna: MonkeyDNA, width: int = 400, height: int = 400) -> str:
        traits = {
            "body_color": dna.traits[TraitCategory.BODY_COLOR].value,
            "expression": dna.traits[TraitCategory.FACE_EXPRESSION].value,
            "accessory": dna.traits[TraitCategory.ACCESSORY].value,
            "pattern": dna.traits[TraitCategory.PATTERN].value,
            "background": dna.traits[TraitCategory.BACKGROUND].value,
            "special": dna.traits[TraitCategory.SPECIAL].value,
        }
        seed = int(dna.dna_hash[:8], 16) if dna.dna_hash else 12345

        svg_parts = [
            f'<svg width="{width}" height="{height}" viewBox="0 0 {width} {height}" xmlns="http://www.w3.org/2000/svg">',
            cls._generate_defs(),
            cls._generate_background(traits["background"], width, height, seed),
            cls._generate_body(traits["body_color"], traits["pattern"], width, height, seed),
            cls._generate_face(traits["expression"], width, height),
            "</svg>",
        ]
        return "\n".join(svg_parts)

    @classmethod
    def _generate_defs(cls) -> str:
        return '''<defs>
    <filter id="shadow" x="-20%" y="-20%" width="140%" height="140%">
        <feDropShadow dx="2" dy="4" stdDeviation="3" flood-opacity="0.3"/>
    </filter>
    <linearGradient id="sky-gradient" x1="0%" y1="0%" x2="0%" y2="100%">
        <stop offset="0%" stop-color="#87CEEB"/><stop offset="100%" stop-color="#E0F4FF"/>
    </linearGradient>
    <linearGradient id="sunset-gradient" x1="0%" y1="0%" x2="0%" y2="100%">
        <stop offset="0%" stop-color="#FF4500"/><stop offset="100%" stop-color="#FFD700"/>
    </linearGradient>
</defs>'''

    @classmethod
    def _generate_background(cls, bg: str, w: int, h: int, seed: int) -> str:
        if bg == "savanna":
            return f'<rect width="{w}" height="{h}" fill="#F4A460"/><circle cx="50" cy="50" r="30" fill="#FFD700" opacity="0.8"/>'
        return f'<rect width="{w}" height="{h}" fill="#FFF5E6"/>'

    @classmethod
    def _generate_body(cls, color: str, pattern: str, w: int, h: int, seed: int) -> str:
        cx, cy = w // 2, h // 2
        c = cls.BODY_COLORS.get(color, cls.BODY_COLORS["brown"])
        parts = []

        # Mane (Big and fluffy)
        for i in range(12):
            angle = i * 30
            parts.append(f'<ellipse cx="{cx}" cy="{cy}" rx="140" ry="140" fill="#8B4513" transform="rotate({angle} {cx} {cy})" opacity="0.8"/>')
        
        parts.append(f'<circle cx="{cx}" cy="{cy}" r="120" fill="#A0522D" filter="url(#shadow)"/>')

        # Ears
        parts.append(f'<circle cx="{cx-70}" cy="{cy-70}" r="25" fill="{c["main"]}"/>')
        parts.append(f'<circle cx="{cx+70}" cy="{cy-70}" r="25" fill="{c["main"]}"/>')
        
        # Head
        parts.append(f'<circle cx="{cx}" cy="{cy}" r="90" fill="{c["main"]}" filter="url(#shadow)"/>')
        
        # Muzzle
        parts.append(f'<ellipse cx="{cx}" cy="{cy+30}" rx="45" ry="35" fill="{c["highlight"]}" opacity="0.6"/>')

        return "\n".join(parts)

    @classmethod
    def _generate_face(cls, expr: str, w: int, h: int) -> str:
        cx, cy = w // 2, h // 2
        parts = []
        
        # Eyes (Intense)
        parts.append(f'<path d="M{cx-40} {cy-10} Q{cx-20} {cy-25} {cx} {cy-10}" stroke="#000" stroke-width="2" fill="none" opacity="0.5"/>')
        parts.append(f'<ellipse cx="{cx-30}" cy="{cy-10}" rx="12" ry="10" fill="#FFD700"/>')
        parts.append(f'<ellipse cx="{cx+30}" cy="{cy-10}" rx="12" ry="10" fill="#FFD700"/>')
        parts.append(f'<circle cx="{cx-30}" cy="{cy-10}" r="4" fill="#000"/>')
        parts.append(f'<circle cx="{cx+30}" cy="{cy-10}" r="4" fill="#000"/>')
        
        # Nose (Broad)
        parts.append(f'<path d="M{cx-20} {cy+20} L{cx+20} {cy+20} L{cx} {cy+45} Z" fill="#3E2723"/>')
        
        # Mouth
        parts.append(f'<path d="M{cx} {cy+45} L{cx} {cy+55}" stroke="#3E2723" stroke-width="2"/>')
        parts.append(f'<path d="M{cx-20} {cy+60} Q{cx-10} {cy+70} {cx} {cy+55}" stroke="#3E2723" stroke-width="2" fill="none"/>')
        parts.append(f'<path d="M{cx+20} {cy+60} Q{cx+10} {cy+70} {cx} {cy+55}" stroke="#3E2723" stroke-width="2" fill="none"/>')
            
        return "\n".join(parts)

    @classmethod
    def generate_thumbnail(cls, dna: MonkeyDNA, size: int = 100) -> str:
        return cls.generate_svg(dna, width=size, height=size)

def main():
    pass

if __name__ == "__main__":
    main()
