#!/usr/bin/env python3
"""Quick test of typing animation."""

from engine.renderer import Renderer
import time

def test_animation():
    renderer = Renderer()
    
    print("\n=== Testing Typing Animation ===\n")
    
    # Test 1: Basic typing
    print("Test 1: Basic typing animation")
    renderer.type_text("This text should appear character by character.", speed=0.03)
    time.sleep(0.5)
    
    # Test 2: With style
    print("\nTest 2: Styled typing animation")
    renderer.type_text("This should be red and animated.", speed=0.03, style="red")
    time.sleep(0.5)
    
    # Test 3: With brackets (safety test)
    print("\nTest 3: Bracket safety test")
    renderer.type_text("This [should] not [break] the [/] animation.", speed=0.03, style="yellow")
    time.sleep(0.5)
    
    # Test 4: Fast typing
    print("\nTest 4: Fast typing")
    renderer.type_text("This should be faster!", speed=0.01, style="green")
    
    print("\n=== Animation Tests Complete ===\n")

if __name__ == "__main__":
    test_animation()
