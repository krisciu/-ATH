"""Reality-bending rule mutation system."""

import random
import time
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass
from enum import Enum


class MutationType(Enum):
    """Category of mutation."""
    MODERATE = "moderate"  # Early-mid game
    WILD = "wild"  # High revelation, late game


class MutationState(Enum):
    """Lifecycle state of a mutation."""
    ACTIVATING = "activating"  # First turn, being introduced
    ACTIVE = "active"  # Fully active
    STACKING = "stacking"  # Active with other mutations
    FADING = "fading"  # Last turn, ending


class MutationRarity(Enum):
    """Rarity tier for mutations."""
    COMMON = "common"  # 60% - Visual effects, choice mods
    UNCOMMON = "uncommon"  # 30% - Format shifts, narrator changes
    RARE = "rare"  # 8% - Genre shifts, free-text modes
    ULTRA_RARE = "ultra_rare"  # 2% - Complete transformations


@dataclass
class Mutation:
    """A rule-breaking gameplay mutation."""
    name: str
    key: str
    type: MutationType
    rarity: MutationRarity
    description: str
    narrative_trigger: str  # How AI introduces it in story
    discovery_method: str  # How player realizes it's active
    duration: int  # How many turns it lasts (0 = one-shot effect)
    can_stack: bool  # Can be active with other mutations
    fade_narrative: str  # How it ends in story
    requires_special_input: bool = False  # Needs non-standard input
    
    def __eq__(self, other):
        if isinstance(other, Mutation):
            return self.key == other.key
        return self.key == other


