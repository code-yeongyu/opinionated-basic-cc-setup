"""Brand new test file for hook verification."""


def simple_function(name: str) -> str:
    """
    Simple greeting function.

    Args:
        name: Person's name

    Returns:
        Greeting message
    """
    return f"Hello, {name}!"


if __name__ == "__main__":
    print(simple_function("World"))
