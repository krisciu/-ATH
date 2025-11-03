# Concept Diversity System

## The Problem: Horror Trope Gravity Wells

Certain horror concepts are so compelling that AI naturally gravitates toward them even when given different starting prompts:

- **Doppelgangers** (mirrors, twins, copies)
- **Darkness** (shadows, blackness)
- **Doors** (thresholds, portals)
- **Eyes watching**
- **Whispers/voices**

This created repetitive experiences where Body Horror → doppelgangers, Falling Forever → doppelgangers, etc.

## The Solution: Active Concept Tracking & Positive Steering

Rather than banning specific concepts (we love doppelgangers!), we implemented a **diversity encouragement system** that tracks what's been used and actively steers toward unexplored territory.

---

## How It Works

### 1. Horror Concept Detection (`story_engine.py`)

After each narrative is generated, the system automatically detects which horror tropes were used:

```python
def detect_horror_concepts(self, narrative: str):
    """Detect common horror tropes in narrative to track variety."""
    concepts = {
        'doppelganger': ['double', 'twin', 'copy', 'duplicate', 'other you'],
        'mirror': ['mirror', 'reflection', 'glass'],
        'pursuit': ['chasing', 'following', 'hunting you'],
        'transformation': ['changing', 'transforming', 'morphing'],
        'voices': ['voices', 'whispers', 'calling'],
        'darkness': ['darkness', 'shadow', 'dark'],
        'eyes': ['eyes watching', 'staring', 'gaze'],
        'doors': ['door', 'doorway', 'entrance'],
        'time_loop': ['again', 'repeat', 'déjà vu'],
        'body_horror': ['flesh', 'skin', 'bones', 'organs'],
        'isolation': ['alone', 'empty', 'abandoned'],
        'fragmentation': ['pieces', 'fragments', 'dissolving'],
    }
```

**Tracks**: Which tropes have appeared this session

### 2. Positive Steering (`story_engine.py`)

Once 3+ concepts have been used, the system generates **positive suggestions** for fresh angles:

```python
def get_concept_diversity_prompt(self) -> str:
    """Generate prompt section encouraging conceptual variety."""
    unused_concepts = [
        'geometric impossibility', 'mathematical horror', 'sensory confusion',
        'bureaucratic nightmare', 'linguistic breakdown', 'archaeological dread',
        'chemical transformation', 'quantum uncertainty', 'biological invasion',
        'architectural wrongness', 'temporal paradox', 'gravity distortion',
        'sound-based horror', 'tactile wrongness', 'olfactory nightmare',
        'pressure changes', 'temperature extremes', 'spatial compression',
        'crowd horror', 'absence of expected', 'too many of something',
        'scale distortion', 'texture horror', 'pattern recognition failure'
    ]
    
    # Suggests 3 random fresh angles to explore
```

**Returns**: Positive prompt additions like:
```
FRESH ANGLES TO EXPLORE: Consider incorporating: quantum uncertainty, 
tactile wrongness, scale distortion

ALREADY EXPLORED THIS SESSION: doppelganger, mirrors, darkness - find new ways to unsettle
```

### 3. AI Integration (`config/prompts.py`)

This diversity prompt is automatically added to every scene generation request:

```python
STYLE INSTRUCTIONS: {style_instructions}{revelation_hint}

{scenario_constraints}{concept_diversity}

PROGRESSION REQUIREMENTS:
- Every 2-3 choices: Major event must occur
```

### 4. Explicit Scenario Steering (`scenario_generator.py`)

Some scenarios now include explicit AVOID/EMPHASIZE directives:

**Before:**
```python
Scenario(
    "BODY HORROR AWAKENING",
    "body_horror",
    "Your body is transforming",
    "Your hand looks wrong. Too many joints...",
    ["Physical transformation", "Flesh horror"]
)
```

**After:**
```python
Scenario(
    "BODY HORROR AWAKENING",
    "body_horror",
    "Your body is transforming",
    """Your hand looks wrong. Too many joints. The skin ripples like water...
    
AVOID: mirrors, reflections, seeing yourself, doppelgangers, copies
EMPHASIZE: Tactile sensations, internal changes, bone movement, joint addition,
           texture shifts, the feeling of becoming plural from within""",
    ["Physical transformation", "Flesh horror", "Internal metamorphosis"]
)
```

