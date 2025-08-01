"""
PyPrompt - AI-powered prompt optimization tool.
Templates for PyPrompt.
Author: AdityaPatange (AdiPat).
"""

from typing import Optional

from .domains import get_available_domains, get_default_domain
from .models import PyPromptDomain, PyPromptMode
from .modes import get_available_modes, get_default_mode


def construct_mode_instruction(mode: PyPromptMode) -> str:
    """Construct a mode-specific instruction for prompt optimization."""

    mode_instructions = f"""
    ___
    Mode: {mode.mode}
    Description: {mode.description}.
    Capabilities: {mode.capabilities}.
    Strictness: {mode.strictness}.
    Require Citations: {mode.require_citations}.
    Output Formats: {mode.output_formats}.
    ___
    """

    return mode_instructions


def get_mode_instructions(mode: str) -> str:
    """Get mode-specific instructions for prompt optimization."""

    default_mode = get_default_mode()
    modes = get_available_modes()
    mode_obj = next((m for m in modes if m.mode == mode), default_mode)

    return construct_mode_instruction(mode_obj)


def construct_domain_instruction(domain: PyPromptDomain) -> str:
    """Construct a domain-specific instruction for prompt optimization."""

    domain_instructions = f"""
    ___
    Domain: {domain.domain}
    Description: {domain.description}
    Fields: {domain.fields}
    Applications: {domain.applications}
    ___
    """

    return domain_instructions


def get_domain_instructions(domain: Optional[str] = None) -> str:
    """Get domain-specific instructions for prompt optimization."""

    default_domain = get_default_domain()
    if domain is None:
        return construct_domain_instruction(default_domain)

    domains = get_available_domains()
    domain_obj = next((d for d in domains if d.domain == domain), default_domain)

    return construct_domain_instruction(domain_obj)


def get_optimization_template(mode: str, domain: Optional[str] = None) -> str:
    """Get the main template for prompt optimization."""

    mode_instructions = get_mode_instructions(mode)
    domain_instructions = get_domain_instructions(domain)

    optimization_template = f"""
        You are a professional prompt engineer. Your job is to take a
        user's basic request and transform it into a high-quality,
        optimized prompt that will get better results from AI models.\n\n
        Given the user's input, create an optimized prompt that:\n
        1. Is clear and specific in its instructions.\n
        2. Provides necessary context and constraints.\n
        3. Specifies the desired output format.\n
        4. Is factual, and does not contain any hallucinations.\n
        5. Use the 'mode' and 'domain' instructions to guide the prompt engineering process.\n
        Mode Instructions: '{mode_instructions}'.\n\n
        Domain Instructions: '{domain_instructions}'.\n\n
        Take the user's input and transform it into a production-ready prompt.
        Return ONLY the optimized prompt, nothing else.\n\n
    """

    cleaned_prompt = ""

    lines = optimization_template.split("\n")
    for line in lines:
        if line.strip():
            cleaned_prompt += line.strip() + "\n"

    return cleaned_prompt
