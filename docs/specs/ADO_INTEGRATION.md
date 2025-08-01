# Specification: ADO Integration in IsoPrompt

**Paper:** [ADO: Automatic Data Optimization for Inputs in LLM Prompts.](https://arxiv.org/abs/2502.11436)

```text
@misc{lin2025adoautomaticdataoptimization,
      title={ADO: Automatic Data Optimization for Inputs in LLM Prompts},
      author={Sam Lin and Wenyue Hua and Lingyao Li and Zhenting Wang and Yongfeng Zhang},
      year={2025},
      eprint={2502.11436},
      archivePrefix={arXiv},
      primaryClass={cs.LG},
      url={https://arxiv.org/abs/2502.11436},
}
```

## 1. **Overview**

Enable users to automatically optimize the input data part of prompts using ADO methods (content engineering + structural reformulation), as a first-class, configurable argument in IsoPrompt. This should work for both the Python SDK and CLI.

## 2. **API Additions**

### **Python API**

**Signature Change:**

```python
def optimize_prompt(
    user_input: str,
    mode: str = "simple",
    domain: Optional[str] = None,
    model: str = "gpt-4",
    temperature: float = 0.7,
    data: Optional[Union[dict, str]] = None,       # NEW
    ado: Union[bool, dict] = False,                # NEW: if dict, allows for custom ADO settings
    verbose: bool = False,
) -> str:
    ...
```

- `data`: Optional. Structured or unstructured data (e.g., dict, JSON string, CSV string) to be inserted/optimized within the prompt.
- `ado`: Optional.

  - If `False`/unset: **No data optimization** (backwards-compatible).
  - If `True`: **Run ADO with default settings** before embedding data in the prompt.
  - If `dict`: **Run ADO with custom options** (see “ADO Options” below).

**Example Usage:**

```python
# Default
optimize_prompt("Analyze this health record for risks.", data=health_dict)

# With ADO (default settings)
optimize_prompt("Analyze this health record for risks.", data=health_dict, ado=True)

# With ADO (custom settings)
optimize_prompt(
    "Analyze this health record for risks.",
    data=health_dict,
    ado={"content": True, "format": "xml", "max_iters": 4}
)
```

---

### **CLI**

**New Flags:**

- `--ado` or `--auto-data-opt`
  Enable automatic data optimization for input data in prompt.
- `--ado-options`
  Pass JSON/YAML string for advanced ADO config.

**Example CLI Usage:**

```bash
# Standard
isoprompt --prompt "Analyze this record." --data health.json

# With ADO (default)
isoprompt --prompt "Analyze this record." --data health.json --ado

# With ADO options
isoprompt --prompt "Analyze this record." --data health.json --ado --ado-options '{"format":"xml","content":true,"max_iters":2}'
```

---

## 3. **ADO Configuration Options**

ADO accepts either a boolean (`True` = run with defaults) or a configuration dict for fine-grained control:

**Configurable fields:**

- `"content"`: (bool, default True) – Perform content engineering (impute, enrich, denoise)
- `"format"`: (str, default "auto") – Target structure, e.g. `"auto"`, `"xml"`, `"table"`, `"json"`, `"nl"` (natural language)
- `"max_iters"`: (int, default 3) – Maximum optimization rounds (controls DPS algorithm)
- `"diversity"`: (float, 0.0-1.0, default 0.5) – Controls candidate diversity in DPS
- `"factual_check"`: (bool, default True) – Enable/disable factual cross-validation step
- `"llm"`: (str, default None) – Which LLM to use for ADO (can override default)

**Defaults:**
If `ado=True`, use:

```python
{
  "content": True,
  "format": "auto",
  "max_iters": 3,
  "diversity": 0.5,
  "factual_check": True,
  "llm": None
}
```

---

## 4. **Programmatic Flow**

1. **If `ado` is enabled and `data` is present:**

   - Apply ADO pipeline (content + format optimization) on the provided data, using the config.
   - Replace/inject the optimized data into the prompt template.
   - Proceed with prompt optimization (existing IsoPrompt workflow).

2. **If `ado` is not set or `data` is not provided:**

   - Skip ADO, use data as-is.

---

## 5. **Extensibility & Future-Proofing**

- **Support for batch input:** (future)
  Allow lists of data; optimize each item.
- **Multiple data sections per prompt:**
  (e.g. in-context examples; optimize each)
- **Plug-in support:**
  Let advanced users plug in custom data optimization algorithms (via callback or module).

---

## 6. **User Documentation**

- Update main docs and API reference with:

  - What is ADO?
  - When to use it.
  - Example usage (Python and CLI).
  - List of available config options.

---

## 7. **Edge Cases & Error Handling**

- If `data` is missing/empty, ignore `ado` and warn if `verbose` is set.
- If ADO fails or times out, fallback to using unoptimized data, with a warning.
- If `format` is unrecognized, auto-select best guess.

---

## 8. **Testing Requirements**

- Tests for API and CLI:

  - With/without ADO
  - Various `data` types (dict, JSON, CSV, etc.)
  - With/without custom config
  - Edge cases (empty data, ADO failure)

---

## 9. **Sample Prompts for LLM Integration**

Maintain a library of meta-prompts/templates for common data types and tasks, as described in the ADO paper. Allow extension by users.

---

# **Summary Table**

| Arg Name      | Type      | Description                                       | Default |
| ------------- | --------- | ------------------------------------------------- | ------- |
| ado           | bool/dict | Enable/Configure automatic data optimization      | False   |
| data          | dict/str  | Input data to be optimized/integrated into prompt | None    |
| --ado         | flag      | (CLI) Enable ADO                                  | Off     |
| --ado-options | str       | (CLI) JSON/YAML config for ADO                    | None    |

---

## **One-Liner Summary**

> **Add an `ado` argument (API) and `--ado` flag (CLI) to IsoPrompt, enabling automatic data optimization on input data using LLM-based content and format refinement, configurable via dict or JSON string.**

---
