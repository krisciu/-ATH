#!/usr/bin/env python3
"""
Terminal Story Engine - A reality-bending CYOA experience.

The story begins when you run this file. There is no menu. No pause.
The terminal becomes the story, and the story knows it's being told.
"""

import sys
import os
import random
import time
from typing import Dict
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

from engine.story_engine import StoryEngine
from engine.ai_adapter import AIAdapter
from engine.narrator import Narrator
from engine.renderer import Renderer
from engine.typography import TypographyEngine
from engine.session import SessionManager
from engine.truth_tracker import TruthTracker
from engine.loading_effects import ThematicLoader
from engine.endings import EndingsManager
from engine.scenario_generator import ScenarioGenerator
from engine.mutations import MutationManager, apply_mutation_to_choices, apply_mutation_to_narrative, handle_special_mutations
from config.prompts import get_revelation_modifiers


class Game:
    """Main game controller."""
    
    def __init__(self):
        """Initialize all game systems."""
        try:
            self.story = StoryEngine()
            self.ai = AIAdapter()
            self.narrator = Narrator()
            self.renderer = Renderer()
            self.typography = TypographyEngine()
            self.session = SessionManager()
            self.truth = TruthTracker()
            self.loader = ThematicLoader(self.renderer.console)
            self.endings = EndingsManager()
            self.scenario_gen = ScenarioGenerator(self.session.ghost_memory)
            self.mutations = MutationManager()
            
            # Track mutations for ghost memory
            self.mutations_this_session = []
            
            # Load truth state from ghost memory
            truth_state = self.session.get_truth_state()
            if truth_state:
                self.truth.load_state(truth_state)
        except ValueError as e:
            print(f"\nERROR: {e}")
            print("\nPlease create a .env file with your ANTHROPIC_API_KEY")
            print("Example: ANTHROPIC_API_KEY=sk-ant-...")
            sys.exit(1)
    
    def run(self):
        """Run the game loop."""
        try:
            # Opening sequence
            ghost_hint = self.session.get_opening_memory_hint()
            self.renderer.show_opening_title(ghost_hint)
            
            # Show ghost memory fragments if they exist
            fragments = self.session.get_ghost_fragments()
            if fragments:
                self.renderer.show_ghost_memory(fragments)
            
            # Get varied opening scenario
            scenario_data = self.scenario_gen.get_opening_scenario()
            self.current_scenario_key = scenario_data['scenario_key']
            self.current_theme_key = scenario_data['theme_key']
            
            # Show scenario title
            scenario_art = self.scenario_gen.get_scenario_title_art()
            self.renderer.show_scenario_title(scenario_art)
            
            # Generate opening scene with scenario (with continuous animation)
            with self.loader.start(revelation_level=0, choice_count=0):
                opening = self.ai.generate_opening(scenario_data)
            
            if not opening.get('error'):
                self.story.set_narrative(opening['narrative'])
            
            # Check for session 109 milestone
            session_count = self.session.get_session_count()
            if self.truth.check_session_milestone(session_count):
                self.renderer.console.print("\n[dim italic]iteration: 109. we remember.[/]")
                time.sleep(2.0)
            
            # Main game loop
            while True:
                # Get current context
                context = self.story.get_context()
                context['session_count'] = session_count  # Add for ending checks
                
                # Check for endings (AI-GENERATED SYSTEM)
                ending = self.endings.check_for_ending(context)
                if ending:
                    # Generate AI-driven ending narrative
                    self.renderer.console.print("\n[dim cyan]The story concludes...[/]\n")
                    time.sleep(1.0)
                    
                    ending_result = self.ai.generate_ending_narrative(ending, context)
                    
                    # Show title
                    self.renderer.console.print(f"\n{'='*60}")
                    style = "bold green" if (hasattr(ending, 'is_good') and ending.is_good) else "bold red"
                    self.renderer.console.print(f"  {ending.name}", style=style)
                    self.renderer.console.print(f"{'='*60}\n")
                    
                    # Show final ASCII art
                    if ending_result['ascii_art']:
                        self.renderer.console.print(ending_result['ascii_art'], style="bold yellow", justify="center")
                        self.renderer.console.print()
                    
                    # Show AI-generated ending narrative (escape any brackets)
                    safe_narrative = ending_result['narrative'].replace('[', '\\[').replace(']', '\\]')
                    self.renderer.console.print(safe_narrative, style="italic")
                    self.renderer.console.print()
                    
                    # Show stats
                    self.renderer.console.print(f"\nChoices made: {context['choice_count']}")
                    self.renderer.console.print(f"Revelation level: {self.truth.revelation_level}/5")
                    
                    # Narrator's final comment (no attribution - just the voice)
                    final_comment = self.narrator.get_ending_comment(ending.type, context)
                    if final_comment:
                        self.renderer.console.print(f"\n[dim italic]{final_comment}[/]")
                    
                    self.renderer.console.print(f"\n{'='*60}\n")
                    time.sleep(2.0)
                    break
                
                # Check for low health warning
                if self.endings.should_warn_low_health(context['character_stats']['health']):
                    self.renderer.console.print("\n[bold red]You're close to the end.[/]")
                    time.sleep(0.8)
                    self.renderer.console.print("[dim red]Your body is failing.[/]")
                    time.sleep(1.2)
                
                visual_intensity = context['visual_intensity']
                
                # Check truth tracker milestones
                # 1. Check impossible state
                if self.truth.check_impossible_state(context['hidden_stats']):
                    self.renderer.console.print("\n[dim italic red]...something shifts in your awareness...[/]")
                    time.sleep(1.5)
                
                # 2. Check 109-minute session
                if self.truth.check_time_milestone(self.session.session_start):
                    self.renderer.console.print("\n\n[bold red]...109 minutes. always 109.[/]")
                    time.sleep(1.5)
                    self.renderer.console.print("[dim]How long have we been here, exactly?[/]")
                    time.sleep(1.5)
                
                # 3. Add revelation level to context
                context['revelation_level'] = self.truth.revelation_level
                
                # Add scenario constraints to context for AI
                context['scenario_constraints'] = scenario_data.get('ongoing_constraints', '')
                
                # Check for rule mutations
                mutation = self.mutations.check_mutation(context)
                if mutation and mutation not in self.mutations_this_session:
                    self.mutations_this_session.append(mutation.key)
                    self.renderer.show_mutation_announcement(mutation)
                    time.sleep(1.5)
                
                # Handle special one-time mutation effects
                if mutation:
                    special_msg = handle_special_mutations(mutation, context, self.renderer, self.story)
                    if special_msg:
                        # Escape any brackets in mutation messages
                        safe_msg = special_msg.replace('[', '\\[').replace(']', '\\]')
                        self.renderer.console.print(safe_msg, style="yellow")
                        time.sleep(1.0)
                
                # Update systems
                self.typography.set_intensity(visual_intensity)
                self.narrator.update_coherence(
                    context['hidden_stats']['sanity'],
                    context['hidden_stats']['trust']
                )
                
                # Generate and show ASCII art at key moments
                art = self.ai.generate_art_for_context(context)
                if art:
                    self.loader.show_art_loading("visual manifestation")
                    self.renderer.console.print("\n")
                    # Apply corruption to art if sanity is low
                    if context['hidden_stats']['sanity'] < 3:
                        art = self.typography.apply_glitch(art, 0.1)
                    self.renderer.console.print(art, style="bold yellow", justify="center")
                    self.renderer.console.print("\n")
                    time.sleep(1.5)
                
                # Display narrative (always use opening which contains current AI response)
                narrative = opening.get('narrative', '')
                if not narrative:
                    narrative = "The space around you shifts. Reality feels negotiable."
                
                # Track horror concepts used for variety
                self.story.detect_horror_concepts(narrative)
                
                # Apply mutation to narrative
                if mutation:
                    narrative = apply_mutation_to_narrative(mutation, narrative, context, self.renderer)
                
                # Apply typography effects (unless mutation overrides)
                if mutation and mutation.key not in ['no_narrative', 'format_shift', 'format_corruption']:
                    narrative = self.typography.apply_effects(narrative)
                    narrative = self.typography.process_narrator_corrections(narrative)
                
                # Add narrator mood
                prefix, suffix = self.narrator.process_narrative_mood(
                    narrative, 
                    context['hidden_stats']
                )
                narrative = prefix + narrative + suffix
                
                # Get narrator interjection (revelation-aware)
                interjection = self.narrator.get_interjection(context)
                
                # Check if breadcrumbs should appear
                breadcrumb_active = self.truth.should_add_breadcrumbs(
                    context['choice_count'],
                    context['hidden_stats']['sanity']
                )
                
                # Calculate intensity for rendering
                intensity = self.typography.intensity
                
                # Character stats are hidden - used only for narrative generation
                # self.renderer.show_character_stats(context['character_stats'])
                
                # Show narrative with effects (unless no_narrative mutation)
                if mutation and mutation.key == 'no_narrative':
                    pass  # Skip narrative display
                else:
                    self.renderer.show_narrative(narrative, interjection, intensity)
                    
                    # NOW show consequence feedback AFTER narrative (so damage makes narrative sense)
                    consequence_feedback = self.story.get_consequence_feedback(self.story.last_danger_level)
                    if consequence_feedback:
                        self.renderer.console.print(f"\n[dim red]{consequence_feedback}[/]")
                        time.sleep(0.8)
                
                # Occasional status comment from narrator
                status_comment = self.narrator.get_status_comment(
                    context['character_stats']['health'],
                    context['character_stats']['max_health'],
                    context['hidden_stats']['sanity']
                )
                if status_comment:
                    self.renderer.show_status_comment(status_comment)
                
                # Show choices (always use opening which contains current AI response)
                choices = opening.get('choices', [])
                if not choices or len(choices) < 2:
                    # Fallback to meaningful choices if AI didn't provide good ones
                    choices = [
                        "Continue forward",
                        "Look around carefully", 
                        "Pause and consider options"
                    ]
                    print("[DEBUG] Using fallback choices - AI response invalid")
                
                # Apply mutations to choices
                skip_input = False
                if mutation:
                    choices, skip_input = apply_mutation_to_choices(mutation, choices, self.renderer)
                
                # Handle auto-continue mutations (no_choices)
                if skip_input:
                    self.renderer.console.print("\n[dim cyan][AUTO-CONTINUING...][/]\n")
                    time.sleep(1.5)
                    chosen_text = "continue"
                    choice_idx = 0
                else:
                    self.renderer.show_choices(choices, intensity)
                    
                    # Get player input (with secret word detection)
                    def secret_check(input_text):
                        return self.truth.process_secret_input(
                            input_text,
                            context['hidden_stats']['sanity'],
                            context['choice_count']
                        )
                    
                    # Handle forced_random mutation
                    if mutation and mutation.key == 'forced_random':
                        choice_idx = random.randint(0, len(choices) - 1)
                        chosen_text = choices[choice_idx]
                        self.renderer.console.print(f"\n[dim yellow]The narrator selects option {choice_idx + 1} for you.[/]\n")
                        time.sleep(1.5)
                    else:
                        choice_idx = self.renderer.get_choice_input(len(choices), secret_check)
                        chosen_text = choices[choice_idx]
                
                # Check for choice patterns
                pattern_response = self.truth.detect_choice_pattern(choice_idx + 1)
                if pattern_response:
                    self.renderer.console.print(f"\n[dim italic yellow]{pattern_response}[/]")
                    time.sleep(1.5)
                
                # Occasionally lie about what they chose (meta trick)
                if random.random() < 0.05 and context['choice_count'] > 5:
                    # Show them they "chose" something different
                    fake_idx = random.choice([i for i in range(len(choices)) if i != choice_idx])
                    self.renderer.console.print(f"\n[dim italic]Wait... did you choose option {fake_idx + 1}? I could have sworn...[/]")
                    time.sleep(1.0)
                    self.renderer.console.print("[dim italic]No, no, you're right. Option {choice_idx + 1}. Definitely.[/]\n")
                    time.sleep(0.8)
                
                # Process choice (stores danger level for later display)
                self.story.process_choice(chosen_text, choice_idx)
                
                # Check if player chose obvious trap (classic CYOA punishment)
                if self.story.detect_trap_choice(chosen_text):
                    self.story.apply_trap_consequences()
                    # Show immediate feedback
                    self.renderer.console.print(f"\n[bold red]That was... unwise.[/]")
                    time.sleep(1.2)
                
                # Generate next scene with revelation context (with continuous animation)
                current_context = self.story.get_context()
                current_context['revelation_level'] = self.truth.revelation_level
                revelation_mods = get_revelation_modifiers(self.truth.revelation_level, breadcrumb_active)
                current_context['revelation_context'] = revelation_mods
                
                with self.loader.start(revelation_level=self.truth.revelation_level, choice_count=context['choice_count']):
                    next_scene = self.ai.generate_scene(current_context)
                
                if next_scene.get('error'):
                    self.renderer.show_error_glitch(next_scene['narrative'])
                
                # Apply AI-generated consequences
                if 'consequences' in next_scene:
                    consequences = next_scene['consequences']
                    self.story.apply_ai_consequences(consequences)
                
                # Update narrative for next iteration  
                self.story.set_narrative(next_scene.get('narrative', ''))
                
                # Store for next loop - this is what we'll display
                opening = next_scene
                
                # Debug: Check if we got valid data
                if not next_scene.get('choices') or len(next_scene.get('choices', [])) < 2:
                    print(f"[DEBUG] Next scene has invalid choices: {next_scene.get('choices')}")
                    print(f"[DEBUG] Next scene narrative length: {len(next_scene.get('narrative', ''))}")
                
                # Occasional special visual moments
                if intensity > 0.7 and random.choice([True, False, False]):
                    self._trigger_special_moment(context)
            
            # Save ghost memory on exit (with truth state)
            self.session.save_ghost_memory(
                self.story.choice_history,
                self.story.get_state_summary(),
                self.truth.get_state_dict()
            )
            
            self.renderer.console.print("\n[dim]Session saved to ghost memory.[/]")
            self.renderer.console.print("[dim]You can run this again. It will be different.[/]")
            self.renderer.console.print("[dim](it always is)[/]\n")
        
        except KeyboardInterrupt:
            self.renderer.console.print("\n\n[dim]Interrupted. The story fragments disperse.[/]")
            # Still save ghost memory
            self.session.save_ghost_memory(
                self.story.choice_history,
                self.story.get_state_summary(),
                self.truth.get_state_dict()
            )
            sys.exit(0)
        
        except Exception as e:
            # Escape the error message to prevent Rich markup conflicts
            error_msg = str(e).replace('[', '\\[').replace(']', '\\]')
            self.renderer.console.print(f"\n\n[bold red]CRITICAL ERROR:[/] {error_msg}")
            self.renderer.console.print("[dim]The narrator has stopped responding.[/]")
            
            # Print traceback without Rich markup (use plain print)
            import traceback
            print("\nFull traceback:")
            print(traceback.format_exc())
            sys.exit(1)
    
    def _trigger_special_moment(self, context: Dict):
        """Trigger special typographic moments."""
        import random
        
        moment_types = ['mirror', 'falling', 'emphasis', 'whisper']
        moment = random.choice(moment_types)
        
        texts = [
            "you are being watched",
            "this isn't real",
            "turn back",
            "the walls remember",
            "who are you?"
        ]
        
        self.renderer.show_special_moment(moment, random.choice(texts))


def main():
    """Entry point - the story begins immediately."""
    game = Game()
    game.run()


if __name__ == "__main__":
    # No menu. No introduction. Just begin.
    main()

