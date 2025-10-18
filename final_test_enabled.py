#!/usr/bin/env python3
"""Final test after enabling plugin."""


def test_enabled() -> str:
    """Test if plugin hooks work after enabling."""
    return "Testing enabled plugin"


if __name__ == "__main__":
    print(test_enabled())
