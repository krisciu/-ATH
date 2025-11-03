"""Typography and visual effects system - experimental terminal horror."""

import random
import re
import time
from typing import List, Optional
from config.settings import VISUAL_INTENSITY


class TypographyEngine:
    """Handles experimental text layout and visual effects."""
    
    # Unicode characters for corruption effects
    CORRUPTION_CHARS = ['̴', '̷', '̶', '̸', '̵', '̢', '̡', '̧', '̨', '̛']
    GLITCH_REPLACEMENTS = {
        'a': ['@', 'a', '4'],
        'e': ['3', 'e', 'é'],
        'i': ['1', 'i', '!'],
        'o': ['0', 'o', 'ø'],
        's': ['$', '5', 's'],
        't': ['+', 't', '7'],
    }
    
    def __init__(self):
        """Initialize typography engine."""
        self.intensity = 0.0
    
    def set_intensity(self, intensity_level: str):
        """Set visual intensity based on game state."""
        self.intensity = VISUAL_INTENSITY.get(intensity_level, 0.0)
    
    def apply_effects(self, text: str, intensity_override: float = None) -> str:
        """Apply typography effects based on current intensity."""
        intensity = intensity_override if intensity_override is not None else self.intensity
        
        if intensity <= 0.1:
            # Even when stable, occasionally mess with the player
            if random.random() < 0.02:  # 2% chance
                return self._add_meta_trick(text)
            return text  # No effects when stable
        
        # Apply effects with increasing probability
        effects = []
        
        if random.random() < intensity * 0.3:
            text = self._add_spacing_glitches(text, intensity)
        
        if random.random() < intensity * 0.4:
            text = self._add_character_substitution(text, intensity)
        
        if random.random() < intensity * 0.25:
            text = self._add_repetition(text, intensity)
        
        if intensity > 0.5 and random.random() < intensity * 0.2:
            text = self._add_corruption(text, intensity)
        
        return text
    
    def _add_meta_trick(self, text: str) -> str:
        """Add subtle meta tricks even when stable."""
        tricks = [
            lambda t: t + " (wait, did I say that out loud?)",
            lambda t: t.replace("you", "you (yes, you reading this)"),
            lambda t: "[RECORDING] " + t,
            lambda t: t + " [REDACTED]",
        ]
        return random.choice(tricks)(text)
    
    def _add_spacing_glitches(self, text: str, intensity: float) -> str:
        """Add random spacing issues."""
        words = text.split()
        result = []
        
        for word in words:
            if random.random() < intensity * 0.3:
                # Add extra spaces within word
                chars = list(word)
                spaced = ' '.join(chars) if len(chars) > 3 else word
                result.append(spaced)
            else:
                result.append(word)
        
        return ' '.join(result)
    
    def apply_glitch(self, text: str, intensity: float = 0.2) -> str:
        """Public method to apply glitch effect to text."""
        return self._add_character_substitution(text, intensity)
    
    def _add_character_substitution(self, text: str, intensity: float) -> str:
        """Replace characters with glitch alternatives."""
        result = []
        
        for char in text:
            if char.lower() in self.GLITCH_REPLACEMENTS and random.random() < intensity * 0.15:
                replacements = self.GLITCH_REPLACEMENTS[char.lower()]
                result.append(random.choice(replacements))
            else:
                result.append(char)
        
        return ''.join(result)
    
    def _add_repetition(self, text: str, intensity: float) -> str:
        """Add word/syllable repetition."""
        words = text.split()
        result = []
        
        for word in words:
            if random.random() < intensity * 0.2 and len(word) > 3:
                # Repeat the word or stutter it
                if random.random() < 0.5:
                    result.append(f"{word} {word}")
                else:
                    # Stutter first syllable
                    stutter = word[:2] + '-' + word
                    result.append(stutter)
            else:
                result.append(word)
        
        return ' '.join(result)
    
    def _add_corruption(self, text: str, intensity: float) -> str:
        """Add Unicode corruption marks."""
        result = []
        
        for char in text:
            result.append(char)
            if char.isalpha() and random.random() < intensity * 0.1:
                result.append(random.choice(self.CORRUPTION_CHARS))
        
        return ''.join(result)
    
    def create_scattered_text(self, text: str, width: int = 80) -> List[str]:
        """Scatter text across multiple lines (panic effect)."""
        words = text.split()
        lines = [''] * 10
        
        for word in words:
            line_idx = random.randint(0, len(lines) - 1)
            pos = random.randint(0, max(0, width - len(word) - 1))
            
            # Create spacing
            spaced_word = ' ' * pos + word
            if len(lines[line_idx]) < pos:
                lines[line_idx] = lines[line_idx].ljust(pos) + word
            else:
                lines[line_idx] += '  ' + word
        
        return [line for line in lines if line.strip()]
    
    def create_spiral_text(self, text: str, inward: bool = True) -> List[str]:
        """Create spiraling text effect."""
        words = text.split()
        lines = []
        indent = 0 if inward else 20
        
        for i, word in enumerate(words[:8]):  # Limit for readability
            if inward:
                indent = i * 2
            else:
                indent = max(0, 20 - i * 2)
            
            lines.append(' ' * indent + word)
        
        return lines
    
    def create_vertical_text(self, text: str) -> List[str]:
        """Create vertical text (falling/climbing effect)."""
        words = text.split()[:5]  # Limit words
        lines = []
        
        for word in words:
            for char in word:
                lines.append('    ' + char)
        
        return lines
    
    def add_strikethrough(self, text: str, word_to_strike: str) -> str:
        """Add strikethrough effect to specific words using Unicode."""
        # Use Unicode strikethrough combining character
        struck = ''.join(c + '\u0336' for c in word_to_strike)
        return text.replace(word_to_strike, struck)
    
    def add_marginalia(self, text: str, note: str, position: str = 'end') -> str:
        """Add margin notes/asides."""
        if position == 'end':
            return f"{text}  [{note}]"
        elif position == 'start':
            return f"[{note}]  {text}"
        else:  # middle
            words = text.split()
            mid = len(words) // 2
            words.insert(mid, f"[{note}]")
            return ' '.join(words)
    
    def create_size_emphasis(self, text: str, emphasis_word: str) -> str:
        """Emphasize words with visual sizing (limited in terminal)."""
        # Use spacing and caps to simulate size
        emphasized = emphasis_word.upper()
        spaced = ' '.join(emphasized)
        return text.replace(emphasis_word, f"\n  {spaced}\n")
    
    def create_fake_footnote(self) -> str:
        """Create fake footnote markers."""
        footnotes = [
            "[1] There is no footnote 1.",
            "[*] This note leads nowhere.",
            "[?] You shouldn't read this.",
            "[†] [MISSING]"
        ]
        return random.choice(footnotes)
    
    def process_narrator_corrections(self, text: str) -> str:
        """Process strikethrough corrections in text."""
        # Look for patterns like "safe" that should be "trapped"
        patterns = [
            ("safe", "trapped"),
            ("door", "mouth"),
            ("hallway", "throat"),
            ("room", "stomach"),
            ("exit", "entrance"),
            ("forward", "backward"),
        ]
        
        if random.random() < self.intensity * 0.3:
            old, new = random.choice(patterns)
            if old in text.lower():
                # Use Unicode strikethrough
                struck_old = ''.join(c + '\u0336' for c in old)
                text = re.sub(
                    r'\b' + old + r'\b', 
                    f"{struck_old} {new}", 
                    text, 
                    count=1,
                    flags=re.IGNORECASE
                )
        
        return text
    
    def get_loading_glitch(self) -> str:
        """Get a loading message that fits the aesthetic."""
        messages = [
            "[LOADING...]",
            "[REMEMBERING...]",
            "[FORGETTING...]",
            "[RECONSTRUCTING...]",
            "[C̴O̷N̶N̸E̷C̴T̸I̷N̶G̸...]",
            "[PLEASE WAIT]",
            "[DO NOT WAIT]",
            "[T̷I̶M̸E̷ ̶E̸R̷R̶O̷R̴]",
        ]
        
        if self.intensity > 0.5:
            return random.choice(messages[-4:])
        return random.choice(messages[:4])
    
    # ===== EXPANDED VISUAL EFFECTS =====
    
    def create_spiral_text(self, text: str, clockwise: bool = True) -> str:
        """Create spiraling text effect."""
        words = text.split()
        if len(words) < 3:
            return text
        
        spiral = []
        indent = 0
        direction = 1 if clockwise else -1
        
        for i, word in enumerate(words[:10]):  # Limit to 10 words
            spiral.append(" " * abs(indent) + word)
            indent += direction
            if abs(indent) > 5:
                direction *= -1
        
        return "\n".join(spiral)
    
    def create_diagonal_text(self, text: str) -> str:
        """Create diagonal sliding text."""
        words = text.split()[:8]
        lines = []
        for i, word in enumerate(words):
            lines.append(" " * i + word)
        return "\n".join(lines)
    
    def create_centered_collapse(self, text: str) -> str:
        """Text that collapses toward center."""
        words = text.split()
        if len(words) < 5:
            return text
        
        mid = len(words) // 2
        lines = []
        
        for i in range(mid):
            indent = mid - i
            lines.append(" " * indent + words[i])
        
        lines.append(words[mid])  # Center word
        
        for i in range(mid + 1, len(words)):
            indent = i - mid
            lines.append(" " * indent + words[i])
        
        return "\n".join(lines)
    
    def create_mirror_text(self, text: str) -> str:
        """Create mirrored/reflected text."""
        return f"{text}\n{''.join(reversed(text))}"
    
    def create_scattered_text(self, text: str, scatter_intensity: float = 0.5) -> str:
        """Scatter text across the space."""
        words = text.split()
        lines = [""] * min(len(words), 8)
        
        for i, word in enumerate(words[:8]):
            indent = random.randint(0, int(40 * scatter_intensity))
            lines[i] = " " * indent + word
        
        return "\n".join(lines)
    
    def create_overlapping_text(self, text1: str, text2: str) -> str:
        """Overlap two texts (simulated)."""
        return f"{text1} {text2}"  # Simple overlap
    
    def create_box_text(self, text: str) -> str:
        """Put text in a box."""
        lines = text.split('\n')
        max_len = max(len(line) for line in lines) if lines else 0
        max_len = min(max_len, 60)
        
        box = ["┌" + "─" * (max_len + 2) + "┐"]
        for line in lines[:5]:  # Limit lines
            padded = line[:max_len].ljust(max_len)
            box.append(f"│ {padded} │")
        box.append("└" + "─" * (max_len + 2) + "┘")
        
        return "\n".join(box)
    
    def create_margin_notes(self, text: str) -> str:
        """Add marginal annotations."""
        notes = [
            "       → this isn't right",
            "       → you're reading this wrong",
            "       → skip this part",
            "       → [CORRUPTED]",
            "       → see footnote [missing]",
        ]
        
        lines = text.split('.')[:3]
        result = []
        for i, line in enumerate(lines):
            result.append(line + ".")
            if random.random() < 0.4 and i < len(notes):
                result.append(notes[i])
        
        return "\n".join(result)
    
    def create_redacted_text(self, text: str, redact_ratio: float = 0.3) -> str:
        """Redact portions of text."""
        words = text.split()
        redacted_words = []
        
        for word in words:
            if random.random() < redact_ratio:
                redacted_words.append("█" * len(word))
            else:
                redacted_words.append(word)
        
        return " ".join(redacted_words)
    
    def create_fading_text(self, text: str) -> str:
        """Text that fades as it goes."""
        chars = list(text)
        fade_chars = ['░', '▒', '▓', '█']
        
        fade_point = len(chars) // 2
        for i in range(fade_point, len(chars)):
            if chars[i] not in [' ', '\n']:
                fade_level = min(3, (i - fade_point) // 10)
                if random.random() < 0.3:
                    chars[i] = fade_chars[fade_level]
        
        return ''.join(chars)
    
    def create_echo_text(self, word: str, echo_count: int = 3) -> str:
        """Create echoing effect for a word."""
        echoes = [word]
        for i in range(1, echo_count):
            faded = ''.join(c if random.random() > (i * 0.3) else '░' for c in word)
            echoes.append(faded)
        return " ".join(echoes)
    
    def create_static_overlay(self, text: str) -> str:
        """Overlay static noise on text."""
        static = ['▓', '▒', '░', '█']
        chars = list(text)
        
        for i in range(len(chars)):
            if chars[i] not in [' ', '\n'] and random.random() < 0.15:
                chars[i] = random.choice(static)
        
        return ''.join(chars)
    
    def create_breathing_space(self, text: str) -> str:
        """Add expanding/contracting spaces (simulated)."""
        words = text.split()
        spaced = []
        
        for i, word in enumerate(words):
            spaces = "  " * (1 + (i % 3))  # Vary spacing
            spaced.append(word + spaces)
        
        return "".join(spaced).rstrip()
    
    def create_terminal_glitch(self) -> str:
        """Create fake terminal artifacts."""
        glitches = [
            "^C^C^C",
            "[CTRL+Z]",
            ">>> ",
            "$ ",
            "ERROR: Segmentation fault",
            "zsh: command not found:",
            "Connection to localhost closed.",
            "-bash: syntax error",
            "kill -9 $$",
        ]
        return random.choice(glitches)
    
    def create_cursor_artifact(self) -> str:
        """Fake cursor/typing indicators."""
        artifacts = [
            "_",
            "▌",
            "█",
            "|",
            "...",
        ]
        return random.choice(artifacts)
    
    def create_permission_denied(self) -> str:
        """Fake permission errors."""
        errors = [
            "Permission denied: you are not meant to read this",
            "Access denied: file corrupted",
            "Error 403: Narrative forbidden",
            "rm: cannot remove 'reality': Permission denied",
        ]
        return random.choice(errors)
    
    def get_creepy_ascii_art(self, art_type: str = "random") -> str:
        """Get pre-made creepy ASCII art - expanded library."""
        arts = {
            "eyes": """
        👁️        👁️
            ‿
            """,
            "watching": """
    👁️ 👁️ 👁️ 👁️ 👁️
      👁️ 👁️ 👁️ 👁️
        👁️ 👁️ 👁️
            """,
            "eyes_detailed": """
      ╱─────╲  ╱─────╲
     │  ◉◉  ││  ◉◉  │
      ╲_____╱  ╲_____╱
        │        │
            """,
            "many_eyes": """
    (◉) (◉) (◉)
      (◉) (◉)
    (◉) (◉) (◉)
       watching
            """,
            "static": """
    ▓▒░░▒▓█▓▒░░▒▓
    ░▒▓█▓▒░░▒▓█▓▒
    ▓▒░░▒▓█▓▒░░▒▓
            """,
            "corruption": """
    ◢◤◢◤◢◤◢◤◢◤
    ◥◣◥◣◥◣◥◣◥◣
    ◢◤◢◤◢◤◢◤◢◤
            """,
            "spiral": """
        ╭─────╮
        │  ◉  │
        ╰─────╯
            """,
            "glitch": """
    █▓▒░T̴H̷I̶N̸K̷█▒▓░
    ░▒▓█E̴R̷R̶O̸R̷░▓▒█
    ▓▒░█N̴O̷W̶░▒▓█▓
            """,
            "void": """
    ░░░░░░░░░░░░░░
    ░░░░░ ◉ ░░░░░
    ░░░░░░░░░░░░░░
            """,
            "mouth": """
        ╱▔▔▔▔▔╲
        ▏  👄  ▕
        ╲_____╱
            """,
            "mouth_teeth": """
      ╱▔▔▔▔▔▔▔╲
     │ ▲▼▲▼▲▼▲ │
     │ ▼▲▼▲▼▲▼ │
      ╲________╱
            """,
            "hands": """
    🖐️         🖐️
      🖐️     🖐️
         🖐️
            """,
            "reaching_hand": """
         ╱│╲
        ╱ │ ╲
       │  │  │
       │  │  │
      ╱│ ╱│╲ │╲
     ╱ │╱ │ ╲│ ╲
    reaching...
            """,
            "twisted_hand": """
      ╱╲  ╱╲  ╱╲
     ╱  ╲╱  ╲╱  ╲
    │ too many  │
     ╲ fingers ╱
      ╲╲╲│╱╱╱
            """,
            "skeletal": """
        ☠
       ╱│╲
      ╱ │ ╲
        │
       ╱ ╲
      ╱   ╲
            """,
            "skull": """
      ┌─────┐
      │ ◉ ◉ │
      │  ▼  │
      │ ══  │
      └─────┘
            """,
            "death_figure": """
        ___
       ╱   ╲
      │ ☠ ☠ │
       ╲___╱
       ╱│││╲
      ╱ │││ ╲
            """,
            "binary": """
    01001000 01000101
    01001100 01010000
    00100001 00100001
            """,
            "flesh_mass": """
      ╱╲╱╲╱╲
     ╱▓▒░▒▓╲
    │ pulsing │
     ╲▒▓░▓▒╱
      ╲╱╲╱╲╱
            """,
            "tendrils": """
       ╱  │  ╲
      ╱   │   ╲
     ╱   ╱│╲   ╲
    │   ╱ │ ╲   │
     ╲ ╱  │  ╲ ╱
      writhing
            """,
            "geometric_horror": """
      ╱╲
     ╱  ╲
    ╱ ╱╲ ╲
    ╲ ╲╱ ╱
     ╲  ╱
      ╲╱
    impossible
            """,
            "doorway": """
    ┌─────────┐
    │         │
    │    ?    │
    │         │
    │  ╱───╲  │
    └──└───┘──┘
            """,
            "machine": """
    ╔═══╦═══╗
    ║ ◉ ║ ◉ ║
    ╠═══╬═══╣
    ║▓▒░│░▒▓║
    ╚═══╩═══╝
    computing
            """,
            "split_face": """
      ╱◉ │ ◉╲
     │   │   │
     │ ══│══ │
      ╲  │  ╱
       ╲_│_╱
            """,
            "melting": """
      ╱▔▔▔╲
     │ ◉ ◉ │
     │ drip │
      ╲╲│╱╱
       ▼▼▼
            """,
            "veins": """
    ╱─╲  ╱─╲
    │ ╱──╲ │
    ╲─╲  ╱─╱
      ╲──╱
    pulsing
            """,
        }
        
        if art_type == "random":
            return random.choice(list(arts.values()))
        return arts.get(art_type, arts["void"])
    
    def get_computer_horror_message(self) -> str:
        """Meta messages about the terminal/computer."""
        messages = [
            "(your terminal is ${COLUMNS} characters wide)",
            "(you've been sitting here for a while)",
            "(your keyboard has fingerprints on the W, A, S, D keys)",
            "(the fan on your computer just got louder)",
            "(did your cursor just move on its own?)",
            "(check your running processes)",
            "(close this window and walk away)",
            "(ps aux | grep fear)",
            "(your screen is very bright in this dark room)",
            "(someone can see your screen from behind you)",
            "(cat /dev/urandom)",
            "(this process is using 99% of your CPU)",
            "(your battery: LOW)",
        ]
        return random.choice(messages)

