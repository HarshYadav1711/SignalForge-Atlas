class SignalForgeError(Exception):
    """Base exception type for recoverable domain errors."""


class ConfigurationError(SignalForgeError):
    """Raised when required runtime configuration is missing."""
