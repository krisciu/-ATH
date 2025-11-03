"""Alternative game modes triggered by mutations."""

import random
from typing import Dict, Optional, List
from enum import Enum


class GameMode(Enum):
    """Different interaction modes."""
    STANDARD = "standard"  # Normal choice-based
    FREE_TEXT = "free_text"  # Player types responses
    REVERSE_NARRATION = "reverse_narration"  # Player narrates
    WORD_PUZZLE = "word_puzzle"  # Solve puzzle to continue
    FILL_BLANK = "fill_blank"  # Fill in narrative gaps
    TIME_PRESSURE = "time_pressure"  # Timed choices
    COORDINATE_INPUT = "coordinate_input"  # Interact with ASCII art
    TEXT_PARSER = "text_parser"  # Old-school commands
    DEBUG_MODE = "debug_mode"  # Fake debug console
    CODE_EDITOR = "code_editor"  # "Edit" story code


class GameModeHandler:
    """Handles alternative interaction modes."""
    
    def __init__(self):
        """Initialize mode handler."""
        self.current_mode = GameMode.STANDARD
        self.mode_data: Dict = {}  # Mode-specific data
    
    def get_mode_for_mutation(self, mutation_key: str) -> GameMode:
        """Determine game mode for a mutation."""
        mode_map = {
            # Free-text mutations
            'open_dialogue': GameMode.FREE_TEXT,
            'confession_booth': GameMode.FREE_TEXT,
            'reality_argument': GameMode.FREE_TEXT,
            'name_horror': GameMode.FREE_TEXT,
            'interactive_narrator': GameMode.FREE_TEXT,
            'reality_negotiation': GameMode.FREE_TEXT,
            
            # Puzzle mutations
            'cipher_lock': GameMode.WORD_PUZZLE,
            'word_association': GameMode.WORD_PUZZLE,
            'memory_test': GameMode.WORD_PUZZLE,
            'pattern_recognition': GameMode.WORD_PUZZLE,
            
            # Genre-shift mutations
            'text_parser': GameMode.TEXT_PARSER,
            'detective_mode': GameMode.TEXT_PARSER,
            
            # Meta mutations
            'debug_mode': GameMode.DEBUG_MODE,
            'code_editor': GameMode.CODE_EDITOR,
            
            # Other
            'time_pressure': GameMode.TIME_PRESSURE,
            'coordinate_input': GameMode.COORDINATE_INPUT,
            'reverse_narration': GameMode.REVERSE_NARRATION,
            'fill_blank': GameMode.FILL_BLANK,
        }
        
        return mode_map.get(mutation_key, GameMode.STANDARD)
    
    def get_input_prompt(self, mode: GameMode, context: Dict) -> str:
        """Get appropriate input prompt for mode."""
        prompts = {
            GameMode.FREE_TEXT: "[Type your response]",
            GameMode.REVERSE_NARRATION: "[Describe what happens next]",
            GameMode.WORD_PUZZLE: "[Enter your answer]",
            GameMode.FILL_BLANK: "[Fill in the blanks]",
            GameMode.TIME_PRESSURE: "[Choose quickly!]",
            GameMode.COORDINATE_INPUT: "[Enter coordinates (x,y)]",
            GameMode.TEXT_PARSER: "[Enter command]",
            GameMode.DEBUG_MODE: "[debug>]",
            GameMode.CODE_EDITOR: "[edit>]",
            GameMode.STANDARD: "[Choose]",
        }
        return prompts.get(mode, "[>]")
    
    def validate_input(self, mode: GameMode, user_input: str, context: Dict) -> tuple[bool, Optional[str]]:
        """
        Validate input for current mode.
        Returns (is_valid, error_message).
        """
        if mode == GameMode.FREE_TEXT:
            if len(user_input.strip()) < 1:
                return False, "You must say something."
            return True, None
        
        elif mode == GameMode.COORDINATE_INPUT:
            # Parse x,y format
            parts = user_input.strip().split(',')
            if len(parts) != 2:
                return False, "Format: x,y (e.g., 5,3)"
            try:
                x, y = int(parts[0]), int(parts[1])
                if 0 <= x <= 20 and 0 <= y <= 20:
                    return True, None
                return False, "Coordinates must be 0-20"
            except ValueError:
                return False, "Invalid coordinates"
        
        elif mode == GameMode.WORD_PUZZLE:
            # Check if answer matches expected (stored in context)
            expected = context.get('puzzle_answer', '')
            if expected and user_input.strip().lower() == expected.lower():
                return True, None
            # Allow any input, AI will judge
            return True, None
        
        elif mode == GameMode.TEXT_PARSER:
            # Accept verb-noun commands
            words = user_input.strip().lower().split()
            if len(words) < 1:
                return False, "Enter a command (e.g., LOOK AROUND, TAKE ITEM)"
            return True, None
        
        else:
            # Most modes accept any text
            return True, None
    
    def generate_puzzle(self, puzzle_type: str) -> Dict:
        """Generate a puzzle for puzzle mode."""
        if puzzle_type == 'cipher':
            # Simple Caesar cipher
            messages = [
                ("DANGER", 3),  # Shift by 3
                ("ESCAPE", 5),
                ("TRUST NO ONE", 2),
                ("THE DOOR", 4),
            ]
            message, shift = random.choice(messages)
            
            def caesar_cipher(text, shift):
                result = []
                for char in text:
                    if char.isalpha():
                        base = ord('A')
                        shifted = (ord(char) - base + shift) % 26
                        result.append(chr(base + shifted))
                    else:
                        result.append(char)
                return ''.join(result)
            
            encrypted = caesar_cipher(message, shift)
            
            return {
                'type': 'cipher',
                'encrypted': encrypted,
                'answer': message,
                'hint': f"Each letter is shifted by {shift}",
                'display': f"Decrypt this message: {encrypted}"
            }
        
        elif puzzle_type == 'word_association':
            # Word association game
            chains = [
                (["DARK", "LIGHT", "SHADOW"], "SHADOW"),
                (["DOOR", "KEY", "LOCK"], "LOCK"),
                (["FEAR", "COURAGE", "TERROR"], "TERROR"),
                (["BLOOD", "LIFE", "DEATH"], "DEATH"),
            ]
            chain, answer = random.choice(chains)
            
            return {
                'type': 'word_association',
                'chain': chain,
                'answer': answer,
                'display': f"Complete the sequence: {' → '.join(chain[:-1])} → ?"
            }
        
        elif puzzle_type == 'pattern':
            # Pattern recognition
            patterns = [
                (["2", "4", "8", "16"], "32", "doubling"),
                (["1", "1", "2", "3", "5"], "8", "fibonacci"),
                (["A", "C", "E", "G"], "I", "every other letter"),
            ]
            sequence, answer, hint = random.choice(patterns)
            
            return {
                'type': 'pattern',
                'sequence': sequence,
                'answer': answer,
                'hint': hint,
                'display': f"What comes next? {', '.join(sequence)}, ?"
            }
        
        else:
            # Memory test
            facts = [
                ("What color was the door?", ["red", "blue", "black"]),
                ("How many rooms have you entered?", ["1", "2", "3", "4", "5"]),
                ("What was the first thing you saw?", ["darkness", "light", "eyes", "door"]),
            ]
            question, possible_answers = random.choice(facts)
            
            return {
                'type': 'memory',
                'question': question,
                'possible_answers': possible_answers,
                'display': question
            }
    
    def generate_debug_output(self, context: Dict) -> str:
        """Generate fake debug console output."""
        char_stats = context.get('character_stats', {})
        hidden_stats = context.get('hidden_stats', {})
        choice_count = context.get('choice_count', 0)
        
        debug_lines = [
            "[DEBUG MODE ACTIVE]",
            f"story_engine.choice_count = {choice_count}",
            f"character.health = {char_stats.get('health', 100)}",
            f"character.sanity = {hidden_stats.get('sanity', 5)}",
            f"narrator.reliability = {random.randint(0, 100)}%",
            f"reality.coherence = {random.randint(0, 100)}%",
            "",
            "Available commands:",
            "  SET <variable> <value>",
            "  GET <variable>",
            "  CONTINUE",
            "  EXIT_DEBUG",
        ]
        
        return "\n".join(debug_lines)
    
    def generate_code_editor_view(self, narrative: str) -> str:
        """Generate fake code editor view of the story."""
        lines = [
            "// story_engine.cpp",
            "// Line 1047-1053",
            "",
            "void StoryEngine::generate_narrative() {",
            f'    std::string text = "{narrative[:50]}...";',
            "    // WARNING: Modifying this will alter reality",
            "    narrator.speak(text);",
            "    player.receive(text);",
            "}",
            "",
            "// [E]dit  [C]ontinue  [R]evert",
        ]
        
        return "\n".join(lines)
    
    def process_text_parser_command(self, command: str, context: Dict) -> Dict:
        """Process old-school text parser commands."""
        command = command.strip().lower()
        words = command.split()
        
        if not words:
            return {'error': "I don't understand."}
        
        verb = words[0]
        noun = ' '.join(words[1:]) if len(words) > 1 else ''
        
        # Map to standard actions
        action_map = {
            'look': 'examine',
            'examine': 'examine',
            'take': 'take',
            'get': 'take',
            'use': 'use',
            'open': 'open',
            'close': 'close',
            'go': 'move',
            'move': 'move',
            'attack': 'attack',
            'talk': 'talk',
            'speak': 'talk',
        }
        
        action = action_map.get(verb, verb)
        
        return {
            'action': action,
            'target': noun,
            'raw_command': command,
            'formatted': f"{action.upper()} {noun.upper()}" if noun else action.upper()
        }

