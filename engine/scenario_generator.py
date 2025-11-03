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
            """Your hand looks wrong. Too many joints. The skin ripples like water. You try to move your fingers—they respond, but there are more than five now, and they're growing longer, splitting at the tips. Your flesh is soft, malleable, warm like clay left in the sun. You can feel new organs forming inside, pressing against ribs that are bending outward.

AVOID: mirrors, reflections, seeing yourself, doppelgangers, copies
EMPHASIZE: Tactile sensations, internal changes, bone movement, joint addition, texture shifts, the feeling of becoming plural from within""",
            ["Physical transformation", "Flesh horror", "Loss of form", "Tactile wrongness", "Internal metamorphosis"]
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
        Scenario(
            "SOUND PRISON",
            "sound_prison",
            "Trapped by sound, silence is deadly",
            "You wake to absolute silence. Moving creates sound. Every sound draws something closer. You hear breathing that isn't yours. The silence between your heartbeats feels dangerous. You must make noise to survive, but noise summons them.",
            ["Audio horror", "Sound as danger", "Silent predator", "Acoustic awareness"]
        ),
        Scenario(
            "INFECTION POINT",
            "infection",
            "Something is spreading through you",
            "Your veins are black. You can see them spreading under your skin like cracks in ice. It doesn't hurt. That's the worst part. You feel... better. Stronger. Different. The infection wants something. You can almost hear what it's saying.",
            ["Body invasion", "Transformation", "Loss of self", "Parasitic horror"]
        ),
        Scenario(
            "WITNESSED",
            "witnessed",
            "Every choice is being recorded and judged",
            "You notice the camera. Then another. Then dozens. Red lights blinking. Recording everything. Someone is watching. Taking notes. Judging. You don't know who or why. Every movement feels like a test you're failing.",
            ["Surveillance horror", "Performance anxiety", "Judgment", "Unseen watchers"]
        ),
        Scenario(
            "BACKWARDS BIRTH",
            "backwards_birth",
            "You're being un-born, regression into nothing",
            "You're getting smaller. Younger. Your memories are disappearing in reverse chronological order. You remember yesterday clearly. Last year is fuzzy. Childhood is gone. Soon you won't remember language. Then thought. Then nothing.",
            ["Regression", "Memory loss", "Identity erosion", "Temporal reversal"]
        ),
        Scenario(
            "SHADOW DEBT",
            "shadow_debt",
            "Your shadow is collecting what you owe",
            "Your shadow doesn't match your movements anymore. It's doing other things. Taking things. It whispers that you owe a debt. You don't remember owing anything. Your shadow remembers. It's here to collect.",
            ["Shadow horror", "Debt", "Doppelganger", "Supernatural obligation"]
        ),
        Scenario(
            "WORD VIRUS",
            "word_virus",
            "Certain words are dangerous, language is breaking",
            "Don't say—[REDACTED]. The word is gone. You try to remember it but there's a blank space in your mind. More words are disappearing. Communication is fracturing. Soon you won't be able to think. Language is the infection.",
            ["Linguistic horror", "Communication breakdown", "Memetic hazard", "Conceptual erasure"]
        ),
        Scenario(
            "RECURSIVE WITNESS",
            "recursive",
            "You're watching yourself watching yourself",
            "You see yourself across the room. They're looking at you. Behind them, another you. And another. Infinite regression. Each iteration is slightly different. Slightly wrong. One of them isn't you. You don't know which.",
            ["Infinite regression", "Mirror horror", "Self-observation", "Iteration terror"]
        ),
        Scenario(
            "FLESH ARCHITECTURE",
            "flesh_architecture",
            "The building is made of meat and it's alive",
            "The walls are warm. Pulsing. You realize you're inside something enormous and living. The floor breathes. Doors are sphincters. The building digests those who stay too long. It's hungry. You're inside its stomach.",
            ["Organic horror", "Living structure", "Digestive threat", "Meat maze"]
        ),
        Scenario(
            "PROBABILITY COLLAPSE",
            "probability",
            "Reality is splitting with every choice",
            "You can see them all. Every version of yourself making different choices. The realities are stacked, translucent, overlapping. You're all of them simultaneously. Each decision splits you further. You're becoming infinite and losing definition.",
            ["Quantum horror", "Choice paralysis", "Reality splitting", "Multiverse awareness"]
        ),
        Scenario(
            "DEBT COLLECTOR",
            "debt_collector",
            "Something demands payment for living",
            "The invoice appears in your hand. For: ONE LIFE LIVED. Amount: EVERYTHING. Due: NOW. The collector stands at the door. Tall, wrong, patient. You've been borrowing time. The interest is steep. Payment will be extracted.",
            ["Supernatural debt", "Life collection", "Extraction horror", "Cosmic billing"]
        ),
        Scenario(
            "STATIC PERSON",
            "static_person",
            "You're becoming television static",
            "Your fingers are dissolving into static. Visual noise where your hands should be. The static spreads. Soon you'll be nothing but white noise and interference patterns. You can hear voices in the static. They sound like you.",
            ["Signal degradation", "Static transformation", "Broadcast horror", "Signal/noise"]
        ),
        Scenario(
            "THE AUDITION",
            "audition",
            "This is a test for something terrible",
            "You're in a waiting room. Others are called before you. They don't come back. Your number approaches. You don't know what you're auditioning for. You don't remember signing up. But if you leave, they'll know you failed.",
            ["Test anxiety", "Unknown evaluation", "Elimination horror", "Performance dread"]
        ),
        Scenario(
            "NEGATIVE SPACE",
            "negative_space",
            "You exist in the space between things",
            "You're not in a place. You're in the absence of place. The gaps between atoms. The silence between sounds. Negative space given consciousness. You can see reality from the outside. It's thin. Fragile. Temporary.",
            ["Void existence", "Between-state", "Absence horror", "Gap consciousness"]
        ),
        Scenario(
            "CONSENSUS REALITY",
            "consensus",
            "Reality only exists when observed",
            "You blink. The room changes. Everything exists only while you're looking at it. Turn away and it becomes undefined. The world behind you is pure probability. You're the only thing holding reality together. If you close your eyes too long...",
            ["Observer effect", "Reality maintenance", "Quantum observation", "Existence burden"]
        ),
        Scenario(
            "ANCESTRAL MEMORY",
            "ancestral",
            "You remember lives you never lived",
            "You died in 1847. No wait, you're alive now. You remember burning at the stake. You remember the trenches. You remember being eaten by something that doesn't exist yet. These aren't dreams. They're memories. Every ancestor is inside you, screaming.",
            ["Genetic memory", "Historical trauma", "Inherited horror", "Past life bleeding"]
        ),
        Scenario(
            "ELEVATOR DESCENT",
            "elevator_descent",
            "Descending past floors that shouldn't exist",
            "The elevator passes floor -47. You pressed 'Lobby'. The descent continues. -89. -134. The numbers accelerate. The elevator cable groans. You're going somewhere buildings don't reach. The doors will open eventually. You don't want to see what's there.",
            ["Vertical horror", "Impossible depth", "Mechanical descent", "Underground revelation"]
        ),
        Scenario(
            "UNDERWATER PRESSURE",
            "underwater_pressure",
            "Drowning in slow motion",
            "Water fills the room. Ankle deep. Knee deep. Waist deep. The doors are sealed. The windows won't break. You have time to think about drowning. To calculate how many breaths remain. To understand exactly how you'll die. The water is patient.",
            ["Slow drowning", "Rising water", "Calculated death", "Liquid pressure"]
        ),
        Scenario(
            "RADIO STATIC",
            "radio_static",
            "Voices in white noise",
            "The radio won't turn off. Static fills the room. But there are words in the noise. Your name. Instructions. Warnings. The static knows things about you. It's trying to tell you something. Or trying to become you. The volume increases.",
            ["Audio horror", "Signal intrusion", "Voice manifestation", "Static communication"]
        ),
        Scenario(
            "MANNEQUIN ROOM",
            "mannequin_room",
            "Surrounded by figures that move when unseen",
            "The department store closed hours ago. You're locked in. The mannequins surround you. Plastic faces, frozen smiles. But they're closer than before. You didn't see them move. You never see them move. But they're always closer. One is wearing your jacket.",
            ["Weeping angel horror", "Unseen movement", "Plastic people", "Retail nightmare"]
        ),
        Scenario(
            "WRONG REFLECTION",
            "wrong_reflection",
            "Your reflection has different plans",
            "The mirror shows you. But wrong. It moves a second late. Or a second early. It's making different choices. Reaching for different things. Its expression doesn't match yours. You realize: it's not your reflection. You're its reflection. It's been the real one all along.",
            ["Mirror horror", "Reflection autonomy", "Identity theft", "Glass boundary"]
        ),
        Scenario(
            "TEETH FALLING",
            "teeth_falling",
            "Your body is betraying you piece by piece",
            "Your tooth comes loose. Then another. They fall like rain. Your fingers next—nails peeling, skin sloughing. You're coming apart. Not dying. Disassembling. The pieces are still alive, still you. You're becoming a pile of conscious fragments. Each piece still feels.",
            ["Body horror", "Disassembly", "Piece-by-piece", "Conscious fragments"]
        ),
        Scenario(
            "BACKWARDS SPEECH",
            "backwards_speech",
            "Everyone speaks in reverse and expects you to understand",
            "They're all speaking backwards. Reversed syllables, inverted meaning. But they expect you to understand. They're getting frustrated with your confusion. You're the one speaking wrong. You've always been speaking wrong. The world has been patient with your defect. That patience is ending.",
            ["Language horror", "Communication breakdown", "Reverse speech", "Linguistic isolation"]
        ),
        Scenario(
            "MEAT LOCKER",
            "meat_locker",
            "Trapped in cold storage with hanging carcasses",
            "The meat locker door closes. Locks. The temperature drops. Hanging carcasses surround you. Beef. Pork. Something else. Something that looks almost human. Almost. The cold seeps in. You have hours before hypothermia. The meat watches with absent eyes.",
            ["Cold horror", "Meat storage", "Hypothermia", "Carcass company"]
        ),
        Scenario(
            "INSECT COLONY",
            "insect_colony",
            "Discovering you're part of something larger",
            "You feel them under your skin. Moving. Building. You're not infested. You're housing. A colony. They've been there for years. You're their world. They're expanding. Soon they'll need more space. They're considering your brain. The queen is already there.",
            ["Parasitic horror", "Body colony", "Insect architecture", "Internal infestation"]
        ),
        Scenario(
            "STATIC FIGURE",
            "static_figure",
            "Something stands perfectly still in every room",
            "It's in the corner. Perfectly still. Human-shaped. Watching. You leave the room. It's in the next room. Same corner. Same position. Same watching. You run. Every room. Every corner. Always there first. Always watching. It's never moved. It's always been there. Waiting.",
            ["Omnipresent entity", "Still watcher", "Corner horror", "Motionless pursuit"]
        ),
    ]
    
    # 20 thematic seeds (conceptual constraints for AI creativity)
    THEMES = [
        Theme(
            "Velocity Focus",
            "velocity",
            "Constant motion, time pressure, no pauses",
            "Keep the protagonist moving. Clock is always ticking. No safe stops.",
            ["Chase sequences", "Time limits", "Breathless pacing", "No respite"]
        ),
        Theme(
            "Liquid Reality",
            "liquid",
            "Everything flows, nothing is solid",
            "Solid things melt. Boundaries are permeable. Reality has surface tension but no structure.",
            ["Melting", "Fluidity", "Boundary dissolution", "State changes"]
        ),
        Theme(
            "Arithmetic Horror",
            "arithmetic",
            "Numbers are wrong, math doesn't work",
            "1+1≠2. Counting fails. Quantities shift. Mathematical rules break down.",
            ["Wrong math", "Counting errors", "Numerical impossibility", "Quantity distortion"]
        ),
        Theme(
            "Inverted Sensation",
            "inverted_sensation",
            "Senses report opposite information",
            "Pain feels pleasant. Light appears as darkness. Up is down to the body.",
            ["Sensory inversion", "False signals", "Trust breakdown", "Confused perception"]
        ),
        Theme(
            "Bureaucratic Nightmare",
            "bureaucratic",
            "Trapped in infinite procedures and paperwork",
            "Forms in triplicate. Rules contradict. Everyone follows protocols that make no sense.",
            ["Red tape", "Kafka-esque", "Procedure loops", "Administrative horror"]
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
        Theme(
            "Sympathy Pain",
            "sympathy",
            "You feel what others feel, boundaries blur",
            "Other people's sensations bleed through. Their pain is yours. Their thoughts intrude. Empathy becomes horror.",
            ["Emotional bleeding", "Shared sensation", "Boundary loss", "Empathic invasion"]
        ),
        Theme(
            "Scale Distortion",
            "scale",
            "Size and distance are negotiable",
            "Things are too close or too far. Vast spaces in tiny rooms. Giants and insects trade places. Perspective is broken.",
            ["Size shifting", "Distance warping", "Perspective horror", "Scale impossibility"]
        ),
        Theme(
            "Fossil Consciousness",
            "fossil",
            "Experiencing ancient, preserved awareness",
            "You're sediment. Compressed time. Millions of years condensed. Ancient thoughts preserved in stone.",
            ["Deep time", "Geological consciousness", "Compressed existence", "Stratified memory"]
        ),
        Theme(
            "Symbiotic Merge",
            "symbiotic",
            "Two beings forced to share existence",
            "Something else lives inside you. You need each other. Boundaries dissolve. Whose thoughts are whose?",
            ["Shared body", "Dual consciousness", "Forced partnership", "Identity fusion"]
        ),
        Theme(
            "Aesthetic Corruption",
            "aesthetic",
            "Beauty becomes revolting, ugly becomes necessary",
            "Gorgeous things cause nausea. Rot appears beautiful. Aesthetic values invert. You crave the disgusting.",
            ["Beauty horror", "Value inversion", "Taste corruption", "Sensibility break"]
        ),
        Theme(
            "Echo Chamber",
            "echo",
            "Everything repeats, layers, reinforces",
            "Your words return changed. Actions echo infinitely. Each repetition amplifies. Feedback loop toward something.",
            ["Repetition", "Amplification", "Feedback loops", "Iteration escalation"]
        ),
        Theme(
            "Obligation Cascade",
            "obligation",
            "Debts and duties compound endlessly",
            "Each action creates new obligations. Help someone, owe three more. Duties multiply exponentially.",
            ["Debt spiral", "Duty multiplication", "Obligation trap", "Responsibility horror"]
        ),
        Theme(
            "Trophy Collection",
            "trophy",
            "Something is collecting parts of you",
            "Pieces go missing. Memories. Feelings. Body parts. Someone is building a collection. You're the source material.",
            ["Part theft", "Collection horror", "Systematic removal", "Identity harvesting"]
        ),
        Theme(
            "Tutorial Hell",
            "tutorial",
            "Trapped in endless instructions and learning",
            "First learn to walk. Now learn to breathe. The tutorial never ends. Each lesson spawns ten more.",
            ["Infinite learning", "Tutorial loop", "Instruction trap", "Training horror"]
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
        # Exclude last 8 scenarios (was 3, now 8 for better variety)
        available_scenarios = [
            s for s in self.SCENARIOS 
            if s.key not in self.recent_scenarios[-8:]
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
            "sound_prison": """
    ╔═══════════════════════════════╗
    ║   SOUND PRISON               ║
    ║   [silence: deadly]          ║
    ╚═══════════════════════════════╝
            """,
            "infection": """
    ╔═══════════════════════════════╗
    ║   ⚠ INFECTION SPREADING ⚠    ║
    ║   [you feel: better?]        ║
    ╚═══════════════════════════════╝
            """,
            "witnessed": """
    ╔═══════════════════════════════╗
    ║   👁 WITNESSED 👁             ║
    ║   [recording: everything]    ║
    ╚═══════════════════════════════╝
            """,
            "backwards_birth": """
    ╔═══════════════════════════════╗
    ║   ⟲ UN-BECOMING ⟲            ║
    ║   [age: reversing]           ║
    ╚═══════════════════════════════╝
            """,
            "shadow_debt": """
    ╔═══════════════════════════════╗
    ║   SHADOW DEBT                ║
    ║   [collection: imminent]     ║
    ╚═══════════════════════════════╝
            """,
            "word_virus": """
    ╔═══════════════════════════════╗
    ║   [REDACTED] VIRUS           ║
    ║   [language: failing]        ║
    ╚═══════════════════════════════╝
            """,
            "recursive": """
    ╔═══════════════════════════════╗
    ║   ∞ RECURSION ∞              ║
    ║   [self: multiplying]        ║
    ╚═══════════════════════════════╝
            """,
            "flesh_architecture": """
    ╔═══════════════════════════════╗
    ║   FLESH ARCHITECTURE         ║
    ║   [building: digesting]      ║
    ╚═══════════════════════════════╝
            """,
            "probability": """
    ╔═══════════════════════════════╗
    ║   ◊ PROBABILITY COLLAPSE ◊   ║
    ║   [reality: splitting]       ║
    ╚═══════════════════════════════╝
            """,
            "debt_collector": """
    ╔═══════════════════════════════╗
    ║   DEBT COLLECTOR             ║
    ║   [payment: due NOW]         ║
    ╚═══════════════════════════════╝
            """,
            "static_person": """
    ╔═══════════════════════════════╗
    ║   ▓▒░ STATIC PERSON ░▒▓      ║
    ║   [signal: degrading]        ║
    ╚═══════════════════════════════╝
            """,
            "audition": """
    ╔═══════════════════════════════╗
    ║   THE AUDITION               ║
    ║   [your number: approaching] ║
    ╚═══════════════════════════════╝
            """,
            "negative_space": """
    ╔═══════════════════════════════╗
    ║   NEGATIVE SPACE             ║
    ║   [existence: between]       ║
    ╚═══════════════════════════════╝
            """,
            "consensus": """
    ╔═══════════════════════════════╗
    ║   CONSENSUS REALITY          ║
    ║   [observation: required]    ║
    ╚═══════════════════════════════╝
            """,
            "ancestral": """
    ╔═══════════════════════════════╗
    ║   ANCESTRAL MEMORY           ║
    ║   [past: bleeding through]   ║
    ╚═══════════════════════════════╝
            """,
            "elevator_descent": """
    ╔═══════════════════════════════╗
    ║   ↓ ELEVATOR DESCENT ↓       ║
    ║   [floor: -∞]                ║
    ╚═══════════════════════════════╝
            """,
            "underwater_pressure": """
    ╔═══════════════════════════════╗
    ║   ≈≈ UNDERWATER ≈≈           ║
    ║   [oxygen: depleting]        ║
    ╚═══════════════════════════════╝
            """,
            "radio_static": """
    ╔═══════════════════════════════╗
    ║   ▓▒░ RADIO STATIC ░▒▓       ║
    ║   [signal: intrusive]        ║
    ╚═══════════════════════════════╝
            """,
            "mannequin_room": """
    ╔═══════════════════════════════╗
    ║   MANNEQUIN ROOM             ║
    ║   [movement: unseen]         ║
    ╚═══════════════════════════════╝
            """,
            "wrong_reflection": """
    ╔═══════════════════════════════╗
    ║   ⇄ WRONG REFLECTION ⇄       ║
    ║   [identity: stolen]         ║
    ╚═══════════════════════════════╝
            """,
            "teeth_falling": """
    ╔═══════════════════════════════╗
    ║   TEETH FALLING              ║
    ║   [body: disassembling]      ║
    ╚═══════════════════════════════╝
            """,
            "backwards_speech": """
    ╔═══════════════════════════════╗
    ║   BACKWARDS SPEECH           ║
    ║   [language: reversed]       ║
    ╚═══════════════════════════════╝
            """,
            "meat_locker": """
    ╔═══════════════════════════════╗
    ║   ❄ MEAT LOCKER ❄           ║
    ║   [temperature: fatal]       ║
    ╚═══════════════════════════════╝
            """,
            "insect_colony": """
    ╔═══════════════════════════════╗
    ║   INSECT COLONY              ║
    ║   [host: you]                ║
    ╚═══════════════════════════════╝
            """,
            "static_figure": """
    ╔═══════════════════════════════╗
    ║   STATIC FIGURE              ║
    ║   [watching: always]         ║
    ╚═══════════════════════════════╝
            """,
        }
        
        return arts.get(self.current_scenario.key, f"""
    ╔═══════════════════════════════╗
    ║   {self.current_scenario.name.upper():^29} ║
    ╚═══════════════════════════════╝
        """)

