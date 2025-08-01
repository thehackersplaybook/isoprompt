"""PyPrompt - AI-powered prompt optimization tool."""

__version__ = "1.0.0"
__author__ = "Aditya Patange (AdiPat)"
__email__ = "zero@thehackersplaybook.org"

# CLI entry point
from .cli import main
from .domains import get_available_domain_names, get_available_domains
from .modes import get_available_mode_names, get_available_modes

# New main API
from .optimizer import (
    optimize_prompt,
    validate_config,
)

__all__ = [
    # Main API
    "optimize_prompt",
    "get_available_modes",
    "get_available_domains",
    "get_available_mode_names",
    "get_available_domain_names",
    "validate_config",
    # CLI
    "main",
    # Metadata
    "__version__",
]
