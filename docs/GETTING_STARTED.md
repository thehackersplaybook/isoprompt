# Getting Started with PyPrompt

## Installation

Install PyPrompt using pip:

```bash
pip install pyprompt
```

## Basic Usage

Here's a simple example:

```python
from pyprompt import optimize_prompt

# Simple prompt optimization
prompt = "Write a blog post about AI"
optimized = optimize_prompt(prompt)
print(optimized)
```

## Advanced Features

### Using Different Modes

PyPrompt supports various optimization modes:

```python
from pyprompt import optimize_prompt, get_available_modes

# List available modes
modes = get_available_modes()
for mode in modes:
    print(f"{mode.mode}: {mode.description}")

# Use analytical mode
optimized = optimize_prompt(
    "Write a technical analysis",
    mode="analytical",
    temperature=0.5
)
```

### Domain Specialization

You can optimize prompts for specific domains:

```python
from pyprompt import optimize_prompt, get_available_domains

# List available domains
domains = get_available_domains()
for domain in domains:
    print(f"{domain.domain}: {domain.description}")

# Use technology domain
optimized = optimize_prompt(
    "Write a technical specification",
    domain="technology",
    mode="analytical"
)
```

## Configuration

PyPrompt can be configured using a JSON file:

```json
{
  "mode": "analytical",
  "domain": "technology",
  "model": "gpt-4.1-nano",
  "temperature": 0.7
}
```

For more examples, see the [examples directory](../examples/).