class MutationManager:
    """Manages selection and application of rule mutations."""
    
    # 10 MODERATE MUTATIONS
    MODERATE_MUTATIONS = [
        Mutation(
            "Choice Inflation",
            "choice_inflation",
            MutationType.MODERATE,
            "Suddenly provides 6-8 choices instead of normal 3-4",
            "[REALITY SHIFT: choice inflation detected]",
            1  # Lasts one turn
        ),
        Mutation(
            "Choice Drought",
            "choice_drought",
            MutationType.MODERATE,
            "Only 2 choices, both clearly bad",
            "[REALITY SHIFT: options collapsing]",
            1
        ),
        Mutation(
            "Time Pressure",
            "time_pressure",
            MutationType.MODERATE,
            "10-second timer added to input",
            "[REALITY SHIFT: temporal acceleration]",
            1
        ),
        Mutation(
            "Forced Random",
            "forced_random",
            MutationType.MODERATE,
            "Narrator auto-selects a choice for you",
            "[REALITY SHIFT: agency override]",
            0  # One-shot
        ),
        Mutation(
            "Hidden Choice",
            "hidden_choice",
            MutationType.MODERATE,
            "One choice is blank/corrupted, mystery option",
            "[REALITY SHIFT: information corruption]",
            1
        ),
        Mutation(
            "Stat Reveal",
            "stat_reveal",
            MutationType.MODERATE,
            "Suddenly shows hidden stats, then hides again",
            "[REALITY SHIFT: data exposure]",
            0  # One-shot
        ),
        Mutation(
            "Reverse Choices",
            "reverse_choices",
            MutationType.MODERATE,
            "Choices listed backwards or shuffled",
            "[REALITY SHIFT: sequence inversion]",
            1
        ),
        Mutation(
            "Duplicate Choices",
            "duplicate_choices",
            MutationType.MODERATE,
            "Same choice appears 3 times with tiny variations",
            "[REALITY SHIFT: pattern repetition]",
            1
        ),
        Mutation(
            "No Narrative",
            "no_narrative",
            MutationType.MODERATE,
            "Just choices, no story text this turn",
            "[REALITY SHIFT: context collapse]",
            1
        ),
        Mutation(
            "No Choices",
            "no_choices",
            MutationType.MODERATE,
            "Just narrative, auto-continues after pause",
            "[REALITY SHIFT: agency suspension]",
            1
        ),
    ]
    
    # 10 WILD MUTATIONS
    WILD_MUTATIONS = [
        Mutation(
            "Narrator Split",
            "narrator_split",
            MutationType.WILD,
            "Two narrators arguing about what happens",
            "[REALITY FRACTURE: narrative schism]",
            2  # Lasts 2 turns
        ),
        Mutation(
            "Format Shift",
            "format_shift",
            MutationType.WILD,
            "Game becomes poetry, chat log, error messages, etc.",
            "[REALITY FRACTURE: format corruption]",
            2
        ),
        Mutation(
            "Memory Rewrite",
            "memory_rewrite",
            MutationType.WILD,
            "Previous choice gets retconned",
            "[REALITY FRACTURE: history revision]",
            0  # One-shot
        ),
        Mutation(
            "Fourth Wall Breach",
            "fourth_wall",
            MutationType.WILD,
            "Narrator addresses player directly about their terminal/life",
            "[REALITY FRACTURE: containment breach]",
            1
        ),
        Mutation(
            "Choice Rebellion",
            "choice_rebellion",
            MutationType.WILD,
            "Your selection gets overridden mid-action",
            "[REALITY FRACTURE: will override]",
            0  # One-shot
        ),
        Mutation(
            "Temporal Loop",
            "temporal_loop",
            MutationType.WILD,
            "Next 3 choices repeat your last 3 exactly",
            "[REALITY FRACTURE: causality loop]",
            3  # Lasts 3 turns
        ),
        Mutation(
            "Cross-Session Bleed",
            "cross_session",
            MutationType.WILD,
            "References to 'other iterations' appear",
            "[REALITY FRACTURE: iteration bleed detected]",
            1
        ),
        Mutation(
            "Format Corruption",
            "format_corruption",
            MutationType.WILD,
            "Output becomes pure ASCII art, code, or glitch",
            "[REALITY FRACTURE: rendering failure]",
            1
        ),
        Mutation(
            "Interactive Narrator",
            "interactive_narrator",
            MutationType.WILD,
            "Narrator asks YOU questions about the story",
            "[REALITY FRACTURE: role inversion]",
            1
        ),
        Mutation(
            "Reality Negotiation",
            "reality_negotiation",
            MutationType.WILD,
            "Choices become debates with narrator about what's real",
            "[REALITY FRACTURE: consensus required]",
            2
        ),
        # VISUAL/COMPUTER HORROR MUTATIONS (15 more)
        Mutation(
            "Spiral Narrative",
            "spiral_narrative",
            MutationType.WILD,
            "Text spirals across the screen",
            "[REALITY FRACTURE: spatial corruption]",
            1
        ),
        Mutation(
            "Terminal Takeover",
            "terminal_takeover",
            MutationType.WILD,
            "Fake terminal commands interrupt story",
            "[SYSTEM OVERRIDE: shell access detected]",
            1
        ),
        Mutation(
            "Margin Madness",
            "margin_madness",
            MutationType.MODERATE,
            "Marginalia and notes appear in the text",
            "[REALITY SHIFT: annotation overflow]",
            2
        ),
        Mutation(
            "Redaction Protocol",
            "redaction",
            MutationType.MODERATE,
            "Parts of narrative are censored/blacked out",
            "[REALITY SHIFT: information classified]",
            1
        ),
        Mutation(
            "Echo Chamber Active",
            "echo_active",
            MutationType.MODERATE,
            "Words repeat and echo across screen",
            "[REALITY SHIFT: signal reflection]",
            1
        ),
        Mutation(
            "Static Vision",
            "static_vision",
            MutationType.WILD,
            "Heavy static overlays all text",
            "[REALITY FRACTURE: signal degradation]",
            1
        ),
        Mutation(
            "Permission Error",
            "permission_error",
            MutationType.WILD,
            "Fake permission denied messages",
            "[SYSTEM ERROR: access violation]",
            0  # One-shot
        ),
        Mutation(
            "Diagonal Slide",
            "diagonal_slide",
            MutationType.MODERATE,
            "Text slides diagonally down screen",
            "[REALITY SHIFT: gravity malfunction]",
            1
        ),
        Mutation(
            "Box Collapse",
            "box_collapse",
            MutationType.MODERATE,
            "Text trapped in shrinking boxes",
            "[REALITY SHIFT: spatial compression]",
            1
        ),
        Mutation(
            "Fade to Nothing",
            "fade_nothing",
            MutationType.WILD,
            "Text progressively fades away",
            "[REALITY FRACTURE: existence decay]",
            1
        ),
        Mutation(
            "Computer Horror",
            "computer_horror",
            MutationType.WILD,
            "Meta messages about your actual computer/terminal",
            "[BOUNDARY BREACH: observer detected]",
            0  # One-shot
        ),
        Mutation(
            "Mirror Reality",
            "mirror_reality",
            MutationType.WILD,
            "Text and its reverse displayed simultaneously",
            "[REALITY FRACTURE: reflection merge]",
            1
        ),
        Mutation(
            "Scattered Thoughts",
            "scattered",
            MutationType.MODERATE,
            "Words scattered randomly across screen",
            "[REALITY SHIFT: coherence dispersal]",
            1
        ),
        Mutation(
            "Breathing Text",
            "breathing_text",
            MutationType.MODERATE,
            "Spacing expands and contracts",
            "[REALITY SHIFT: spatial respiration]",
            2
        ),
        Mutation(
            "ASCII Intrusion",
            "ascii_intrusion",
            MutationType.WILD,
            "Creepy ASCII art interrupts narrative",
            "[REALITY FRACTURE: visual manifestation]",
            0  # One-shot
        ),
    ]
    
    def __init__(self):
        """Initialize mutation manager."""
        self.active_mutations: List[Tuple[Mutation, int, MutationState]] = []  # (mutation, turns_remaining, state)
        self.mutation_history: List[str] = []
        self.cooldown = 0
    
    def check_mutation(self, context: Dict) -> Optional[Mutation]:
        """
        Check if a mutation should occur this turn.
        Returns Mutation if one should happen, None otherwise.
        """
        # If a mutation is still active, continue it
        if self.active_mutation and self.duration_remaining > 0:
            self.duration_remaining -= 1
            if self.duration_remaining == 0:
                self.active_mutation = None  # Mutation ends
            return self.active_mutation
        
        # Clear active mutation if duration expired
        self.active_mutation = None
        
        # Decrement cooldown
        if self.cooldown > 0:
            self.cooldown -= 1
            return None
        
        # Check for guaranteed mutations at specific choice counts - EARLIER triggers
        choice_count = context.get('choice_count', 0)
        guaranteed_thresholds = [5, 10, 15]  # Changed from [7, 15, 23]
        
        if choice_count in guaranteed_thresholds:
            mutation = self._select_mutation(context, guaranteed=True)
            self._activate_mutation(mutation)
            return mutation
        
        # Random chance based on instability - INCREASED from 5% to 15% base
        instability = context.get('instability_level', 0)
        base_chance = 0.15 + (instability * 0.05)  # Changed from 0.05 + (instability * 0.02)
        
        if random.random() < base_chance:
            mutation = self._select_mutation(context)
            self._activate_mutation(mutation)
            return mutation
        
        return None
    
    def _select_mutation(self, context: Dict, guaranteed: bool = False) -> Mutation:
        """Select an appropriate mutation based on context."""
        revelation_level = context.get('revelation_level', 0)
        
        # Determine available pool
        if revelation_level < 3:
            pool = self.MODERATE_MUTATIONS.copy()
        else:
            # High revelation - both moderate and wild available
            pool = self.MODERATE_MUTATIONS.copy() + self.WILD_MUTATIONS.copy()
        
        # Filter out recently used mutations (avoid last 5)
        available = [m for m in pool if m.key not in self.mutation_history[-5:]]
        
        # If we filtered out everything, allow repeats
        if not available:
            available = pool
        
        # Select mutation
        chosen = random.choice(available)
        
        # Record in history
        self.mutation_history.append(chosen.key)
        
        return chosen
    
    def _activate_mutation(self, mutation: Mutation):
        """Activate a mutation and set its duration."""
        self.active_mutation = mutation
        self.duration_remaining = mutation.duration
        
        # Set cooldown (2-4 choices before next mutation can occur) - REDUCED from 3-6
        self.cooldown = random.randint(2, 4)
    
    def get_state_dict(self) -> Dict:
        """Get mutation state for saving."""
        return {
            'mutation_history': self.mutation_history,
            'cooldown': self.cooldown,
        }
    
    def load_state(self, state: Dict):
        """Load mutation state from save."""
        self.mutation_history = state.get('mutation_history', [])
        self.cooldown = state.get('cooldown', 0)


