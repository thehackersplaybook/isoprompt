"""
PyPrompt - AI-powered prompt optimization tool.
Data structures for PyPrompt.
Author: AdityaPatange (AdiPat).
"""

from typing import List

from pydantic import BaseModel


class PyPromptMode(BaseModel):
    """
    A model for a PyPrompt mode.

    Args:
        mode_id: The ID of the mode.
        mode_name: The name of the mode.
        mode_description: The description of the mode.
        mode_usage: The usage of the mode.
        mode_industries: The industries of the mode.
        mode_topics: The topics of the mode.
    """

    mode: str
    description: str
    usage: str
    capabilities: List[str]
    strictness: str
    require_citations: bool
    output_formats: List[str]
    industries: List[str]
    topics: List[str]


class PyPromptDomain(BaseModel):
    """
    A model for a PyPrompt domain.

    Args:
        domain: The ID of the domain.
        description: The description of the domain.
        fields: The fields of the domain.
        applications: The applications of the domain.
    """

    domain: str
    description: str
    fields: List[str] = []
    applications: List[str] = []
