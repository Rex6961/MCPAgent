import os

from mcp.server.fastmcp import FastMCP

mcp = FastMCP("FileSystemServer")

@mcp.tool()
def list_files(directory: str) -> dict:
    """Echoes directories files.

    Args:
        directory (str): The root directory.

    Returns:
        str: Directories files
    """
    return {"files": str(os.listdir(directory))}


if __name__=="__main__":
    mcp.run()
