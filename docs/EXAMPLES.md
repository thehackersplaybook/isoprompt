# PyPrompt Examples.

## Basic Usage.

```python
from pyprompt import optimize_prompt

# Simple prompt optimization.
prompt = "Write a blog post about AI"
optimized = optimize_prompt(prompt)
print(optimized)
```

## Advanced Usage.

### Using Different Modes.

```python
from pyprompt import optimize_prompt, get_available_modes

# List available modes.
modes = get_available_modes()
for mode in modes:
    print(f"{mode.mode}: {mode.description}")

# Use analytical mode.
optimized = optimize_prompt(
    "Write a technical analysis",
    mode="analytical",
    temperature=0.5
)
```

### Domain Specialization.

```python
from pyprompt import optimize_prompt, get_available_domains

# List available domains.
domains = get_available_domains()
for domain in domains:
    print(f"{domain.domain}: {domain.description}")

# Use technology domain.
optimized = optimize_prompt(
    "Write a technical specification",
    domain="technology",
    mode="analytical"
)
```

### Configuration.

```python
# Load configuration from file.
with open("config.json", "r") as f:
    config = json.load(f)

# Use configuration.
optimized = optimize_prompt(
    "Write documentation",
    **config
)
```

## Command Line Usage.

```bash
# Simple prompt
pyprompt --prompt "Write a blog post about AI"

# With mode and domain
pyprompt --prompt "Write a technical spec" --mode analytical --domain technology
```
