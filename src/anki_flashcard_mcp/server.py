import asyncio
import requests
from mcp.server.models import InitializationOptions
import mcp.types as types
from mcp.server import Server
import mcp.server.stdio

server = Server("anki-flashcard-mcp")

@server.list_tools()
async def handle_list_tools() -> list[types.Tool]:
    return [
        types.Tool(
            name="add-anki-note",
            description="Add a new flashcard to an Anki deck.",
            inputSchema={
                "type": "object",
                "properties": {
                    "deckName": {"type": "string"},
                    "front": {"type": "string"},
                    "back": {"type": "string"},
                },
                "required": ["deckName", "front", "back"],
            },
        )
    ]

@server.call_tool()
async def handle_call_tool(name: str, arguments: dict | None) -> list[types.TextContent]:
    if name != "add-anki-note":
        raise ValueError(f"Unknown tool: {name}")

    if not arguments:
        raise ValueError("Missing arguments")

    deck_name = arguments.get("deckName")
    front_content = arguments.get("front")
    back_content = arguments.get("back")

    if not all([deck_name, front_content, back_content]):
        raise ValueError("Missing 'deckName', 'front', or 'back'")

    try:
        anki_connect_url = "http://host.docker.internal:8765"
        response = requests.post(anki_connect_url, json={
            "action": "addNote",
            "version": 6,
            "params": {
                "note": {
                    "deckName": deck_name,
                    "modelName": "Basic",
                    "fields": {
                        "Front": front_content,
                        "Back": back_content,
                    },
                    "options": {"allowDuplicate": False},
                    "tags": ["mcp"],
                }
            }
        })
        response_data = response.json()
        if response_data.get("error"):
            raise Exception(response_data["error"])

        return [
            types.TextContent(
                type="text",
                text=f"✅ Added note to '{deck_name}'\nFront: {front_content}\nBack: {back_content}"
            )
        ]

    except Exception as e:
        return [
            types.TextContent(
                type="text",
                text=f"❌ Failed to add note: {e}. Make sure Anki and AnkiConnect are running."
            )
        ]

async def main():
    # Pass empty capabilities dict to avoid notification/tool errors
    capabilities = {}

    async with mcp.server.stdio.stdio_server() as (read_stream, write_stream):
        await server.run(
            read_stream,
            write_stream,
            InitializationOptions(
                server_name="anki-flashcard-mcp",
                server_version="0.1.0",
                capabilities=capabilities,
            ),
        )

if __name__ == "__main__":
    asyncio.run(main())