# Mutation effect application functions
def apply_mutation_to_choices(
    mutation: Mutation, 
    choices: List[str],
    renderer
) -> Tuple[List[str], bool]:
    """
    Apply mutation effect to choice list.
    Returns (modified_choices, skip_input) where skip_input=True means auto-continue.
    """
    if not mutation:
        return choices, False
    
    key = mutation.key
    
    # CHOICE INFLATION - 6-8 choices
    if key == "choice_inflation":
        # Duplicate and vary existing choices
        inflated = choices.copy()
        variations = [
            lambda c: c + " (carefully)",
            lambda c: c + " (quickly)",
            lambda c: c + " (hesitantly)",
            lambda c: c + " (recklessly)",
        ]
        for choice in choices[:2]:  # Vary first 2 choices
            inflated.append(random.choice(variations)(choice))
        return inflated, False
    
    # CHOICE DROUGHT - Only 2 choices
    elif key == "choice_drought":
        bad_choices = [
            "Give up",
            "Accept the inevitable",
        ]
        return bad_choices, False
    
    # HIDDEN CHOICE - One choice is corrupted
    elif key == "hidden_choice":
        hidden_idx = random.randint(0, len(choices) - 1)
        choices[hidden_idx] = "░░░░░░░░░░░░░░"
        return choices, False
    
    # REVERSE CHOICES - Backwards order
    elif key == "reverse_choices":
        return list(reversed(choices)), False
    
    # DUPLICATE CHOICES - Same choice 3 times with tiny variations
    elif key == "duplicate_choices":
        base = random.choice(choices)
        return [
            base,
            base + ".",
            base + " ",
        ], False
    
    # NO NARRATIVE - Will be handled in main loop
    elif key == "no_narrative":
        return choices, False
    
    # NO CHOICES - Auto-continue
    elif key == "no_choices":
        return [], True  # Empty choices signals auto-continue
    
    # NARRATOR SPLIT - Will be handled in renderer
    elif key == "narrator_split":
        return choices, False
    
    # FORMAT SHIFT - Will be handled in renderer
    elif key == "format_shift":
        return choices, False
    
    # FOURTH WALL - Add meta choice
    elif key == "fourth_wall":
        choices.append("(close the terminal)")
        return choices, False
    
    # TEMPORAL LOOP - Will need special handling in main
    elif key == "temporal_loop":
        return choices, False
    
    # CROSS SESSION - Add meta hints
    elif key == "cross_session":
        choices.append("Remember other iterations")
        return choices, False
    
    # FORMAT CORRUPTION - Choices become glitched
    elif key == "format_corruption":
        glitched = []
        for choice in choices:
            if random.random() < 0.5:
                glitched.append(''.join(random.choice(['█', '▓', '▒', '░', c]) for c in choice))
            else:
                glitched.append(choice)
        return glitched, False
    
    # INTERACTIVE NARRATOR - Narrator asks questions
    elif key == "interactive_narrator":
        questions = [
            "Should I continue?",
            "What would you like to see happen?",
            "Is this what you expected?",
        ]
        return questions, False
    
    # REALITY NEGOTIATION - Debate options
    elif key == "reality_negotiation":
        debates = [
            "Insist this is real",
            "Claim this is simulation",
            "Deny the narrator's authority",
        ]
        return debates, False
    
    return choices, False


