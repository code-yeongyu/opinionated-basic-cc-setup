"""Simple test module to verify plugin functionality."""

from typing import Protocol


class Greeter(Protocol):
    """Protocol for greeting functionality."""

    def greet(self, name: str) -> str:
        """Return a greeting message."""
        ...


def create_greeting(name: str, *, formal: bool = False) -> str:
    """
    Create a personalized greeting message.

    Args:
        name: The name of the person to greet
        formal: Whether to use formal greeting style

    Returns:
        A formatted greeting string
    """
    if formal:
        return f"Good day, {name}. It is a pleasure to meet you."
    return f"Hello, {name}! Nice to meet you."


async def fetch_user_greeting(user_id: int) -> str:
    """
    Fetch and create a greeting for a user asynchronously.

    Args:
        user_id: The unique identifier of the user

    Returns:
        A personalized greeting message
    """
    # Simulate async operation
    import asyncio

    await asyncio.sleep(0.1)
    return create_greeting(f"User-{user_id}")


if __name__ == "__main__":
    # Example usage
    print(create_greeting("World"))
    print(create_greeting("Sir", formal=True))
