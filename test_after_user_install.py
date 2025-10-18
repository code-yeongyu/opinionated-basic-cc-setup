#!/usr/bin/env python3
"""Test file after user-level plugin installation."""


def test_hooks():
    """Test if hooks are now working."""
    print("Testing hooks after user-level installation")
    return True


if __name__ == "__main__":
    test_hooks()
