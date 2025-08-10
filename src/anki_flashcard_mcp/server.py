from mcp.server.fastmcp import FastMCP
import requests

ANKI_CONNECT_URL = "http://host.docker.internal:8765"

def add_note_to_anki():
    payload = {
        "action": "addNote",
        "version": 5,
        "params": {
            "note": {
                "deckName": "Default",  # Change if you want another deck
                "modelName": "Basic",   # Standard front/back model
                "fields": {
                    "Front": "hello",
                    "Back": "word"
                },
                "tags": ["mcp-added"]
            }
        }
    }

    response = requests.post(ANKI_CONNECT_URL, json=payload)
    data = response.json()
    if data.get("error"):
        return f"Error adding note: {data['error']}"
    else:
        return f"Note added with ID: {data['result']}"

def main():
    mcp = FastMCP("anki-flashcard-mcp")

    @mcp.tool()
    def add_anki_note():
        """Add a note with Front='hello', Back='word' to Anki."""
        return add_note_to_anki()

    mcp.run()

if __name__ == "__main__":
    main()
