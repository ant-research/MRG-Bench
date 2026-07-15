"""LLM adapter interface.

Users MUST implement their own LLM backend and register it via set_adapter().
See the docstring of set_adapter() for the required function signature.
"""

import sys
import os
from pathlib import Path
from typing import List, Dict, Optional, Callable, Tuple

_AdapterFn = Callable[..., Optional[Tuple[str, str]]]


def _default_adapter(
    model: str,
    api_key: Optional[str],
    messages: List[Dict[str, str]],
    *,
    enable_think: bool = False,
) -> Optional[Tuple[str, str]]:
    """Placeholder adapter that raises NotImplementedError.

    Replace this by calling set_adapter() with your own implementation.
    """
    raise NotImplementedError(
        "No LLM adapter configured. "
        "Define your own adapter function and register it via call_llm.set_adapter(). "
        "The adapter must have the signature:\n"
        "  adapter(model: str, api_key: Optional[str], messages: List[Dict[str, str]], "
        "*, enable_think: bool = False) -> Optional[Tuple[str, str]]\n"
        "Returns (content, reasoning_content) on success, or None on failure."
    )


_adapter = _default_adapter


def set_adapter(fn: _AdapterFn) -> None:
    """Register a user-provided LLM backend.

    The adapter function must follow this signature:

        def my_adapter(
            model: str,
            api_key: Optional[str],
            messages: List[Dict[str, str]],
            *,
            enable_think: bool = False,
        ) -> Optional[Tuple[str, str]]:
            ...

    Parameters:
        model: Name of the model to call (e.g. "gpt-4", "claude-3-opus").
        api_key: API key for authentication.
        messages: List of {"role": "...", "content": "..."} dicts representing
                  the full conversation history.
        enable_think: Whether to enable reasoning/thinking output (chain-of-thought).

    Returns:
        A tuple (content, reasoning_content) on success.
        content: The model's text response.
        reasoning_content: The model's internal reasoning (if enabled), or empty string.
        Return None on any failure (network error, empty response, etc.).

    Example:
        >>> import openai
        >>> def my_adapter(model, api_key, messages, *, enable_think=False):
        ...     client = openai.OpenAI(api_key=api_key)
        ...     resp = client.chat.completions.create(
        ...         model=model, messages=messages,
        ...     )
        ...     return (resp.choices[0].message.content, "")
        >>> set_adapter(my_adapter)
    """
    global _adapter
    _adapter = fn


def call_llm(
    model: str,
    api_key: Optional[str],
    messages: List[Dict[str, str]],
    *,
    enable_think: bool = False,
) -> Optional[Tuple[str, str]]:
    """Call the LLM backend via the registered adapter.

    Returns (content, reasoning_content) on success, or None on failure.
    """
    return _adapter(model=model, api_key=api_key, messages=messages, enable_think=enable_think)
