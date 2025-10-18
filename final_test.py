"""Final test module for hook verification."""

from typing import Protocol


class Calculator(Protocol):
    """Protocol for calculator operations."""

    def add(self, a: int, b: int) -> int:
        """Add two numbers."""
        ...


def multiply(x: int, y: int) -> int:
    """
    Multiply two numbers.

    Args:
        x: First number
        y: Second number

    Returns:
        Product of x and y
    """
    return x * y


async def async_operation(value: str) -> dict[str, str]:
    """
    Perform an async operation.

    Args:
        value: Input value to process

    Returns:
        Dictionary with processed result
    """
    import asyncio

    await asyncio.sleep(0.1)
    return {"result": value}


if __name__ == "__main__":
    print(multiply(5, 10))
