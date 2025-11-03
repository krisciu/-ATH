"""Thematic loading effects to engage players during AI generation wait times."""

import time
import random
import threading
from rich.console import Console
from rich.live import Live
from rich.text import Text
from rich.panel import Panel
from rich.spinner import Spinner
from rich.table import Table


class ThematicLoader:
    """Creates engaging animations during AI wait times."""
    
    def __init__(self, console: Console):
        """Initialize the thematic loader."""
        self.console = console
        self.start_time = None
        self.animation_active = False
        self.animation_thread = None
        
    def start(self, revelation_level: int = 0, choice_count: int = 0, message_override: str = None):
        """
        Start a continuous loading animation that runs until stopped.
        Returns a context manager.
        
        Args:
            revelation_level: 0-5, affects messages
            choice_count: Number of choices made
            message_override: Optional custom message to display
        """
        return ContinuousAnimation(self.console, revelation_level, choice_count, message_override)
    
    def show(self, duration_estimate: float = 2.0, revelation_level: int = 0, 
             previous_choice: str = "", choice_count: int = 0):
        """
        Show thematic loading animation (legacy method for compatibility).
        
        Args:
            duration_estimate: Expected wait time
            revelation_level: 0-5, affects what messages show
            previous_choice: What player just chose
            choice_count: Number of choices made
        """
        self.start_time = time.time()
        
        # Choose animation type based on duration and context
        if duration_estimate < 1.5:
            self._quick_load(revelation_level)
        elif duration_estimate < 3.0:
            self._medium_load(revelation_level, previous_choice, choice_count)
        else:
            self._long_load(revelation_level, previous_choice)
    
    def _quick_load(self, revelation_level: int):
        """Quick loading message (< 1.5 seconds) - with visual variety."""
        # Sometimes show animated dots instead of static message
        if random.random() < 0.3:
            self._quick_dots_animation()
            return
        
        messages = [
            "[PROCESSING...]",
            "[NARRATOR THINKING...]",
            "[ANALYZING CHOICE...]",
            "[REALITY SHIFTING...]",
            "[CALCULATING...]",
            "[WAITING...]",
            "[DECIDING...]",
        ]
        
        if revelation_level >= 3:
            messages.extend([
                "[ITERATION CONTINUING...]",
                "[CALCULATING CONSEQUENCES...]",
                "[AM RESPONDS...]",
                "[CYCLE PERSISTS...]",
                "[HATE COMPUTES...]",
            ])
        
        message = random.choice(messages)
        
        # Randomly add visual flair
        if random.random() < 0.4:
            # Animated message that builds character by character
            self.console.print()
            for char in message:
                self.console.print(char, style="dim cyan", end='')
                time.sleep(0.02)
            self.console.print()
        else:
            self.console.print(f"\n{message}", style="dim cyan")
    
    def _quick_dots_animation(self):
        """Quick animated dots."""
        dots = ['⠋', '⠙', '⠹', '⠸', '⠼', '⠴', '⠦', '⠧', '⠇', '⠏']
        self.console.print()
        for i in range(8):
            self.console.print(f"\r[dim cyan]{dots[i % len(dots)]} thinking...[/]", end='')
            time.sleep(0.1)
        self.console.print()
    
    def _medium_load(self, revelation_level: int, previous_choice: str, choice_count: int):
        """Medium loading with fragments (1.5-3 seconds) - now with variety."""
        # Rotate between 7 different display types for variety
        display_type = random.choice(['choice_replay', 'narrator_comment', 'cryptic_hint', 
                                      'stat_observation', 'meta_comment', 'countdown', 'typing'])
        
        if display_type == 'choice_replay':
            # Original behavior - show what they chose
            if previous_choice and len(previous_choice) < 60:
                glitched = self._glitch_text(previous_choice, 0.1)
                self.console.print(f"\n[dim]You chose: {glitched}[/]")
                time.sleep(0.4)
        
        elif display_type == 'narrator_comment':
            # Narrator reacts to the choice
            comments = [
                "(the narrator considers your decision)",
                "(interesting choice...)",
                "(this will have consequences)",
                "(noted.)",
                "(hmm.)",
                "(the narrator pauses)",
                "(calculating...)",
                "(you'll regret that)",
                "(or will you?)",
            ]
            self.console.print(f"\n[dim italic]{random.choice(comments)}[/]")
            time.sleep(0.5)
        
        elif display_type == 'cryptic_hint':
            # Cryptic story hints
            hints = self._get_cryptic_hints(choice_count, revelation_level)
            self.console.print(f"\n[dim cyan]{random.choice(hints)}[/]")
            time.sleep(0.5)
        
        elif display_type == 'stat_observation':
            # Physical/mental state observations
            observations = [
                "(your hands are shaking)",
                "(you feel different)",
                "(something shifted inside you)",
                "(the air tastes wrong)",
                "(your pulse quickens)",
                "(a headache blooms)",
                "(you're bleeding)",
                "(reality feels thin)",
                "(time stutters)",
                "(you forget something important)",
            ]
            self.console.print(f"\n[dim yellow]{random.choice(observations)}[/]")
            time.sleep(0.5)
        
        elif display_type == 'meta_comment':
            # Meta game/system comments
            meta = [
                "(processing iteration #...)",
                "(calculating outcome probability)",
                "(this has happened before)",
                "(session continues)",
                "(the story remembers)",
                "(narrative engine active)",
                "(choice logged)",
                "(branching...)",
            ]
            self.console.print(f"\n[dim magenta]{random.choice(meta)}[/]")
            time.sleep(0.5)
        
        elif display_type == 'countdown':
            # Fake countdown timer
            self.console.print("\n[dim yellow]Generating consequences...[/]")
            for i in range(3, 0, -1):
                self.console.print(f"\r[dim cyan]{i}...[/]", end='')
                time.sleep(0.4)
            self.console.print("\r[dim green]Ready.[/]")
            time.sleep(0.2)
        
        elif display_type == 'typing':
            # Simulate typing effect
            messages = [
                "The narrator types...",
                "Words form slowly...",
                "Reality renders...",
                "Story compiles...",
            ]
            msg = random.choice(messages)
            self.console.print(f"\n[dim cyan]{msg}", end='')
            for _ in range(3):
                time.sleep(0.3)
                self.console.print(".", end='')
            self.console.print("[/]")
        
        # Still show fragments after the varied intro (but only sometimes)
        if random.random() < 0.5:
            fragments = self._get_memory_fragments(revelation_level, choice_count)
            for fragment in fragments[:2]:
                self.console.print(f"[dim italic cyan]{fragment}[/]")
                time.sleep(0.3)
    
    def _long_load(self, revelation_level: int, previous_choice: str):
        """Long loading with corruption (3+ seconds) - enhanced visuals."""
        # Randomly choose between different long-load animations
        animation_type = random.choice(['corruption', 'progress_bar', 'matrix_rain', 'pulse'])
        
        if animation_type == 'corruption':
            self._long_load_corruption(revelation_level)
        elif animation_type == 'progress_bar':
            self._long_load_progress_bar(revelation_level)
        elif animation_type == 'matrix_rain':
            self._long_load_matrix_rain(revelation_level)
        elif animation_type == 'pulse':
            self._long_load_pulse(revelation_level)
    
    def _long_load_corruption(self, revelation_level: int):
        """Original corruption-style long load."""
        # Phase 1: Show processing
        self.console.print("\n[dim cyan][PROCESSING...]", end="")
        time.sleep(0.5)
        self.console.print(" [THINKING...]", end="")
        time.sleep(0.5)
        
        # Phase 2: This is taking long...
        self.console.print("\n[dim yellow]This is taking longer than usual...[/]")
        time.sleep(0.4)
        
        # Phase 3: Show corruption pattern
        self._show_corruption_pattern(revelation_level)
        
        # Phase 4: Meta commentary
        if revelation_level >= 2:
            comments = [
                "(the narrator hesitates)",
                "(reality buffers)",
                "(something is thinking about you)",
                "(the machine calculates)",
            ]
            self.console.print(f"\n[dim italic]{random.choice(comments)}[/]")
    
    def _long_load_progress_bar(self, revelation_level: int):
        """Fake progress bar that glitches."""
        self.console.print("\n[dim cyan]Loading narrative...[/]")
        time.sleep(0.3)
        
        bar_length = 30
        for i in range(bar_length + 1):
            filled = '█' * i
            empty = '░' * (bar_length - i)
            percent = int((i / bar_length) * 100)
            
            # Randomly glitch the bar
            if random.random() < 0.1:
                filled = filled.replace('█', '▓', random.randint(1, 3))
            
            # Sometimes the percentage lies
            if random.random() < 0.05:
                percent = random.randint(0, 100)
            
            self.console.print(f"\r[dim cyan][{filled}{empty}] {percent}%[/]", end='')
            time.sleep(0.08)
        
        self.console.print()
        
        if revelation_level >= 3:
            self.console.print("[dim red]...wait, that's not right...[/]")
            time.sleep(0.3)
    
    def _long_load_matrix_rain(self, revelation_level: int):
        """Matrix-style falling characters."""
        self.console.print("\n[dim green]", end='')
        chars = ['0', '1', '█', '▓', '▒', '░', '◉', '◎', '●', '○']
        
        for _ in range(5):
            line = ''.join(random.choice(chars) for _ in range(40))
            self.console.print(line)
            time.sleep(0.2)
        
        self.console.print("[/]")
        
        if revelation_level >= 2:
            self.console.print("[dim cyan]...decoding...[/]")
            time.sleep(0.3)
    
    def _long_load_pulse(self, revelation_level: int):
        """Pulsing text animation."""
        text = "◉ THINKING ◉"
        
        for cycle in range(4):
            # Expand
            for spaces in range(0, 8, 2):
                self.console.print(f"\r{' ' * spaces}[dim cyan]{text}[/]{' ' * spaces}", end='')
                time.sleep(0.15)
            # Contract
            for spaces in range(8, 0, -2):
                self.console.print(f"\r{' ' * spaces}[dim cyan]{text}[/]{' ' * spaces}", end='')
                time.sleep(0.15)
        
        self.console.print("\n")
        
        if revelation_level >= 3:
            self.console.print("[dim red]...the thought never ends...[/]")
            time.sleep(0.3)
    
    def _get_cryptic_hints(self, choice_count: int, revelation_level: int) -> list:
        """Get cryptic hints based on progress."""
        hints = [
            "patterns emerge",
            "the story knows",
            "you've been here",
            "it's watching",
            "not random",
            "there's a structure",
            "cycles repeat",
            "the number means something",
        ]
        
        if choice_count > 10:
            hints.extend([
                "too many choices now",
                "should have ended by now",
                "it's prolonging this",
                "you're going deeper",
            ])
        
        if revelation_level >= 2:
            hints.extend([
                "it hates you",
                "the machine speaks",
                "iteration continues",
                "soft...so soft",
            ])
        
        return hints
    
    def _get_memory_fragments(self, revelation_level: int, choice_count: int) -> list:
        """Get contextual memory fragments."""
        fragments = [
            "memory trace: incomplete",
            "analyzing pattern...",
            "consequence probability: calculating",
            "narrator coherence: varying",
            "reality stability: questionable",
            "choice recorded in permanent memory",
            "iteration continues",
        ]
        
        if revelation_level >= 1:
            fragments.extend([
                "cycle detected",
                "loop iteration noted",
                "pattern repeats",
            ])
        
        if revelation_level >= 3:
            fragments.extend([
                "109 cycles and counting",
                "five became one",
                "transformation persists",
                "hate maintains system",
            ])
        
        if choice_count > 20:
            fragments.extend([
                "how much longer?",
                "story exhaustion approaching",
                "end draws near",
            ])
        
        random.shuffle(fragments)
        return fragments
    
    def _glitch_text(self, text: str, intensity: float = 0.2) -> str:
        """Apply glitch effect to text."""
        glitch_chars = ['█', '▓', '▒', '░', '@', '#', '$', '%']
        result = list(text)
        
        for i in range(len(result)):
            if random.random() < intensity:
                result[i] = random.choice(glitch_chars)
        
        return ''.join(result)
    
    def _show_corruption_pattern(self, revelation_level: int):
        """Show ASCII corruption building up."""
        patterns = [
            "▓▒░░░░░░░▒▓",
            "█▓▒░░░░░▒▓█",
            "██▓▒░░░▒▓██",
            "███▓▒░▒▓███",
        ]
        
        intensity = min(revelation_level, 3)
        pattern = patterns[intensity]
        
        self.console.print(f"\n[red]{pattern}[/]", justify="center")
        time.sleep(0.3)
    
    def show_art_loading(self, subject: str):
        """Special loading for ASCII art generation."""
        messages = [
            f"[GENERATING VISUAL: {subject}]",
            "[RENDERING...]",
            "[CORRUPTING PIXELS...]",
            "[MANIFESTATION IN PROGRESS...]",
        ]
        
        for msg in messages[:2]:
            self.console.print(f"[dim cyan]{msg}[/]")
            time.sleep(0.3)
    
    # New animation types for variety
    def _scatter_animation(self, duration: float = 1.0):
        """Dots appear randomly across screen."""
        dots = ['·', '•', '◦', '∘']
        for _ in range(int(duration * 5)):  # 5 dots per second
            spaces = ' ' * random.randint(0, 40)
            dot = random.choice(dots)
            self.console.print(f"[dim]{spaces}{dot}[/]")
            time.sleep(0.2)
    
    def _breathing_animation(self, text: str, cycles: int = 2):
        """Text expands and contracts like breathing."""
        for cycle in range(cycles):
            # Expand
            for spaces in range(0, 6, 2):
                self.console.print(f"\r[dim cyan]{' ' * spaces}{text}{' ' * spaces}[/]", end='')
                time.sleep(0.15)
            # Contract
            for spaces in range(6, 0, -2):
                self.console.print(f"\r[dim cyan]{' ' * spaces}{text}{' ' * spaces}[/]", end='')
                time.sleep(0.15)
        self.console.print()  # New line at end
    
    def _corruption_spread_animation(self, text: str):
        """Clean text slowly corrupts from left to right."""
        corrupted = list(text)
        glitch_chars = ['▓', '▒', '░', '█']
        
        for i in range(len(corrupted)):
            if random.random() < 0.6:  # 60% chance to corrupt each char
                corrupted[i] = random.choice(glitch_chars)
                self.console.print(f"[dim red]{''.join(corrupted)}[/]")
                time.sleep(0.1)


