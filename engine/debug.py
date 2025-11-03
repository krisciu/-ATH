"""Global debug flag system for ~ATH."""

class DebugManager:
    """Singleton manager for debug output."""
    _instance = None
    _debug_enabled = False
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance
    
    @classmethod
    def enable(cls):
        """Enable debug output."""
        cls._debug_enabled = True
        print("\n[DEBUG SYSTEM] Debug output ENABLED")
    
    @classmethod
    def disable(cls):
        """Disable debug output."""
        cls._debug_enabled = False
        print("\n[DEBUG SYSTEM] Debug output DISABLED\n")
    
    @classmethod
    def toggle(cls):
        """Toggle debug output."""
        if cls._debug_enabled:
            cls.disable()
        else:
            cls.enable()
    
    @classmethod
    def is_enabled(cls) -> bool:
        """Check if debug is enabled."""
        return cls._debug_enabled
    
    @classmethod
    def log(cls, message: str):
        """Log a debug message if debug is enabled."""
        if cls._debug_enabled:
            print(message)


# Convenience function
def debug_log(message: str):
    """Log a debug message if debug is enabled."""
    DebugManager.log(message)

