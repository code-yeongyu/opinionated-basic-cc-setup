"""Hook test module to verify language guide injection."""

from typing import Final


MAX_RETRIES: Final[int] = 3


def calculate_sum(numbers: list[int]) -> int:
    """
    Calculate the sum of a list of numbers.

    Args:
        numbers: List of integers to sum

    Returns:
        The total sum of all numbers
    """
    return sum(numbers)


async def fetch_data(url: str, *, timeout: int = 30) -> dict[str, str]:
    """
    Fetch data from a URL asynchronously.

    Args:
        url: The URL to fetch data from
        timeout: Request timeout in seconds

    Returns:
        Dictionary containing the fetched data
    """
    import asyncio

    await asyncio.sleep(0.1)
    return {"url": url, "status": "success"}


if __name__ == "__main__":
    result = calculate_sum([1, 2, 3, 4, 5])
    print(f"Sum: {result}")
