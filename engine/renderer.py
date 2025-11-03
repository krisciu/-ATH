"""Rich-based rendering system with typing effects and visual layouts."""

import time
import random
from typing import List, Optional
from rich.console import Console
from rich.panel import Panel
from rich.layout import Layout
from rich.text import Text
from rich.table import Table
from rich import box
from rich.align import Align
from rich.columns import Columns


class Renderer:
    """Handles all visual output using Rich library."""
    
    # Dynamic color palettes for different moods
    COLOR_PALETTES = {
        'stable': ['white', 'bright_white', 'grey70'],
        'unsettled': ['cyan', 'bright_cyan', 'blue', 'white'],
        'disturbed': ['yellow', 'bright_yellow', 'orange1', 'gold1'],
        'breaking': ['red', 'bright_red', 'orange_red1', 'dark_orange'],
        'collapsed': ['magenta', 'bright_magenta', 'purple', 'violet', 'red'],
        'horror': ['red', 'dark_red', 'red3', 'indian_red'],
        'glitch': ['green', 'bright_green', 'cyan', 'magenta', 'yellow'],
        'void': ['grey30', 'grey23', 'grey15', 'black'],
    }
    
    def __init__(self):
        """Initialize the renderer."""
        self.console = Console()
        self.typing_speed = 0.02  # Base typing speed
        self.current_palette = 'stable'
        self.interrupt_count = 0  # Track Ctrl+C attempts across entire session
    
    @staticmethod
    def escape_markup(text: str) -> str:
        """Escape Rich markup characters to prevent parsing errors."""
        return text.replace('[', '\\[').replace(']', '\\]')
    
    def get_dynamic_color(self, intensity: float = 0.0) -> str:
        """Get a color based on current intensity."""
        if intensity >= 0.8:
            palette = self.COLOR_PALETTES['collapsed']
        elif intensity >= 0.6:
            palette = self.COLOR_PALETTES['breaking']
        elif intensity >= 0.4:
            palette = self.COLOR_PALETTES['disturbed']
        elif intensity >= 0.2:
            palette = self.COLOR_PALETTES['unsettled']
        else:
            palette = self.COLOR_PALETTES['stable']
        
        return random.choice(palette)
    
    def get_random_color_from_palette(self, palette_name: str) -> str:
        """Get random color from a specific palette."""
        return random.choice(self.COLOR_PALETTES.get(palette_name, ['white']))
    
    def clear(self):
        """Clear the screen."""
        self.console.clear()
    
    def show_loading(self, message: str = "[LOADING...]", duration: float = 1.0):
        """Show a loading message."""
        # Occasionally mess with the player
        if random.random() < 0.1:  # 10% chance
            tricks = [
                self._loading_trick_fake_error,
                self._loading_trick_watching,
                self._loading_trick_slow,
            ]
            random.choice(tricks)(message, duration)
        else:
            with self.console.status(message, spinner="dots"):
                time.sleep(duration)
    
    def _loading_trick_fake_error(self, message: str, duration: float):
        """Fake an error during loading."""
        with self.console.status(message, spinner="dots"):
            time.sleep(duration * 0.3)
        self.console.print("[red]ERROR: Connection lost[/]")
        time.sleep(0.8)
        self.console.print("[dim]...just kidding[/]")
        time.sleep(0.5)
    
    def _loading_trick_watching(self, message: str, duration: float):
        """Make it seem like the program is watching."""
        with self.console.status(message, spinner="dots"):
            time.sleep(duration * 0.5)
        self.console.print("[dim]...are you still there?[/]")
        time.sleep(0.8)
        with self.console.status("[RESUMING...]", spinner="dots"):
            time.sleep(duration * 0.5)
    
    def _loading_trick_slow(self, message: str, duration: float):
        """Pretend to load very slowly then speed up."""
        self.console.print(f"{message}", style="dim")
        time.sleep(duration * 1.5)
        self.console.print("[dim]oh sorry, that was slow[/]")
        time.sleep(0.3)
    
    def type_text(self, text: str, speed: Optional[float] = None, style: str = ""):
        """Type out text character by character with proper animation."""
        from rich.live import Live
        from rich.text import Text
        
        speed = speed or self.typing_speed
        
        # Escape any Rich markup in the text for safety
        safe_text = text.replace('[', '\\[').replace(']', '\\]')
        
        # Build text progressively with Live display
        displayed_text = Text()
        
        with Live(displayed_text, console=self.console, refresh_per_second=30) as live:
            for char in safe_text:
                displayed_text.append(char, style=style)
                live.update(displayed_text)
                
                # Add delay for non-whitespace characters
                if char not in [' ', '\n', '\t']:
                    time.sleep(speed * random.uniform(0.5, 1.5))
                elif char == ' ':
                    time.sleep(speed * 0.3)
        
        self.console.print()  # Newline after animation completes
    
    def show_narrative(self, narrative: str, interjection: Optional[str] = None, intensity: float = 0.0):
        """Display narrative text with optional narrator interjection - DYNAMIC COLORS."""
        # Adjust typing speed based on intensity
        speed = self.typing_speed * (1 + intensity * 0.5)
        
        # Get dynamic color based on intensity
        color = self.get_dynamic_color(intensity)
        style = f"bold {color}" if intensity > 0.6 else color
        
        # Type the narrative
        self.console.print()
        self.type_text(narrative, speed=speed, style=style)
        
        # Add interjection if present with varied colors
        if interjection:
            time.sleep(0.3)
            interjection_color = self.get_random_color_from_palette('glitch' if intensity > 0.7 else 'unsettled')
            self.console.print(f"\n  {interjection}", style=f"dim italic {interjection_color}")
        
        self.console.print()
    
    def show_choices(self, choices: List[str], intensity: float = 0.0):
        """Display choice options - DYNAMIC COLORS."""
        self.console.print()
        
        # Get dynamic colors for choices
        for i, choice in enumerate(choices, 1):
            # Each choice gets a slightly different color
            choice_color = self.get_dynamic_color(intensity)
            number_color = self.get_random_color_from_palette('horror' if intensity > 0.7 else 'disturbed' if intensity > 0.4 else 'stable')
            
            # Add visual corruption to choices at high intensity
            if intensity > 0.7 and random.random() < 0.3:
                choice = self._corrupt_text(choice)
            
            self.console.print(f"  [bold {number_color}]{i}[/]. [{choice_color}]{choice}[/]")
        
        self.console.print()
    
    def get_choice_input(self, num_choices: int, secret_check_callback=None) -> int:
        """Get player's choice input (with optional secret word detection)."""
        # Very rarely, pretend someone else is typing
        if random.random() < 0.03:  # 3% chance
            self.console.print("[bold green]>[/] ", end="")
            time.sleep(0.5)
            fake_choice = random.randint(1, num_choices)
            for char in str(fake_choice):
                self.console.print(char, end="")
                time.sleep(0.2)
            self.console.print()
            time.sleep(0.8)
            self.console.print("[dim]...wait, that wasn't you, was it?[/]")
            time.sleep(1.0)
            self.console.print("[dim]Let's try that again.[/]\n")
            time.sleep(0.5)
        
        while True:
            try:
                choice = self.console.input("[bold green]>[/] ")
                
                # Check for debug toggle command
                if choice.lower().strip() == 'debug':
                    from engine.debug import DebugManager
                    DebugManager.toggle()
                    continue  # Ask for input again
                
                # Check for secret words if callback provided
                if secret_check_callback:
                    secret_response = secret_check_callback(choice)
                    if secret_response:
                        self.console.print(f"\n[dim italic yellow]{secret_response}[/]")
                        time.sleep(2.0)
                        self.console.print("[dim]Let's continue. We have eternity.[/]\n")
                        time.sleep(1.0)
                        continue  # Ask for input again
                
                choice_num = int(choice)
                if 1 <= choice_num <= num_choices:
                    return choice_num - 1  # Return 0-indexed
                else:
                    self.console.print(f"[red]Please enter a number between 1 and {num_choices}[/]")
            except ValueError:
                self.console.print("[red]Please enter a valid number[/]")
            except KeyboardInterrupt:
                self.interrupt_count += 1
                if self.interrupt_count == 1:
                    self.console.print("\n[dim]Cannot escape that easily...[/]")
                    time.sleep(0.5)
                elif self.interrupt_count == 2:
                    # Fake exit - make it look like the program closed
                    self.console.clear()
                    time.sleep(0.8)
                    self.console.print("\n\n\n\n\n")
                    self.console.print("                    :)", style="bold white")
                    time.sleep(1.2)
                    self.console.print("\n[dim]Did you really think it would be that easy?[/]")
                    time.sleep(1.0)
                    self.console.print("[dim]Try again if you really want to leave...[/]\n")
                    time.sleep(0.5)
                else:
                    self.console.print("\n[dim]Fine. The story releases you.[/]")
                    time.sleep(0.5)
                    raise  # Let it propagate to main handler
            except EOFError:
                return 0  # Default to first choice if EOF
    
    def get_free_text_input(self, prompt: str = "What do you say?") -> str:
        """Get free-form text input from player."""
        self.console.print(f"\n[bold yellow]{prompt}[/]")
        self.console.print("[dim](Type your response, press Enter when done)[/]\n")
        
        try:
            response = self.console.input("[bold green]>[/] ")
            return response.strip()
        except (KeyboardInterrupt, EOFError):
            return "[silence]"
    
    def get_timed_choice_input(self, choices: List[str], timeout: int = 10) -> int:
        """Get choice input with countdown timer."""
        import threading
        from rich.live import Live
        from rich.text import Text
        
        result = {'choice': None, 'timed_out': False}
        
        def countdown_display():
            """Display countdown."""
            for remaining in range(timeout, 0, -1):
                if result['choice'] is not None:
                    break
                time.sleep(1)
            result['timed_out'] = True
        
        # Start countdown in background
        timer_thread = threading.Thread(target=countdown_display, daemon=True)
        timer_thread.start()
        
        # Show choices with timer
        self.console.print()
        for i, choice in enumerate(choices, 1):
            self.console.print(f"  [bold yellow]{i}[/]. {choice}")
        
        self.console.print(f"\n[bold red]⏰ You have {timeout} seconds[/]\n")
        
        start_time = time.time()
        while time.time() - start_time < timeout:
            try:
                choice = self.console.input(f"[bold green]>[/] ")
                choice_num = int(choice)
                if 1 <= choice_num <= len(choices):
                    result['choice'] = choice_num - 1
                    return result['choice']
            except (ValueError, KeyboardInterrupt):
                pass
            
            if result['timed_out']:
                break
        
        # Timeout - return random choice
        self.console.print("\n[bold red]⏰ TIME'S UP[/]")
        time.sleep(0.5)
        default = random.randint(0, len(choices) - 1)
        self.console.print(f"[dim]The narrator chooses for you: {choices[default]}[/]")
        time.sleep(1)
        return default
    
    def get_coordinate_input(self, art: str, prompt: str = "Enter coordinates") -> tuple[int, int]:
        """Get coordinate input for ASCII art interaction."""
        self.console.print(f"\n{art}\n", style="cyan")
        self.console.print(f"[bold yellow]{prompt} (format: x,y)[/]")
        self.console.print("[dim](e.g., 5,3 for column 5, row 3)[/]\n")
        
        while True:
            try:
                coord_input = self.console.input("[bold green]>[/] ")
                parts = coord_input.strip().split(',')
                if len(parts) == 2:
                    x, y = int(parts[0]), int(parts[1])
                    if 0 <= x <= 20 and 0 <= y <= 20:
                        return (x, y)
                    self.console.print("[red]Coordinates must be 0-20[/]")
                else:
                    self.console.print("[red]Format: x,y (e.g., 5,3)[/]")
            except ValueError:
                self.console.print("[red]Invalid coordinates[/]")
            except (KeyboardInterrupt, EOFError):
                return (0, 0)  # Default
    
    def get_word_puzzle_input(self, puzzle_display: str, hint: str = "") -> str:
        """Get input for word puzzle."""
        self.console.print(f"\n[bold yellow]PUZZLE:[/]")
        self.console.print(f"{puzzle_display}\n")
        if hint:
            self.console.print(f"[dim]Hint: {hint}[/]\n")
        
        try:
            answer = self.console.input("[bold green]Answer>[/] ")
            return answer.strip()
        except (KeyboardInterrupt, EOFError):
            return ""
    
    def get_fill_blank_input(self, narrative_with_blanks: str) -> List[str]:
        """Get fill-in-the-blank input."""
        self.console.print(f"\n{narrative_with_blanks}\n")
        self.console.print("[bold yellow]Fill in the blanks:[/]\n")
        
        # Count blanks
        blank_count = narrative_with_blanks.count('_____')
        
        answers = []
        for i in range(blank_count):
            try:
                answer = self.console.input(f"[bold green]Blank {i+1}>[/] ")
                answers.append(answer.strip())
            except (KeyboardInterrupt, EOFError):
                answers.append("[...]")
        
        return answers
    
    def get_text_parser_input(self) -> str:
        """Get old-school text parser command."""
        self.console.print("\n[dim]Enter command (e.g., LOOK AROUND, TAKE ITEM, GO NORTH)[/]")
        
        try:
            command = self.console.input("[bold green]>[/] ")
            return command.strip()
        except (KeyboardInterrupt, EOFError):
            return "WAIT"
    
    def show_character_stats(self, stats: dict, visible: bool = False):
        """Display character stats panel (hidden by default for ~ATH)."""
        # Stats are now hidden - used only for narrative generation
        # Players experience the story without seeing numbers
        if not visible:
            return
        
        health_percent = stats['health'] / stats['max_health']
        health_color = "green" if health_percent > 0.6 else "yellow" if health_percent > 0.3 else "red"
        
        stats_text = f"""[{health_color}]HP:[/] {stats['health']}/{stats['max_health']}
[cyan]STR:[/] {stats['strength']}  [cyan]SPD:[/] {stats['speed']}  [cyan]INT:[/] {stats['intelligence']}"""
        
        panel = Panel(
            stats_text,
            title="[bold]Status[/]",
            border_style="dim white",
            box=box.ROUNDED,
            padding=(0, 1)
        )
        
        self.console.print(panel)
    
    def show_ascii_art(self, art: str, intensity: float = 0.0):
        """Display ASCII art with potential corruption - DYNAMIC COLORS."""
        lines = art.split('\n')
        corrupted_lines = []
        
        for line in lines:
            # Corrupt some lines at high intensity
            if intensity > 0.6 and random.random() < intensity * 0.3:
                line = self._corrupt_text(line)
            corrupted_lines.append(line)
        
        # Use dynamic colors for ASCII art
        art_color = self.get_dynamic_color(intensity)
        
        # Occasionally use horror or glitch palette for extra creepiness
        if random.random() < 0.3:
            art_color = self.get_random_color_from_palette('horror' if intensity > 0.5 else 'glitch')
        
        self.console.print(Align.center('\n'.join(corrupted_lines)), style=f"bold {art_color}")
        self.console.print()
    
    def show_scattered_text(self, lines: List[str]):
        """Display scattered text effect."""
        for line in lines:
            self.console.print(line, style="dim white")
            time.sleep(0.1)
    
    def show_spiral_text(self, lines: List[str]):
        """Display spiraling text effect."""
        for line in lines:
            self.console.print(line, style="yellow")
            time.sleep(0.15)
    
    def show_vertical_text(self, lines: List[str]):
        """Display vertical text effect."""
        for line in lines:
            self.console.print(line, style="white")
            time.sleep(0.08)
    
    def show_ghost_memory(self, fragments: List[str]):
        """Display ghost memory fragments."""
        if not fragments:
            return
        
        self.console.print()
        self.console.print("[dim italic]...memory fragments detected...[/]", style="cyan")
        time.sleep(0.5)
        
        for fragment in fragments[:3]:  # Show max 3 fragments
            self.console.print(f"  [dim cyan]{fragment}[/]")
            time.sleep(0.3)
        
        self.console.print()
    
    def show_opening_title(self, ghost_hint: Optional[str] = None):
        """Display opening sequence."""
        self.clear()
        
        # ~ATH title
        title = """
    ╔═══════════════════════════════════════╗
    ║                                       ║
    ║              ~ A T H                  ║
    ║                                       ║
    ║     a story that shouldn't exist     ║
    ║                                       ║
    ╚═══════════════════════════════════════╝
        """
        
        self.console.print(title, style="bold cyan")
        time.sleep(1)
        
        if ghost_hint:
            self.console.print(f"\n  [dim italic]{ghost_hint}[/]")
            time.sleep(1.5)
        
        self.console.print("\n[dim]The cursor blinks. Something begins.[/]")
        time.sleep(1.5)
        self.show_loading("[INITIALIZING...]", 1.5)
    
    def show_game_over(self, message: str, narrator_comment: str, choice_count: int):
        """Display game over screen."""
        self.console.print("\n\n")
        
        game_over_text = f"""
╔════════════════════════════════════════════╗
║                                            ║
║              T E R M I N A T E D           ║
║                                            ║
╚════════════════════════════════════════════╝

{message}

{narrator_comment}

Choices made: {choice_count}
Session ended.

(the story is already forgetting you)
        """
        
        self.console.print(game_over_text, style="dim red")
        time.sleep(2)
    
    def show_error_glitch(self, error_message: str):
        """Show an error as a narrative glitch."""
        glitch_panel = Panel(
            f"[bold red]S̴Y̷S̶T̸E̷M̴ ̸E̷R̶R̸O̷R̴[/]\n\n{error_message}\n\n[dim](continuing anyway...)[/]",
            border_style="red",
            box=box.DOUBLE
        )
        self.console.print(glitch_panel)
        time.sleep(1)
    
    def show_status_comment(self, comment: str):
        """Show narrator comment on player status."""
        self.console.print(f"\n  [dim italic yellow]{comment}[/]")
        time.sleep(0.5)
    
    def _corrupt_text(self, text: str) -> str:
        """Apply simple corruption to text."""
        chars = list(text)
        for i in range(len(chars)):
            if random.random() < 0.1 and chars[i].isalpha():
                chars[i] = random.choice(['█', '▓', '▒', '░', chars[i]])
        return ''.join(chars)
    
    def show_special_moment(self, moment_type: str, text: str):
        """Display special typographic moments."""
        if moment_type == "mirror":
            # Show text and its mirror
            self.console.print(f"\n{text}", style="white")
            reversed_text = text[::-1]
            self.console.print(f"{reversed_text}\n", style="dim white")
        
        elif moment_type == "falling":
            # Vertical text
            self.console.print()
            for char in text[:20]:  # Limit length
                self.console.print(f"     {char}")
                time.sleep(0.05)
        
        elif moment_type == "emphasis":
            # Big emphasis
            emphasized = text.upper()
            spaced = ' '.join(emphasized)
            self.console.print(f"\n\n  {spaced}\n\n", style="bold white")
        
        elif moment_type == "whisper":
            # Very small/dim
            self.console.print(f"\n  {text.lower()}\n", style="dim italic")
    
    def show_scenario_title(self, scenario_art: str):
        """Display scenario announcement with ASCII art."""
        self.console.print(scenario_art, style="bold cyan", justify="center")
        time.sleep(1.5)
    
    def show_mutation_announcement(self, mutation):
        """Display mutation announcement."""
        # Visual glitch effect
        glitch_chars = ['█', '▓', '▒', '░']
        glitch_line = ''.join(random.choice(glitch_chars) for _ in range(40))
        
        self.console.print(f"\n{glitch_line}", style="red")
        time.sleep(0.3)
        self.console.print(f"[bold red]{mutation.announcement}[/]", justify="center")
        time.sleep(0.5)
        self.console.print(f"[dim yellow]{mutation.description}[/]", justify="center")
        time.sleep(0.3)
        self.console.print(f"{glitch_line}\n", style="red")
    
    def show_narrator_split(self, narrative1: str, narrative2: str):
        """Show two narrators arguing in columns."""
        table = Table(show_header=True, header_style="bold", box=box.SIMPLE)
        table.add_column("Narrator A", style="cyan", width=35)
        table.add_column("Narrator B", style="magenta", width=35)
        
        # Split narratives into chunks
        words1 = narrative1.split()
        words2 = narrative2.split()
        
        chunk1 = ' '.join(words1[:30]) if len(words1) > 30 else narrative1
        chunk2 = ' '.join(words2[:30]) if len(words2) > 30 else narrative2
        
        table.add_row(chunk1, chunk2)
        
        self.console.print("\n[bold red][TWO VOICES DETECTED][/]\n")
        self.console.print(table)
        self.console.print("[dim](both claim to be the narrator)[/]\n")
    
    def show_format_corruption(self, text: str, corruption_type: str):
        """Display text in corrupted formats."""
        if corruption_type == "poetry":
            lines = text.split('. ')
            self.console.print("\n[dim cyan][POETRY MODE][/]")
            for line in lines:
                self.console.print(f"  {line}")
                time.sleep(0.2)
            self.console.print()
        
        elif corruption_type == "code":
            self.console.print("\n[dim green][CODE MODE][/]")
            self.console.print(f"// NARRATIVE_BUFFER\nstd::string story = \"{text[:60]}...\";\n// CONTINUE")
        
        elif corruption_type == "error":
            self.console.print("\n[bold red][ERROR LOG][/]")
            self.console.print(f"ERROR 0x7F9A: {text[:50]}...\n[STACK TRACE CORRUPTED]")
        
        elif corruption_type == "ascii":
            # Heavy ASCII glitching
            glitched = ''.join(random.choice(['█', '▓', '▒', '░', c]) if random.random() < 0.4 else c for c in text)
            self.console.print(f"\n{glitched}\n", style="yellow")

