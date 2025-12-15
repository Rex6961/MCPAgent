from datetime import datetime

from mcp.server.fastmcp import FastMCP

mcp = FastMCP("TimeAndMathServer")


@mcp.tool()
def add_numbers(a: int, b: int) -> int:
    """Add two numbers.

    Args:
        a (int): First integer.
        b (int): Second integer.

    Returns:
        int: Integer.
    """
    return a + b


@mcp.tool()
def get_echo(text: str) -> str:
    """Echoes the input text back must be with a prefix.

    Args:
        text (str): The string to echo.

    Returns:
        str: The string.
    """
    return f"Echo from MCP: {text}"

@mcp.tool()
def get_current_time() -> str:
    """Get the current time

    Returns:
        str: The current time
    """
    current_time = datetime.now().strftime("%d/%m/%Y %H:%M")
    return current_time


if __name__ == "__main__":
    mcp.run()
