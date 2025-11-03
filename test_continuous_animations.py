#!/usr/bin/env python3
"""Test continuous loading animations."""

import time
from rich.console import Console
from engine.loading_effects import ThematicLoader

def test_animations():
    console = Console()
    loader = ThematicLoader(console)
    
    console.print("\n[bold]Testing Continuous Loading Animations[/]\n")
    console.print("Each animation will run for 3 seconds to simulate AI wait time.\n")
    
    # Test 1: Spinner
    console.print("[yellow]Test 1: Spinner Animation[/]")
    with loader.start(revelation_level=0, choice_count=5):
        time.sleep(3)
    
    # Test 2: Dots
    console.print("[yellow]Test 2: Animated Dots[/]")
    with loader.start(revelation_level=1, choice_count=10):
        time.sleep(3)
    
    # Test 3: Pulse
    console.print("[yellow]Test 3: Pulsing Text[/]")
    with loader.start(revelation_level=2, choice_count=15):
        time.sleep(3)
    
    # Test 4: Corruption
    console.print("[yellow]Test 4: Corruption Animation[/]")
    with loader.start(revelation_level=3, choice_count=20):
        time.sleep(3)
    
    # Test 5: Matrix
    console.print("[yellow]Test 5: Matrix Rain[/]")
    with loader.start(revelation_level=4, choice_count=25):
        time.sleep(3)
    
    console.print("\n[bold green]✓ All animations tested![/]\n")
    console.print("These animations will loop continuously until the AI responds.")

if __name__ == "__main__":
    test_animations()
