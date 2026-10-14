import asyncio
import sys
from pathlib import Path
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client


async def main() -> None:
    server_file = Path(__file__).with_name("mcp_server.py")
    server_parameters = StdioServerParameters(
        command=sys.executable,
        args=[str(server_file)],
    )

    # Start the server as a child process and communicate with it over stdio.
    async with stdio_client(server_parameters) as (read_stream, write_stream):
        async with ClientSession(read_stream, write_stream) as session:
            await session.initialize()
            result = await session.call_tool(
                "add_numbers",
                arguments={"first": 4, "second": 5},
            )

            for item in result.content:
                if hasattr(item, "text"):
                    print(item.text)


if __name__ == "__main__":
    asyncio.run(main())
