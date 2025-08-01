#!/usr/bin/env python3
"""
Command-line interface for PyPrompt, prompt optimization a command away.
Type lazy, get more. Transform basic prompts into optimized, production-ready prompts with domain-tuning.
Author: AdityaPatange (AdiPat).
"""

import argparse
import sys
import time
import traceback
from pathlib import Path

from dotenv import load_dotenv

from .constants import DEFAULT_LLM_MODEL, DEFAULT_TEMPERATURE
from .domains import get_default_domain
from .modes import get_default_mode
from .optimizer import (
    get_available_domain_names,
    get_available_mode_names,
    optimize_prompt,
    validate_config,
)


def create_parser() -> argparse.ArgumentParser:
    """Create and configure the argument parser."""
    parser = argparse.ArgumentParser(
        prog="pyprompt",
        description="Type lazy, get more. Transform basic prompts into optimized, production-ready prompts with domain-tuning.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
    Examples:
    # Basic optimization.
    pyprompt --prompt "write a blog post about AI"

    # With domain specialization.
    pyprompt --prompt "optimize our supply chain" --domain supply_chain

    # Creative mode with refinement.
    pyprompt --prompt "marketing campaign ideas" --mode creative --refine

    # From file input.
    pyprompt --input basic_prompt.txt --output optimized_prompt.txt
        """,
    )

    # Input options: You can either provide a prompt or an input file.
    input_group = parser.add_mutually_exclusive_group(required=True)
    input_group.add_argument(
        "--prompt", "-p", type=str, help="Basic prompt to optimize."
    )
    input_group.add_argument(
        "--input", "-i", type=str, help="File containing basic prompt."
    )

    # Output file can be passed regardless of input type.
    parser.add_argument(
        "--output",
        "-o",
        type=str,
        help="Save optimized prompt to file. If not provided, the optimized prompt will be printed to the console.",
    )

    # Optimization options: You can choose a mode and domain.
    mode_choices = get_available_mode_names()
    parser.add_argument(
        "--mode",
        "-m",
        type=str,
        choices=mode_choices,
        default=get_default_mode().mode,
        help=f"Optimization mode (default: {get_default_mode().mode}).",
    )

    parser.add_argument(
        "--domain",
        "-d",
        type=str,
        choices=get_available_domain_names(),
        help=f"Domain specialization (default: {get_default_domain().domain}).",
    )

    # Refinement options
    parser.add_argument(
        "--refine",
        "-r",
        action="store_true",
        help="Apply additional refinement to the optimized prompt.",
    )

    # Model options
    parser.add_argument(
        "--model",
        type=str,
        default=DEFAULT_LLM_MODEL,
        help=f"OpenAI model for optimization (default: {DEFAULT_LLM_MODEL}).",
    )

    parser.add_argument(
        "--temperature",
        "-t",
        type=float,
        default=DEFAULT_TEMPERATURE,
        help=f"Temperature for optimization, must be between 0.0 and 2.0 (default: {DEFAULT_TEMPERATURE}).",
    )

    # Utility options
    parser.add_argument("--version", action="version", version="pyprompt v1.0.0.")

    parser.add_argument(
        "--verbose", "-v", action="store_true", help="Show detailed output."
    )

    return parser


def load_prompt_from_file(file_path: str) -> str:
    """
    Load prompt text from file.

    Args:
        file_path: The path to the file containing the prompt.

    Returns:
        The prompt text.
    """
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            return f.read().strip()
    except FileNotFoundError:
        print(f"Error: File '{file_path}' not found", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"Error reading file: {e}", file=sys.stderr)
        sys.exit(1)


def save_prompt_to_file(prompt: str, file_path: str) -> None:
    """
    Save optimized prompt to file.

    Args:
        prompt: The optimized prompt to save.
        file_path: The path to the file to save the prompt to.
    """
    try:
        output_path = Path(file_path)
        output_path.parent.mkdir(parents=True, exist_ok=True)

        with open(output_path, "w", encoding="utf-8") as f:
            f.write(prompt)

        print(f"✓ Optimized prompt saved to: {file_path}")
    except Exception as e:
        print(f"Error saving file: {e}", file=sys.stderr)
        sys.exit(1)


def generate_input_preview(user_input: str) -> str:
    """
    Generate a preview of the input prompt.
    """
    return f"INPUT: [{user_input[:100]}...]."


def format_output(optimized: str) -> str:
    """
    Format the output prompt.
    """
    return f"OPTIMIZED PROMPT: `{optimized}`."


def load_env() -> None:
    """
    Load the environment variables from the .env file.
    """
    env_loaded = load_dotenv(dotenv_path=".env")
    if env_loaded:
        print("🔧 Environment variables loaded from .env file.")
    else:
        print("🔧 No .env file found. Using default environment variables.")
        print("🔧 Please create a .env file with the following variables:")
        print("🔧 OPENAI_API_KEY=your_api_key")


def main() -> None:
    """
    Run the main CLI entry point.

    Args:
        None

    Returns:
        None
    """

    load_env()

    parser = create_parser()
    args = parser.parse_args()

    # Get input prompt
    if args.prompt:
        user_input = args.prompt
    elif args.input:
        user_input = load_prompt_from_file(args.input)
    else:
        print("Error: No prompt provided.", file=sys.stderr)
        sys.exit(1)

    if not user_input.strip():
        print("Error: Empty prompt provided.", file=sys.stderr)
        sys.exit(1)

    # Validate configuration
    config = {
        "mode": args.mode,
        "domain": args.domain,
        "temperature": args.temperature,
        "model": args.model,
    }

    try:
        validate_config(config)
    except ValueError as e:
        print(f"Configuration error: {e}.")
        print(
            "Please check if you have passed correct arguments, run --help for more information."
        )
        traceback.print_exc()
        sys.exit(1)

    if args.verbose:
        print(generate_input_preview(user_input))
        print(f"Mode: {args.mode}")
        if args.domain:
            print(f"Domain: {args.domain}")

    try:
        # Optimize the prompt
        start_time = time.time()
        print("🔧 Starting PyPrompt run now.")
        optimized = optimize_prompt(
            user_input=user_input,
            mode=args.mode,
            domain=args.domain,
            model=args.model,
            temperature=args.temperature,
            verbose=args.verbose,
        )
        end_time = time.time()
        duration = end_time - start_time

        # Output result
        print(
            f"🎉 PyPrompt Run Complete: Prompt optimization succeeded in {duration:.2f} seconds."
        )
        if args.output:
            save_prompt_to_file(optimized, args.output)
        else:
            print(format_output(optimized))

        if not args.output:
            print("💡 Tip: Use --output to save the optimized prompt to a file.")

    except Exception as e:
        print("Error: PyPrompt run failed: " + str(e) + ".")
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
