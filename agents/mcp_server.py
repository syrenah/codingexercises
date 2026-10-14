from mcp.server.fastmcp import FastMCP

server = FastMCP("Simple utilities")


@server.tool()
def add_numbers(first: int, second: int) -> int:
    """Add two whole numbers and return the result."""
    return first + second


if __name__ == "__main__":
    server.run(transport="stdio")
