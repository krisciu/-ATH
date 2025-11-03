"""Core story engine with dual stat systems and state management."""

import random
from typing import Dict, List, Optional
from copy import deepcopy
from config.settings import (
    DEFAULT_CHARACTER_STATS,
    DEFAULT_HIDDEN_STATS,
    PROGRESSION_CONFIG,
    CRITICAL_EVENTS
)


class StoryEngine:
    """Manages game state, stats, and progression."""
    
    def __init__(self):
        """Initialize the story engine."""
        self.character_stats = deepcopy(DEFAULT_CHARACTER_STATS)
        self.hidden_stats = deepcopy(DEFAULT_HIDDEN_STATS)
        self.choice_count = 0
        self.choice_history: List[str] = []
        self.event_flags: List[str] = []
        self.current_narrative = ""
        self.instability_level = 0
        self.last_danger_level = 'none'  # Track for consequence feedback
        
        # Event tracking for forced progression
        self.event_timer = 0  # Forces event every 2-3 choices
        self.discoveries: List[str] = []  # Track what's been revealed
        self.active_threats: List[str] = []  # Ongoing dangers
        self.transformations: List[str] = []  # Body/reality changes
        
        # Horror concept tracking for variety
        self.horror_concepts_used: List[str] = []  # Track tropes to avoid repetition
        
        # Narrative momentum tracking for faster pacing
        self.momentum_level = 0  # Tracks narrative escalation
        self.climax_triggered = False
        self.must_end_soon = False  # Flag for forcing conclusion
    
    def process_choice(self, choice_text: str, choice_index: int) -> Dict:
        """Process a player choice and modify stats."""
        self.choice_count += 1
        self.choice_history.append(choice_text)
        
        # Store last danger level for feedback
        self.last_danger_level = 'none'
        
        # Increment event timer for forced progression
        self.event_timer += 1
        
        # Modify stats based on choice characteristics
        self._apply_choice_effects(choice_text, choice_index)
        
        # Update instability level
        self._update_instability()
        
        # Return current context for AI generation
        return self.get_context()
    
    def _apply_choice_effects(self, choice_text: str, choice_index: int):
        """Apply stat modifications based on choice content - with early game protection."""
        text_lower = choice_text.lower()
        
        # Early game protection (first 8 choices) - prevent premature endings
        early_game_multiplier = 1.0
        if self.choice_count <= 8:
            early_game_multiplier = 0.5  # Half damage/changes early on
        
        # Check for dangerous choices FIRST (consequences)
        danger_level = self._assess_choice_danger(text_lower)
        self.last_danger_level = danger_level  # Store for feedback
        self.last_damage_dealt = 0  # Track actual damage dealt
        self._apply_consequences(danger_level, text_lower)
        
        # Track if any stat changed this turn
        something_changed = False
        
        # Courage modifications - BIGGER SWINGS (with early game protection)
        if any(word in text_lower for word in ['attack', 'fight', 'confront', 'face', 'charge']):
            self._modify_hidden_stat('courage', int(random.randint(2, 4) * early_game_multiplier))
            self._modify_character_stat('strength', int(random.randint(1, 3) * early_game_multiplier))
            something_changed = True
        elif any(word in text_lower for word in ['flee', 'hide', 'retreat', 'avoid', 'run']):
            self._modify_hidden_stat('courage', int(random.randint(-4, -2) * early_game_multiplier))
            self._modify_character_stat('speed', int(random.randint(0, 2) * early_game_multiplier))
            something_changed = True
        
        # Sanity modifications - REDUCED from -3 to -2 max (with early game protection)
        if any(word in text_lower for word in ['look', 'examine', 'study', 'observe', 'stare']):
            self._modify_hidden_stat('sanity', int(random.randint(-2, -1) * early_game_multiplier))
            self._modify_hidden_stat('curiosity', int(random.randint(2, 4) * early_game_multiplier))
            something_changed = True
        
        # Curiosity modifications - BIGGER (with early game protection)
        if any(word in text_lower for word in ['open', 'read', 'touch', 'take', 'investigate']):
            self._modify_hidden_stat('curiosity', int(random.randint(2, 4) * early_game_multiplier))
            self._modify_hidden_stat('trust', int(random.randint(-2, 0) * early_game_multiplier))
            something_changed = True
        
        # Trust modifications - BIGGER (with early game protection)
        if any(word in text_lower for word in ['listen', 'follow', 'trust', 'believe', 'accept']):
            self._modify_hidden_stat('trust', int(random.randint(1, 3) * early_game_multiplier))
            something_changed = True
        elif any(word in text_lower for word in ['ignore', 'refuse', 'doubt', 'question', 'reject']):
            self._modify_hidden_stat('trust', int(random.randint(-3, -1) * early_game_multiplier))
            self._modify_hidden_stat('courage', int(random.randint(0, 2) * early_game_multiplier))
            something_changed = True
        
        # NO PASSIVE DECAY - stats only change from meaningful choices and AI consequences
        # This gives players more agency and makes stat changes feel earned/deserved
    
    def _modify_hidden_stat(self, stat: str, change: int):
        """Modify a hidden stat (clamped 0-10)."""
        if stat in self.hidden_stats:
            self.hidden_stats[stat] = max(0, min(10, self.hidden_stats[stat] + change))
    
    def _modify_character_stat(self, stat: str, change: int):
        """Modify a character stat."""
        if stat in self.character_stats:
            if stat == 'health':
                # Health clamped to 0-max_health
                self.character_stats[stat] = max(
                    0, 
                    min(self.character_stats['max_health'], self.character_stats[stat] + change)
                )
            else:
                # Other stats clamped to 1-10
                self.character_stats[stat] = max(1, min(10, self.character_stats[stat] + change))
    
    def _update_instability(self):
        """Update instability level based on progression."""
        # Choice-based progression
        threshold = PROGRESSION_CONFIG['instability_choice_threshold']
        self.instability_level = self.choice_count // threshold
        
        # Stat-based modifiers
        if self.hidden_stats['sanity'] < 3:
            self.instability_level += 2
        if self.hidden_stats['trust'] < 2:
            self.instability_level += 1
        
        # Event-based spikes
        for event in self.event_flags:
            if event in CRITICAL_EVENTS:
                self.instability_level += 1
    
    def trigger_event(self, event_name: str):
        """Trigger a critical event that affects instability."""
        if event_name not in self.event_flags:
            self.event_flags.append(event_name)
            self._update_instability()
    
    def get_visual_intensity(self) -> str:
        """Get current visual effect intensity level."""
        if self.choice_count >= PROGRESSION_CONFIG['reality_collapse_at']:
            return 'collapsed'
        elif self.choice_count >= PROGRESSION_CONFIG['major_breakdown_at']:
            return 'breaking'
        elif self.choice_count >= PROGRESSION_CONFIG['minor_breakdown_at']:
            return 'disturbed'
        elif self.instability_level > 0:
            return 'unsettled'
        return 'stable'
    
    def get_context(self) -> Dict:
        """Get current context for AI generation."""
        # Update momentum before returning context
        self.update_momentum()
        
        return {
            'character_stats': self.character_stats.copy(),
            'hidden_stats': self.hidden_stats.copy(),
            'choice_count': self.choice_count,
            'previous_choice': self.choice_history[-1] if self.choice_history else 'BEGIN',
            'recent_narrative': self.current_narrative,
            'instability_level': self.instability_level,
            'visual_intensity': self.get_visual_intensity(),
            'event_flags': self.event_flags.copy(),
            # Event tracking for forced progression
            'event_urgency': self.event_timer >= 2,  # Signal AI to make something happen
            'recent_discoveries': self.discoveries[-3:] if self.discoveries else [],
            'active_threats': self.active_threats.copy(),
            'transformations': self.transformations.copy(),
            # Horror concept diversity tracking
            'horror_concepts_used': self.horror_concepts_used.copy(),
            'concept_diversity_prompt': self.get_concept_diversity_prompt(),
            # Narrative momentum for faster pacing
            'momentum_level': self.momentum_level,
            'momentum_prompt': self.get_momentum_prompt_modifier(),
            'must_end_soon': self.must_end_soon,
        }
    
    def set_narrative(self, narrative: str):
        """Update current narrative text."""
        self.current_narrative = narrative
    
    def apply_ai_consequences(self, consequences: Dict[str, int]):
        """
        Apply stat changes generated by the AI.
        This ensures consequences match the narrative perfectly.
        """
        # Apply health change
        if 'health' in consequences and consequences['health'] != 0:
            self._modify_character_stat('health', consequences['health'])
            # Track damage for feedback
            if consequences['health'] < 0:
                self.last_damage_dealt = abs(consequences['health'])
                # Determine danger level based on damage amount
                if abs(consequences['health']) >= 30:
                    self.last_danger_level = 'extreme'
                elif abs(consequences['health']) >= 20:
                    self.last_danger_level = 'high'
                elif abs(consequences['health']) >= 10:
                    self.last_danger_level = 'medium'
                else:
                    self.last_danger_level = 'low'
            else:
                self.last_damage_dealt = 0
                self.last_danger_level = 'none'
        
        # Apply sanity change
        if 'sanity' in consequences and consequences['sanity'] != 0:
            self._modify_hidden_stat('sanity', consequences['sanity'])
        
        # Apply courage change
        if 'courage' in consequences and consequences['courage'] != 0:
            self._modify_hidden_stat('courage', consequences['courage'])
    
    def record_event(self, event_type: str, description: str):
        """Record an event occurrence and reset timer."""
        if event_type == "discovery":
            self.discoveries.append(description)
        elif event_type == "threat":
            if description not in self.active_threats:
                self.active_threats.append(description)
        elif event_type == "transformation":
            self.transformations.append(description)
        
        # Reset event timer
        self.event_timer = 0
    
    def detect_horror_concepts(self, narrative: str):
        """Detect common horror tropes in narrative to track variety."""
        concepts = {
            'doppelganger': ['doppelganger', 'double', 'twin', 'copy', 'duplicate', 'reflection that moves', 'other you', 'another you', 'identical'],
            'mirror': ['mirror', 'reflection', 'glass'],
            'pursuit': ['chasing', 'following', 'pursuing', 'hunting you'],
            'transformation': ['changing', 'transforming', 'morphing', 'becoming'],
            'voices': ['voices', 'whispers', 'speaking', 'calling'],
            'darkness': ['darkness', 'shadow', 'dark', 'blackness'],
            'eyes': ['eyes watching', 'staring', 'gaze', 'observing'],
            'doors': ['door', 'doorway', 'entrance', 'threshold'],
            'time_loop': ['again', 'repeat', 'before', 'déjà vu', 'happened before'],
            'body_horror': ['flesh', 'skin', 'bones', 'organs', 'blood'],
            'isolation': ['alone', 'empty', 'abandoned', 'no one'],
            'fragmentation': ['pieces', 'fragments', 'breaking apart', 'dissolving'],
        }
        
        narrative_lower = narrative.lower()
        for concept, keywords in concepts.items():
            if any(keyword in narrative_lower for keyword in keywords):
                if concept not in self.horror_concepts_used:
                    self.horror_concepts_used.append(concept)
    
    def get_concept_diversity_prompt(self) -> str:
        """Generate prompt section encouraging conceptual variety."""
        if not self.horror_concepts_used:
            return ""
        
        # Build positive steering (what to explore) rather than negative (what to avoid)
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
        
        # If we've used many concepts, suggest fresh angles
        if len(self.horror_concepts_used) >= 3:
            suggestions = [c for c in unused_concepts if random.random() < 0.4][:3]
            if suggestions:
                return f"\n\nFRESH ANGLES TO EXPLORE: Consider incorporating: {', '.join(suggestions)}\nALREADY EXPLORED THIS SESSION: {', '.join(self.horror_concepts_used[-5:])} - find new ways to unsettle"
        
        return ""
    
    def update_momentum(self):
        """Track narrative momentum to force climax - ensures faster pacing."""
        # Momentum increases with choices, danger, low stats
        if self.choice_count >= 12:
            self.momentum_level += 2
        elif self.choice_count >= 8:
            self.momentum_level += 1
        
        if self.character_stats['health'] < 30:
            self.momentum_level += 2
        
        if self.hidden_stats['sanity'] < 3:
            self.momentum_level += 3
        
        # Critical momentum = must end soon
        if self.momentum_level >= 15 and not self.climax_triggered:
            self.climax_triggered = True
            self.must_end_soon = True
        
        return self.momentum_level
    
    def get_momentum_prompt_modifier(self) -> str:
        """Add momentum-based urgency to AI prompts - SUBTLE, no telegraphing."""
        if self.must_end_soon:
            return "\n\nRaise stakes significantly. Make choices matter more."
        elif self.momentum_level >= 10:
            return "\n\nIncrease tension and consequences."
        elif self.momentum_level >= 5:
            return "\n\nBegin escalating stakes."
        return ""
    
    def detect_trap_choice(self, choice_text: str) -> bool:
        """Detect if player chose an obvious trap/bad choice (classic CYOA mechanic)."""
        trap_indicators = [
            'ignore warning', 'ignore the warning', 'ignore all',
            'obviously', 'despite', 'anyway', 'against',
            'clearly dangerous', 'strange liquid', 'unknown substance',
            'trust the', 'believe the', 'follow the monster',
            'touch the', 'grab the', 'drink the', 'eat the',
            'step into the trap', 'walk into',
        ]
        
        text_lower = choice_text.lower()
        
        # Check for trap indicators
        for indicator in trap_indicators:
            if indicator in text_lower:
                return True
        
        # Check for parenthetical warnings being ignored
        if '(' in choice_text and ')' in choice_text:
            # Extract parenthetical content
            paren_content = choice_text[choice_text.find('(')+1:choice_text.find(')')].lower()
            warning_words = ['poison', 'danger', 'trap', 'dead', 'death', 'hurt', 'bad', 'kill', 'fatal']
            if any(word in paren_content for word in warning_words):
                return True
        
        return False
    
    def apply_trap_consequences(self):
        """Apply severe consequences for choosing obvious trap choices."""
        # Immediate heavy damage
        self._modify_character_stat('health', random.randint(-40, -25))  # Massive damage
        self._modify_hidden_stat('sanity', random.randint(-3, -1))
        
        # Set flag for forced bad outcome
        self.event_flags.append('TRAP_TRIGGERED')
        self.must_end_soon = True  # Force ending soon after trap
        self.momentum_level += 5  # Jump momentum
    
    def _assess_choice_danger(self, choice_text: str) -> str:
        """
        Assess danger level of a choice.
        Returns: 'none', 'low', 'medium', 'high', 'extreme'
        """
        # Keywords indicating danger levels
        extreme_keywords = ['attack', 'charge', 'confront directly', 'fight']
        high_keywords = ['investigate', 'touch', 'open', 'enter', 'confront']
        medium_keywords = ['explore', 'examine closely', 'follow', 'pursue']
        low_keywords = ['look', 'listen', 'observe', 'cautious']
        
        # Instant death trap check (1-2% for obvious traps)
        if any(word in choice_text for word in ['obvious trap', 'clearly dangerous', 'suicide']):
            if random.random() < 0.015:  # 1.5% chance
                return 'instant_death'
        
        # Check keywords
        if any(word in choice_text for word in extreme_keywords):
            return 'extreme'
        elif any(word in choice_text for word in high_keywords):
            return 'high'
        elif any(word in choice_text for word in medium_keywords):
            return 'medium'
        elif any(word in choice_text for word in low_keywords):
            return 'low'
        
        return 'none'
    
    def _apply_consequences(self, danger_level: str, choice_text: str):
        """Apply health and sanity consequences based on danger."""
        # Scale danger based on progression
        progression_multiplier = 1.0
        if self.choice_count > 20:
            progression_multiplier = 1.5  # Late game is more dangerous
        elif self.choice_count > 10:
            progression_multiplier = 1.2  # Mid game moderately dangerous
        
        # Apply consequences based on danger level
        if danger_level == 'instant_death':
            # Instant death trap triggered
            self.character_stats['health'] = 0
            self.trigger_event('instant_death_trap')
            return
        
        elif danger_level == 'extreme':
            # 20-30 health loss
            damage = random.randint(20, 30)
            damage = int(damage * progression_multiplier)
            self._modify_character_stat('health', -damage)
            self._modify_hidden_stat('sanity', random.randint(-2, -1))
            self.last_damage_dealt = damage  # Track for feedback
        
        elif danger_level == 'high':
            # 15-25 health loss
            damage = random.randint(15, 25)
            damage = int(damage * progression_multiplier)
            self._modify_character_stat('health', -damage)
            self._modify_hidden_stat('sanity', random.randint(-1, 0))
            self.last_damage_dealt = damage  # Track for feedback
        
        elif danger_level == 'medium':
            # 10-20 health loss
            damage = random.randint(10, 20)
            damage = int(damage * progression_multiplier)
            self._modify_character_stat('health', -damage)
            self.last_damage_dealt = damage  # Track for feedback
        
        elif danger_level == 'low':
            # 5-10 health loss
            damage = random.randint(5, 10)
            if self.choice_count > 10:
                damage = int(damage * progression_multiplier)
            self._modify_character_stat('health', -damage)
            self.last_damage_dealt = damage  # Track for feedback
        
        # Random sanity drain (paranoia, witnessing horror)
        if 'horror' in choice_text or 'witness' in choice_text:
            self._modify_hidden_stat('sanity', random.randint(-2, -1))
        
        # Paranoid choices reduce sanity
        if 'paranoid' in choice_text or 'suspicious' in choice_text:
            self._modify_hidden_stat('sanity', -1)
    
    def get_consequence_feedback(self, danger_level: str) -> Optional[str]:
        """
        Get narrator feedback about consequences taken.
        Only shows feedback when actual damage was dealt from a dangerous choice.
        """
        # Don't show feedback if no danger or no actual damage was dealt
        if danger_level == 'none' or not hasattr(self, 'last_damage_dealt') or self.last_damage_dealt == 0:
            return None
        
        # Only show feedback if there was actual damage from the choice
        feedbacks = {
            'extreme': [
                "(that was unwise)",
                "(brave, but stupid)",
                "You pay the price.",
                "(ouch)",
            ],
            'high': [
                "(that cost you)",
                "Your health suffers.",
                "(was it worth it?)",
                "Pain follows."
            ],
            'medium': [
                "(careful...)",
                "That hurt.",
                "(consequences)",
            ],
            'low': [
                "(you felt that)",
                "A small price.",
            ]
        }
        
        if danger_level in feedbacks and self.last_damage_dealt > 0:
            return random.choice(feedbacks[danger_level])
        
        return None
    
    def is_game_over(self) -> tuple[bool, Optional[str]]:
        """Check if game has ended."""
        # Death
        if self.character_stats['health'] <= 0:
            return True, "TERMINATION: Biological systems offline."
        
        # Sanity collapse
        if self.hidden_stats['sanity'] <= 0:
            return True, "TERMINATION: Coherence failure. You are no longer you."
        
        # Maximum choices reached (story exhaustion)
        if self.choice_count >= 30:
            return True, "TERMINATION: The story has run out of itself."
        
        return False, None
    
    def get_state_summary(self) -> Dict:
        """Get complete state for ghost memory saving."""
        return {
            'character_stats': self.character_stats,
            'hidden_stats': self.hidden_stats,
            'choice_count': self.choice_count,
            'choice_history': self.choice_history,
            'event_flags': self.event_flags,
            'instability_level': self.instability_level
        }

