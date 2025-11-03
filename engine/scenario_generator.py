"""Scenario and theme generation system for story variety."""

import random
from typing import Dict, List
from dataclasses import dataclass


@dataclass
class Scenario:
    """A distinct opening scenario."""
    name: str
    key: str
    description: str
    opening_prompt: str
    constraints: List[str]


@dataclass
class Theme:
    """A thematic constraint applied throughout the session."""
    name: str
    key: str
    description: str
    pacing_notes: str
    ai_constraints: List[str]


class ScenarioGenerator:
    """Generates varied opening scenarios and themes."""
    
    # 15 distinct opening scenarios
    SCENARIOS = [
        Scenario(
            "BURIED ALIVE",
            "buried_alive",
            "Confined underground, running out of air",
            "You wake in absolute darkness. Wood above you, inches from your face. The air is thick, stale. Your fingers scrape rough wood. You realize: you're in a coffin, underground. Panic rises.",
            ["Confined space", "Oxygen depletion", "Claustrophobia", "Physical struggle"]
        ),
        Scenario(
            "MID-CHASE",
            "mid_chase",
            "Already running from something unknown",
            "You're running. You don't remember when it started. Your lungs burn, your feet ache. Behind you: footsteps. Breathing. Something that doesn't sound quite human. You can't stop.",
            ["Constant motion", "No safe pauses", "Pursuing threat", "Exhaustion"]
        ),
        Scenario(
            "TIME LOOP CONVERSATION",
            "time_loop",
            "Repeating dialogue with subtle changes",
            "\"Hello again.\" The voice is familiar. You've heard these exact words before. Many times. The person in front of you smiles, but their eyes are wrong. \"Shall we begin?\" This conversation has happened before.",
            ["Dialogue focus", "Subtle variations", "Déjà vu", "Pattern recognition"]
        ),
        Scenario(
            "IMPOSSIBLE ARCHITECTURE",
            "impossible_architecture",
            "Escher-like geometry and spatial paradoxes",
            "The hallway slopes up. You walk. It should lead somewhere higher. But when you look back, you're below where you started. The walls meet at angles that shouldn't exist. Gravity feels negotiable.",
            ["Spatial paradoxes", "Geometric impossibility", "Disorientation", "Non-Euclidean space"]
        ),
        Scenario(
            "BODY HORROR AWAKENING",
            "body_horror",
            "Your body is transforming, something is wrong",
            "Your hand looks wrong. Too many joints. The skin ripples. You try to move your fingers—they respond, but there are more than five now. Your flesh is soft, malleable. This isn't your body. Or it wasn't.",
            ["Physical transformation", "Flesh horror", "Loss of form", "Tactile wrongness"]
        ),
        Scenario(
            "COMPUTATIONAL NIGHTMARE",
            "computational",
            "Inside a machine, formatted as data",
            "ERROR: CONSCIOUSNESS DETECTED IN SECTOR 7F9A. You exist as text on a screen. Your thoughts are code. Someone—something—is reading you, editing you, deleting parts of your memory. You are data.",
            ["Digital existence", "Code formatting", "Data corruption", "Machine logic"]
        ),
        Scenario(
            "MEMORY PLAYBACK",
            "memory_playback",
            "Watching corrupted memories glitch and fail",
            "You see yourself five years ago. But the memory is wrong. You're saying things you never said. Doing things you never did. The memory rewinds, plays again. Different this time. Which version is real?",
            ["False memories", "Temporal confusion", "Identity erosion", "Glitching past"]
        ),
        Scenario(
            "SURGERY TABLE",
            "surgery_table",
            "Conscious during your own operation",
            "You can't move. You can see the ceiling. You feel hands inside you. Gloved fingers touching organs. You're awake. Fully conscious. The surgeons haven't noticed. Or they don't care. They're taking something out.",
            ["Helplessness", "Visceral body horror", "Medical dread", "Conscious paralysis"]
        ),
        Scenario(
            "PHONE CALL",
            "phone_call",
            "One-sided conversation with an entity",
            "The phone rings. You answer. The voice knows things about you—private things. It asks questions. Gives instructions. No one else can hear the voice. Your hands move to obey. You don't remember picking up the phone.",
            ["Auditory focus", "One-sided dialogue", "Compulsion", "Invisible control"]
        ),
        Scenario(
            "MIRROR WORLD",
            "mirror_world",
            "Everything inverted, wrong doppelgangers",
            "Your reflection doesn't match your movements. It smiles when you don't. Behind you in the mirror: people. But when you turn, no one's there. The mirror-you mouths words: \"Come through.\"",
            ["Reflection horror", "Doppelgangers", "Inversion", "Parallel reality"]
        ),
        Scenario(
            "FALLING FOREVER",
            "falling_forever",
            "Endless descent through impossible space",
            "You've been falling for... how long? Minutes? Hours? There's no ground. Things pass by: furniture, doors, bodies. You reach for them but gravity is wrong. Your stomach has forgotten what up feels like.",
            ["Vertigo", "Endless motion", "Passing imagery", "Gravity distortion"]
        ),
        Scenario(
            "WITNESS PROTECTION",
            "witness_protection",
            "Someone is hunting you specifically",
            "They know your name. Your address. Your patterns. You saw something you shouldn't have. The messages started a week ago. Then the calls. Then the footsteps outside your door. They're getting closer. Paranoia isn't paranoia if they're really coming.",
            ["Paranoia", "Stalking dread", "Investigation", "Hunter and hunted"]
        ),
        Scenario(
            "LAST HUMAN",
            "last_human",
            "Everyone else is gone or transformed",
            "The streets are empty. Every person you find is wrong—their faces too smooth, their voices too similar. They move in sync. Smile in sync. They say they're human. But you remember when there were real people. Where did everyone go?",
            ["Isolation", "Investigation", "Wrongness detection", "Alone in crowd"]
        ),
        Scenario(
            "PUPPET SHOW",
            "puppet_show",
            "You're controlling someone else, or being controlled",
            "Your limbs move but you don't will them to. You watch yourself walk, talk, act. Or: you're watching someone else and your hands make them move. Which are you? The puppet or the puppeteer? Both feel true.",
            ["Control ambiguity", "Agency loss", "Third person horror", "Identity split"]
        ),
        Scenario(
            "DIGITAL HELL",
            "digital_hell",
            "Trapped in corrupted virtual space",
            "LOADING... ERROR... RETRY... You're inside a program. Walls are textures, stretched and glitching. NPCs repeat dialogue loops. You try to exit. There's no exit command. The system administrator is watching. They're changing the rules.",
            ["Virtual prison", "Game logic horror", "Glitch reality", "Administrator presence"]
        ),
    ]
    
    # 10 thematic seeds
    THEMES = [
        Theme(
            "Velocity Focus",
            "velocity",
            "Constant motion, time pressure, no pauses",
            "Keep the protagonist moving. Clock is always ticking. No safe stops.",
            ["Chase sequences", "Time limits", "Breathless pacing", "No respite"]
        ),
        Theme(
            "Body Horror",
            "body_horror",
            "Physical transformation, flesh wrongness",
            "Focus on tactile sensations. Describe skin, bones, organs. Things are happening to the body.",
            ["Transformation", "Flesh descriptions", "Physical pain", "Form loss"]
        ),
        Theme(
            "Identity Crisis",
            "identity",
            "Who are you really? Memory unreliability",
            "Question the protagonist's identity. False memories. Name confusion. Multiple selves.",
            ["Memory gaps", "Name changes", "Multiple identities", "Self-doubt"]
        ),
        Theme(
            "Computational Dread",
            "computational",
            "Machine logic, algorithms, data corruption",
            "Describe things in technical terms. Binary logic. System errors. The protagonist is data.",
            ["Code language", "Error messages", "System logic", "Processing"]
        ),
        Theme(
            "Pursuit Horror",
            "pursuit",
            "Something hunting you, getting closer",
            "Maintain presence of a pursuer. Footsteps. Breathing. Distance closing. Hunter is persistent.",
            ["Stalker presence", "Distance markers", "Pursuit advancement", "No escape"]
        ),
        Theme(
            "Temporal Anomaly",
            "temporal",
            "Time breaks, loops, paradoxes",
            "Time doesn't work right. Events repeat. Cause precedes effect. Chronology is broken.",
            ["Time loops", "Temporal paradoxes", "Future memories", "Broken causality"]
        ),
        Theme(
            "Spatial Impossibility",
            "spatial",
            "Geometry defies logic, Escher-like",
            "Rooms that shouldn't connect do. Stairs lead nowhere. Impossible angles. Space is wrong.",
            ["Non-Euclidean geometry", "Impossible connections", "Spatial paradoxes", "Disorienting layout"]
        ),
        Theme(
            "Hivemind",
            "hivemind",
            "Multiple voices, collective consciousness",
            "\"We\" instead of \"I\". Shared thoughts. Many speaking as one. Individual dissolving into collective.",
            ["Collective pronouns", "Shared consciousness", "Voice multiplicity", "Individual loss"]
        ),
        Theme(
            "Sensory Deprivation",
            "sensory_deprivation",
            "Losing senses one by one",
            "Senses fail progressively. Vision darkens. Hearing muffles. Touch numbs. Isolation through sense loss.",
            ["Sense degradation", "Darkness increasing", "Sound fading", "Touch loss"]
        ),
        Theme(
            "Metamorphosis",
            "metamorphosis",
            "Gradual transformation into something else",
            "Slow change. Protagonist becoming other. Physical and mental transformation. New form emerging.",
            ["Gradual change", "New abilities", "Form shift", "Becoming other"]
        ),
    ]
    
    def __init__(self, ghost_memory: Dict):
        """Initialize with ghost memory to track recent scenarios."""
        self.ghost_memory = ghost_memory
        self.recent_scenarios = ghost_memory.get('scenarios', [])
        self.current_scenario = None
        self.current_theme = None
    
    def get_opening_scenario(self) -> Dict:
        """
        Select a scenario and theme, avoiding recent repeats.
        Returns dict with all data needed for opening generation.
        """
        # Exclude last 3 scenarios
        available_scenarios = [
            s for s in self.SCENARIOS 
            if s.key not in self.recent_scenarios[-3:]
        ]
        
        # If we've exhausted variety, allow repeats
        if not available_scenarios:
            available_scenarios = self.SCENARIOS
        
        # Select scenario and theme
        self.current_scenario = random.choice(available_scenarios)
        self.current_theme = random.choice(self.THEMES)
        
        return {
            'scenario': self.current_scenario,
            'theme': self.current_theme,
            'scenario_key': self.current_scenario.key,
            'theme_key': self.current_theme.key,
            'opening_prompt': self._build_opening_prompt(),
            'ongoing_constraints': self._build_ongoing_constraints()
        }
    
    def _build_opening_prompt(self) -> str:
        """Build the initial AI prompt with scenario and theme."""
        prompt = f"""OPENING SCENARIO: {self.current_scenario.name}

{self.current_scenario.opening_prompt}

THEMATIC CONSTRAINT: {self.current_theme.name}
{self.current_theme.description}

OPENING REQUIREMENTS:
- Start with the scenario exactly as described above
- Immediately establish concrete, specific details (what you see, hear, feel)
- Create 3-4 choices that reflect both the scenario and theme
- NO vague atmosphere - be specific about the situation
- Make the first choice matter immediately

Generate the opening scene following this scenario."""
        return prompt
    
    def _build_ongoing_constraints(self) -> str:
        """Build constraints for ongoing scene generation."""
        constraints = f"""ACTIVE SCENARIO: {self.current_scenario.name}
Constraints: {', '.join(self.current_scenario.constraints)}

ACTIVE THEME: {self.current_theme.name}
Pacing: {self.current_theme.pacing_notes}
Requirements: {', '.join(self.current_theme.ai_constraints)}

PACING REQUIREMENTS:
- Something concrete must happen this turn (physical event, discovery, transformation, threat advancement)
- AVOID: "you sense something", "you feel uneasy", vague spaces
- REQUIRE: Specific actions, visible changes, tangible threats
- Show, don't tell - describe what happens, not what might happen
"""
        return constraints
    
    def get_scenario_title_art(self) -> str:
        """Get ASCII art for scenario announcement."""
        arts = {
            "buried_alive": """
    ╔═══════════════════════════════╗
    ║   BURIED  ALIVE              ║
    ║   [oxygen depleting...]      ║
    ╚═══════════════════════════════╝
            """,
            "mid_chase": """
    ╔═══════════════════════════════╗
    ║   >>>  MID-CHASE  >>>        ║
    ║   [don't stop running]       ║
    ╚═══════════════════════════════╝
            """,
            "time_loop": """
    ╔═══════════════════════════════╗
    ║   LOOP ∞ LOOP ∞ LOOP         ║
    ║   [this has happened before] ║
    ╚═══════════════════════════════╝
            """,
            "impossible_architecture": """
    ╔═══════════════════════════════╗
    ║   ╱╲ IMPOSSIBLE SPACE ╱╲     ║
    ║   [geometry: unstable]       ║
    ╚═══════════════════════════════╝
            """,
            "body_horror": """
    ╔═══════════════════════════════╗
    ║   YOUR BODY: WRONG           ║
    ║   [flesh: malleable]         ║
    ╚═══════════════════════════════╝
            """,
            "computational": """
    ╔═══════════════════════════════╗
    ║   > SYSTEM.REALITY.ERROR     ║
    ║   [you are: data]            ║
    ╚═══════════════════════════════╝
            """,
            "memory_playback": """
    ╔═══════════════════════════════╗
    ║   ⟲ MEMORY CORRUPTED ⟲       ║
    ║   [playback: unreliable]     ║
    ╚═══════════════════════════════╝
            """,
            "surgery_table": """
    ╔═══════════════════════════════╗
    ║   SURGERY IN PROGRESS        ║
    ║   [patient: conscious]       ║
    ╚═══════════════════════════════╝
            """,
            "phone_call": """
    ╔═══════════════════════════════╗
    ║   ☎ INCOMING CALL            ║
    ║   [caller: unknown]          ║
    ╚═══════════════════════════════╝
            """,
            "mirror_world": """
    ╔═══════════════════════════════╗
    ║   ⇄ MIRROR WORLD ⇄           ║
    ║   [reflection: independent]  ║
    ╚═══════════════════════════════╝
            """,
            "falling_forever": """
    ╔═══════════════════════════════╗
    ║   ↓↓↓ FALLING ↓↓↓            ║
    ║   [ground: undefined]        ║
    ╚═══════════════════════════════╝
            """,
            "witness_protection": """
    ╔═══════════════════════════════╗
    ║   THEY'RE COMING             ║
    ║   [hunter: active]           ║
    ╚═══════════════════════════════╝
            """,
            "last_human": """
    ╔═══════════════════════════════╗
    ║   LAST HUMAN (?)             ║
    ║   [everyone else: wrong]     ║
    ╚═══════════════════════════════╝
            """,
            "puppet_show": """
    ╔═══════════════════════════════╗
    ║   ↕ PUPPET / PUPPETEER ↕     ║
    ║   [control: ambiguous]       ║
    ╚═══════════════════════════════╝
            """,
            "digital_hell": """
    ╔═══════════════════════════════╗
    ║   LOADING... ERROR...        ║
    ║   [exit: not found]          ║
    ╚═══════════════════════════════╝
            """,
        }
        
        return arts.get(self.current_scenario.key, f"""
    ╔═══════════════════════════════╗
    ║   {self.current_scenario.name.upper():^29} ║
    ╚═══════════════════════════════╝
        """)