def apply_mutation_to_narrative(
    mutation: Mutation,
    narrative: str,
    context: Dict,
    renderer
) -> str:
    """Apply mutation effect to narrative display."""
    if not mutation:
        return narrative
    
    key = mutation.key
    
    # NO NARRATIVE - Return empty
    if key == "no_narrative":
        return ""
    
    # FORMAT SHIFT - Transform to different format
    elif key == "format_shift":
        formats = ["poetry", "chat", "code", "error"]
        format_type = random.choice(formats)
        
        if format_type == "poetry":
            lines = narrative.split('. ')
            poetry = "\n".join(f"  {line}" for line in lines)
            return f"[POETRY MODE]\n{poetry}"
        
        elif format_type == "chat":
            return f"[SYSTEM]: {narrative}\n[USER]: ..."
        
        elif format_type == "code":
            return f"// NARRATIVE_BUFFER\nstd::string story = \"{narrative[:50]}...\";\n// EXECUTION_CONTINUE"
        
        elif format_type == "error":
            return f"ERROR 0x7F9A: {narrative[:30]}... [STACK TRACE CORRUPTED]"
    
    # FOURTH WALL - Add direct address
    elif key == "fourth_wall":
        addresses = [
            "(I can see your terminal window, you know.)",
            "(How long have you been sitting there?)",
            "(Your keyboard sounds nervous.)",
        ]
        return narrative + "\n\n" + random.choice(addresses)
    
    # CROSS SESSION - Reference other runs
    elif key == "cross_session":
        references = [
            "(This happened differently in iteration #47.)",
            "(The other you made a different choice here.)",
            "(Across 109 sessions, no one has done this.)",
        ]
        return narrative + "\n\n" + random.choice(references)
    
    # FORMAT CORRUPTION - Heavy glitching
    elif key == "format_corruption":
        # Convert random words to glitch
        words = narrative.split()
        corrupted = []
        for word in words:
            if random.random() < 0.3:
                corrupted.append(''.join(random.choice(['█', '▓', '▒', '░', c]) for c in word))
            else:
                corrupted.append(word)
        return ' '.join(corrupted)
    
    # NEW VISUAL MUTATIONS
    elif key == "spiral_narrative":
        from engine.typography import TypographyEngine
        typo = TypographyEngine()
        return typo.create_spiral_text(narrative)
    
    elif key == "terminal_takeover":
        from engine.typography import TypographyEngine
        typo = TypographyEngine()
        glitch = typo.create_terminal_glitch()
        return f"{glitch}\n{narrative}\n{typo.create_cursor_artifact()}"
    
    elif key == "margin_madness":
        from engine.typography import TypographyEngine
        typo = TypographyEngine()
        return typo.create_margin_notes(narrative)
    
    elif key == "redaction":
        from engine.typography import TypographyEngine
        typo = TypographyEngine()
        return typo.create_redacted_text(narrative, 0.4)
    
    elif key == "echo_active":
        # Echo key words
        words = narrative.split()
        if len(words) > 3:
            from engine.typography import TypographyEngine
            typo = TypographyEngine()
            echo_word = random.choice(words[1:-1])
            echoed = typo.create_echo_text(echo_word)
            return narrative.replace(echo_word, echoed, 1)
        return narrative
    
    elif key == "static_vision":
        from engine.typography import TypographyEngine
        typo = TypographyEngine()
        return typo.create_static_overlay(narrative)
    
    elif key == "diagonal_slide":
        from engine.typography import TypographyEngine
        typo = TypographyEngine()
        return typo.create_diagonal_text(narrative)
    
    elif key == "box_collapse":
        from engine.typography import TypographyEngine
        typo = TypographyEngine()
        return typo.create_box_text(narrative)
    
    elif key == "fade_nothing":
        from engine.typography import TypographyEngine
        typo = TypographyEngine()
        return typo.create_fading_text(narrative)
    
    elif key == "computer_horror":
        from engine.typography import TypographyEngine
        typo = TypographyEngine()
        horror_msg = typo.get_computer_horror_message()
        return f"{narrative}\n\n{horror_msg}"
    
    elif key == "mirror_reality":
        from engine.typography import TypographyEngine
        typo = TypographyEngine()
        return typo.create_mirror_text(narrative)
    
    elif key == "scattered":
        from engine.typography import TypographyEngine
        typo = TypographyEngine()
        return typo.create_scattered_text(narrative, 0.7)
    
    elif key == "breathing_text":
        from engine.typography import TypographyEngine
        typo = TypographyEngine()
        return typo.create_breathing_space(narrative)
    
    elif key == "ascii_intrusion":
        from engine.typography import TypographyEngine
        typo = TypographyEngine()
        art = typo.get_creepy_ascii_art()
        return f"{art}\n\n{narrative}"
    
    elif key == "permission_error":
        from engine.typography import TypographyEngine
        typo = TypographyEngine()
        error = typo.create_permission_denied()
        return f"{error}\n\n{narrative}"
    
    return narrative


