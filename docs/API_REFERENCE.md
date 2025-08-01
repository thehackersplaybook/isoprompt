# PyPrompt API Reference.

## Core Functions.

### Optimize Prompt.

```python
def optimize_prompt(
    user_input: str,
    mode: str = "simple",
    domain: Optional[str] = None,
    model: str = "gpt-4.1-nano",
    temperature: float = 0.7,
) -> str
```

Optimizes a user's basic prompt into a high-quality, production-ready prompt.

### Validate Config.

```python
def validate_config(config: Dict[str, Any]) -> None
```

Validates configuration parameters for prompt optimization.

## Modes and Domains.

### Get available modes.

```python
def get_available_modes() -> List[PyPromptMode]
```

Gets a list of available optimization modes with metadata.

### Get available domains.

```python
def get_available_domains() -> List[PyPromptDomain]
```

Gets a list of available domains with metadata.
