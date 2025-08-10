# anki-flashcard-mcp MCP server

In this project we will be creating a custom dockerised mcp-server using the mcp python library and utilising through the claude app. Although you can easily use this mcp-server using other desired LLMs.

I started the mcp server by following this boilerplate guide to building and mcp server https://github.com/modelcontextprotocol/create-python-server/tree/main

I also was guided from to dockerise the mcp-server:
https://github.com/RGGH/python360



Running the commands

Using uvx (recommended)
uvx create-mcp-server
cd my-server
uv sync --dev --all-extras
uv run my-server

Then after you follow that guide create a dockerfile
then build the image using:
docker build -t anki-flashcard-mcp . 


To test the docker container on the mcp inspector do:
npx @modelcontextprotocol/inspector docker run -i --rm --init -e DOCKER_CONTAINER=true anki-flashcard-mcp

You can then test the prompts and tools to see if they return the desired output and the container runs with no errors. If errors persist rexamine the dockerfile and make changes accordingly.

When using it with the claude app, go to the settings then go to developer. It should say Local MCP servers.

Make sure claude desktop has access to docker. You can run the command:
launchctl setenv PATH "$PATH"

Click edit config and open the claude_desktop_config.json. Then edit the json:
{
  "command": "docker",
  "args": [
    "run", "-i", "--rm", "--init",
    "-e", "DOCKER_CONTAINER=true",
    "anki-flashcard-mcp"
  ]
}

If this does not work Use a wrapper shell script (workaround)
Instead of setting "command": "docker" in Claude, set:
{
  "mcpServers": {
    "anki-flashcard-mcp": {
      "command": "/Users/cademaxwell/.scripts/run-anki-docker.sh"
    }
  }
}

Create /Users/cademaxwell/.scripts/run-anki-docker.sh:
#!/bin/bash
exec /usr/local/bin/docker run -i --rm --init -e DOCKER_CONTAINER=true anki-flashcard-mcp

Make it executable:
chmod +x ~/.scripts/run-anki-docker.sh
Replace /usr/local/bin/docker with the result of running which docker.

This script is now a stable entry point that Claude can use, even if it doesn’t inherit your shell environment.

Your dockerised mcp-server should now be usuable by claude. Each time you open claude desktop a docker container for anki_flashcard_mcp image will be started.

Now we need to sync it to anki. AnkiConnect Prerequisites
This code relies on the AnkiConnect add-on being installed and running within your Anki desktop application. You can install it by going to Tools > Add-ons > Get Add-ons... in Anki and entering the code 2055492159. Anki must be open for the server to work.