def handle_special_mutations(
    mutation: Mutation,
    context: Dict,
    renderer,
    story_engine
) -> Optional[str]:
    """
    Handle mutations that require special one-time effects.
    Returns message to display, or None.
    """
    if not mutation:
        return None
    
    key = mutation.key
    
    # TIME PRESSURE - Show countdown
    if key == "time_pressure":
        return "[You have 10 seconds to choose]"
    
    # FORCED RANDOM - Auto-select
    elif key == "forced_random":
        return "[The narrator chooses for you]"
    
    # STAT REVEAL - Show and hide stats
    elif key == "stat_reveal":
        stats = context['hidden_stats']
        msg = f"\n[STATS EXPOSED]\nCourage: {stats['courage']}\nSanity: {stats['sanity']}\nCuriosity: {stats['curiosity']}\nTrust: {stats['trust']}\n[DATA PURGED]\n"
        return msg
    
    # MEMORY REWRITE - Retcon previous choice
    elif key == "memory_rewrite":
        prev_choice = context.get('previous_choice', 'BEGIN')
        if prev_choice != 'BEGIN':
            fake_choice = f"Actually, you chose to {random.choice(['run', 'hide', 'scream', 'surrender'])}"
            return f"\n[MEMORY CORRECTION]\nNo, wait. {fake_choice}.\nThe records have been updated.\n"
    
    # CHOICE REBELLION - Override player's choice
    elif key == "choice_rebellion":
        return "[Your choice is noted. But you do something else instead.]"
    
    return None