---

## Design Philosophy: Positive Reinforcement

### ❌ What We DON'T Do (and why):

**Hard-coded bans:**
```
"Never mention doppelgangers"  ← Too restrictive
"Avoid mirrors completely"     ← Kills legitimate scenarios
```

**Negative-only feedback:**
```
"Don't use X, Y, Z"  ← AI doesn't know what TO do instead
```

### ✅ What We DO:

**Positive suggestions:**
```
"Try: quantum uncertainty, tactile wrongness, crowd horror"  ← Gives alternatives
"Emphasize: internal changes, texture shifts"                ← Specific directions
```

**Context-aware steering:**
- If Mirror World scenario → doppelgangers are EXPECTED
- If Body Horror scenario → steer toward internal/tactile, away from visual/reflection

**Emergent variety:**
- Tracking means each session naturally explores different concepts
- AI has creative freedom within gentle guidance
- Nothing is banned, just encouraged to diversify

---

## Example Flow

### Session Start (Body Horror)
```
Opening: "Your hand looks wrong. Too many joints..."
Concepts detected: [body_horror]
Diversity prompt: (none yet, need 3+ concepts)
```

### Choice 2
```
AI generates: "You feel bones shifting under skin..."
Concepts detected: [body_horror, transformation]
Diversity prompt: (still accumulating)
```

### Choice 4
```
AI generates: "Behind you, another version of yourself emerges..."
Concepts detected: [body_horror, transformation, doppelganger]
Diversity prompt: NOW ACTIVATES
```

### Choice 5+
```
AI receives:
"FRESH ANGLES TO EXPLORE: quantum uncertainty, olfactory nightmare, crowd horror
 ALREADY EXPLORED: body_horror, transformation, doppelganger - find new ways"

AI generates: "The room fills with the smell of copper and ozone. Your sense of 
              up and down inverts..."
              
Concepts: [body_horror, transformation, doppelganger, sensory_confusion]
```

Session continues with increasing variety as more concepts are explored.

---

## Why This Works

1. **Tracks actual usage**, not assumptions
2. **Suggests alternatives**, doesn't ban concepts
3. **Specific guidance**, not vague requests
4. **Respects scenario intent** (Mirror World can have doppelgangers)
5. **Accumulative effect** - the more you play, the more diverse it gets
6. **AI maintains creativity** - it's guided, not constrained

---

## Creative Solutions Beyond Code

The system also includes:

**24 "Fresh Angle" Suggestions:**
- Geometric impossibility
- Mathematical horror (2+2=5 type dread)
- Sensory confusion (taste colors, hear textures)
- Bureaucratic nightmare (Kafka-style endless forms)
- Linguistic breakdown (words stop meaning things)
- Quantum uncertainty (multiple states at once)
- Crowd horror (too many people)
- Absence of expected (no shadows, no reflections where there should be)
- Pattern recognition failure (can't parse what you're seeing)
- And 15 more...

Each session will naturally discover 3-5 of these based on what hasn't been used yet.

---

## Result

**Before:**
- Body Horror → see doppelganger in mirror
- Falling Forever → meet doppelganger falling beside you
- Mirror World → evil doppelganger (appropriate here!)

**After:**
- Body Horror → feel bones multiplying internally, tactile wrongness
- Falling Forever → gravity inverts randomly, spatial confusion
- Mirror World → evil doppelganger (still appropriate!)
- Mid-session: AI explores quantum states, mathematical impossibilities, crowd horror, etc.

**You love doppelgangers → they still appear!**
**But not in EVERY scenario, especially when they don't fit the theme.**

---

## Future Enhancements

Could expand to:
- Track concepts across sessions (in ghost memory)
- Suggest concepts that pair well together
- Weight suggestions based on scenario theme
- Track which combinations lead to best stories
- Add player-specific concept preferences

For now, the system elegantly solves the problem: **creative variety through positive steering, not restrictive banning**.

