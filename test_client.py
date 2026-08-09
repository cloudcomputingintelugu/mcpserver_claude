import asyncio
from fastmcp import Client


async def main():

    client = Client("https://d328sl4s1apjvq.cloudfront.net/mcp")

    async with client:

        tools = await client.list_tools()

        print("Available tools:")
        for tool in tools:
            print(f"- {tool.name}")

        print("\nCalling get_leave_balance...")

        result = await client.call_tool(
            "get_leave_balance",
            {
                "employee_id": "E001"
            }
        )

        print(result)


asyncio.run(main())