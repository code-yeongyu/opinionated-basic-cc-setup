"""Example feature module to test plugin hooks."""

from typing import Protocol


class DataProcessor(Protocol):
    """Protocol for data processing functionality."""

    def process(self, data: str) -> dict[str, str]:
        """Process input data."""
        ...


def validate_input(data: str, *, strict: bool = False) -> bool:
    """
    Validate input data format.

    Args:
        data: The input string to validate
        strict: Whether to use strict validation rules

    Returns:
        True if validation passes, False otherwise
    """
    if not data:
        return False

    if strict:
        return data.isalnum()

    return len(data) > 0


async def process_async_data(items: list[str]) -> list[dict[str, str]]:
    """
    Process multiple items asynchronously.

    Args:
        items: List of items to process

    Returns:
        List of processed results
    """
    import asyncio

    await asyncio.sleep(0.1)

    return [{"item": item, "status": "processed"} for item in items]


if __name__ == "__main__":
    print(validate_input("test"))
    print(validate_input("test-123", strict=True))