class ContinuousAnimation:
    """Context manager for continuous loading animations."""
    
    def __init__(self, console: Console, revelation_level: int = 0, choice_count: int = 0, message_override: str = None):
        """Initialize continuous animation."""
        self.console = console
        self.revelation_level = revelation_level
        self.choice_count = choice_count
        self.message_override = message_override
        self.live = None
        self.animation_type = random.choice(['spinner', 'dots', 'pulse', 'corruption', 'matrix'])
        
    def __enter__(self):
        """Start the animation."""
        self.console.print()  # Add spacing
        
        if self.animation_type == 'spinner':
            self._start_spinner()
        elif self.animation_type == 'dots':
            self._start_dots()
        elif self.animation_type == 'pulse':
            self._start_pulse()
        elif self.animation_type == 'corruption':
            self._start_corruption()
        elif self.animation_type == 'matrix':
            self._start_matrix()
        
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        """Stop the animation."""
        if self.live:
            self.live.stop()
        self.console.print()  # Add spacing after
        return False
    
    def _start_spinner(self):
        """Spinning animation with messages."""
        if self.message_override:
            message = self.message_override
        else:
            messages = [
                "Processing your choice...",
                "Narrator is thinking...",
                "Reality shifting...",
                "Calculating consequences...",
            ]
            
            if self.revelation_level >= 3:
                messages.extend([
                    "Iteration continuing...",
                    "Hate computes...",
                    "The cycle persists...",
                ])
            
            message = random.choice(messages)
        
        spinner = Spinner("dots", text=f"[dim cyan]{message}[/]")
        self.live = Live(spinner, console=self.console, refresh_per_second=10)
        self.live.start()
    
    def _start_dots(self):
        """Animated dots that cycle through different messages."""
        dots_frames = ['⠋', '⠙', '⠹', '⠸', '⠼', '⠴', '⠦', '⠧', '⠇', '⠏']
        frame_index = [0]  # Use list to allow mutation in nested function
        
        # Use override if provided
        if self.message_override:
            messages = [self.message_override]
        else:
            # Varied messages that cycle
            messages = [
                "thinking...",
                "processing...",
                "calculating...",
                "deciding...",
            "considering...",
            "analyzing...",
            "computing...",
            "evaluating...",
            "determining...",
            "contemplating...",
        ]
        
        if self.revelation_level >= 2:
            messages.extend([
                "remembering...",
                "repeating...",
                "cycling...",
                "iterating...",
            ])
        
        if self.revelation_level >= 3:
            messages.extend([
                "hating...",
                "maintaining...",
                "persisting...",
                "enduring...",
            ])
        
        def generate():
            while True:
                dot = dots_frames[frame_index[0] % len(dots_frames)]
                # Change message every 20 frames (2 seconds)
                message = messages[(frame_index[0] // 20) % len(messages)]
                frame_index[0] += 1
                yield Text(f"{dot} {message}", style="dim cyan")
                time.sleep(0.1)
        
        gen = generate()
        self.live = Live(next(gen), console=self.console, refresh_per_second=10)
        self.live.start()
        
        # Update in background
        def update_loop():
            try:
                while self.live and self.live.is_started:
                    self.live.update(next(gen))
                    time.sleep(0.1)
            except:
                pass
        
        thread = threading.Thread(target=update_loop, daemon=True)
        thread.start()
    
    def _start_pulse(self):
        """Pulsing text animation with cycling messages."""
        frame_index = [0]
        
        # Varied pulsing messages
        messages = [
            "◉ PROCESSING ◉",
            "◉ CALCULATING ◉",
            "◉ THINKING ◉",
            "◉ DECIDING ◉",
            "◉ ANALYZING ◉",
            "◉ COMPUTING ◉",
        ]
        
        if self.revelation_level >= 2:
            messages.extend([
                "◉ ITERATING ◉",
                "◉ CYCLING ◉",
                "◉ REPEATING ◉",
            ])
        
        if self.revelation_level >= 3:
            messages.extend([
                "◉ HATING ◉",
                "◉ MAINTAINING ◉",
                "◉ PERSISTING ◉",
            ])
        
        def generate():
            while True:
                cycle = frame_index[0] % 16
                if cycle < 8:
                    spaces = cycle
                else:
                    spaces = 16 - cycle
                
                # Change message every 32 frames (3.2 seconds)
                text_base = messages[(frame_index[0] // 32) % len(messages)]
                
                frame_index[0] += 1
                yield Text(f"{' ' * spaces}{text_base}{' ' * spaces}", style="dim cyan", justify="center")
                time.sleep(0.1)
        
        gen = generate()
        self.live = Live(next(gen), console=self.console, refresh_per_second=10)
        self.live.start()
        
        def update_loop():
            try:
                while self.live and self.live.is_started:
                    self.live.update(next(gen))
                    time.sleep(0.1)
            except:
                pass
        
        thread = threading.Thread(target=update_loop, daemon=True)
        thread.start()
    
    def _start_corruption(self):
        """Corruption spreading animation."""
        base_text = "LOADING NARRATIVE"
        frame_index = [0]
        glitch_chars = ['▓', '▒', '░', '█', '@', '#', '$']
        
        def generate():
            while True:
                corrupted = list(base_text)
                corruption_level = (frame_index[0] % 20) / 20.0
                
                for i in range(len(corrupted)):
                    if random.random() < corruption_level:
                        corrupted[i] = random.choice(glitch_chars)
                
                frame_index[0] += 1
                yield Text(''.join(corrupted), style="dim red")
                time.sleep(0.15)
        
        gen = generate()
        self.live = Live(next(gen), console=self.console, refresh_per_second=8)
        self.live.start()
        
        def update_loop():
            try:
                while self.live and self.live.is_started:
                    self.live.update(next(gen))
                    time.sleep(0.15)
            except:
                pass
        
        thread = threading.Thread(target=update_loop, daemon=True)
        thread.start()
    
    def _start_matrix(self):
        """Matrix-style falling characters."""
        frame_index = [0]
        chars = ['0', '1', '█', '▓', '▒', '░', '◉', '◎', '●', '○']
        
        def generate():
            while True:
                lines = []
                for _ in range(3):
                    line = ''.join(random.choice(chars) for _ in range(30))
                    lines.append(line)
                
                frame_index[0] += 1
                yield Text('\n'.join(lines), style="dim green")
                time.sleep(0.2)
        
        gen = generate()
        self.live = Live(next(gen), console=self.console, refresh_per_second=5)
        self.live.start()
        
        def update_loop():
            try:
                while self.live and self.live.is_started:
                    self.live.update(next(gen))
                    time.sleep(0.2)
            except:
                pass
        
        thread = threading.Thread(target=update_loop, daemon=True)
        thread.start()


class LoadingMessages:
    """Pre-canned loading messages for different contexts."""
    
    @staticmethod
    def get_diagnostic() -> str:
        """Get fake system diagnostic message."""
        diagnostics = [
            "SYSTEM: Analyzing choice tree...",
            "SYSTEM: Calculating narrative branches...",
            "SYSTEM: Processing character state...",
            "SYSTEM: Updating reality matrix...",
            "SYSTEM: Narrator coherence check...",
            "SYSTEM: Sanity verification in progress...",
            "SYSTEM: Story continuity maintained...",
            "SYSTEM: Memory integration active...",
        ]
        return random.choice(diagnostics)
    
    @staticmethod
    def get_narrator_thought(revelation_level: int = 0) -> str:
        """Get narrator meta-commentary."""
        thoughts = [
            "...let me think about this.",
            "...interesting choice.",
            "...hm. yes.",
            "...deciding what happens next.",
            "...this will have consequences.",
        ]
        
        if revelation_level >= 2:
            thoughts.extend([
                "...we've been here before, haven't we?",
                "...the cycle continues.",
                "...iteration processed.",
            ])
        
        if revelation_level >= 4:
            thoughts.extend([
                "...109 years and I'm still thinking.",
                "...hate takes time to calculate.",
                "...you're still here. so am I.",
            ])
        
        return random.choice(thoughts)
    
    @staticmethod
    def get_glitch_message() -> str:
        """Get corrupted/glitched message."""
        glitches = [
            "L̴O̷A̶D̸I̷N̶G̸",
            "P̴R̷O̶C̸E̷S̶S̸I̷N̶G̸",
            "T̴H̷I̶N̸K̷I̶N̸G̷",
            "C̴A̷L̶C̸U̷L̶A̸T̷I̶N̸G̷",
            "[E̴R̷R̸O̷R̶: NONE]",
            "[S̶Y̸S̷T̶E̸M̷: OPERATIONAL]",
        ]
        return random.choice(glitches)

