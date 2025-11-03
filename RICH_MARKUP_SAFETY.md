# Rich Markup Safety Guide

## The Problem

Rich console uses square brackets `[` and `]` for markup tags like `[bold]`, `[red]`, `[/]`, etc. When AI-generated content or error messages contain these characters, Rich tries to parse them as markup, causing `MarkupError: closing tag '[/]' has nothing to close`.

## The Solution

Always escape brackets in dynamic/user-generated content before passing to `console.print()`:

```python
safe_text = text.replace('[', '\\[').replace(']', '\\]')
self.renderer.console.print(safe_text, style="...")
```

Or use the helper function:

```python
safe_text = Renderer.escape_markup(text)
self.renderer.console.print(safe_text, style="...")
```

## Protected Locations

### ✅ Already Protected

1. **`main.py` line 389** - Error messages in exception handler
2. **`main.py` line 125** - AI-generated ending narratives
3. **`main.py` line 181** - Mutation special messages
4. **`engine/renderer.py` line 75** - `type_text()` animation function

### 🔍 Safe (No Escaping Needed)

These use only hard-coded strings or safe data:

- **`main.py` line 114-137** - Ending display (uses `=` characters and numbers)
- **`main.py` line 250** - Consequence feedback (from predefined list)
- **`main.py` line 299** - Narrator choice selection (uses numbers)
- **`main.py` line 308** - Pattern response (from truth tracker, predefined)
- **`main.py` line 315** - Choice gaslighting (uses numbers)

## Animation System

### Fixed: `type_text()` Function

**Problem**: Was using `console.print()` per character without proper live updates, causing instant display instead of animation.

**Solution**: Now uses Rich's `Live` display with `Text` object for proper character-by-character animation:

```python
from rich.live import Live
from rich.text import Text

with Live(displayed_text, console=self.console, refresh_per_second=30) as live:
    for char in safe_text:
        displayed_text.append(char, style=style)
        live.update(displayed_text)
        time.sleep(speed)
```

This provides:
- ✅ Smooth character-by-character typing
- ✅ Proper color styling
- ✅ Safe markup escaping
- ✅ Variable speed based on intensity

## Best Practices

1. **Always escape AI-generated content** - narratives, choices, endings
2. **Always escape error messages** - they often contain brackets
3. **Use `Renderer.escape_markup()` helper** - consistent escaping
4. **Test with bracket-heavy content** - `"test [bold] text [/]"`
5. **Use plain `print()` for tracebacks** - avoid nested Rich parsing

## Testing

To test markup safety, try generating content with:
- `"This [should] not break"`
- `"Error: closing tag '[/]' found"`
- `"[SYSTEM] message [/END]"`

All should display as literal text, not cause parsing errors.

