# PyPrompt.

Type lazy, get more. Transform simple queries into high-quality, production-grade prompts for LLMs.

PyPrompt [`pyprompt`] offers prompt optimization via a simple, user-friendly CLI and programmable API SDK.

## Documentation.

- [Getting Started](docs/GETTING_STARTED.md).
- [API Reference](docs/API_REFERENCE.md).
- [Examples](docs/EXAMPLES.md).

## Quick Start (SDK).

```python
from pyprompt import optimize_prompt

prompt = "Write a blog post about AI"
optimized = optimize_prompt(prompt)
print(optimized)
```

## Quick Start (CLI).

```bash
pyprompt --prompt "Generate a fitness plan for students."
```

## Installation.

```bash
pip install pyprompt
```

## Development.

```bash
# Install development dependencies.
make install-dev

# Run tests.
make test

# Run linter.
make lint

# Run all checks.
make validate
```

## License.

MIT License - see [LICENSE](LICENSE) for details.
