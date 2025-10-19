# First run `npm install -g @playwright/mcp@latest` to install the MCP server.
import asyncio
from autogen_agentchat.agents import AssistantAgent
from autogen_agentchat.ui import Console
from autogen_ext.models.anthropic import AnthropicChatCompletionClient
from autogen_ext.tools.mcp import McpWorkbench, StdioServerParams
import os
from dotenv import load_dotenv




# load the keys from the .env file
load_dotenv()

async def main() -> None:

    anthropic_client = AnthropicChatCompletionClient(
        model="claude-sonnet-4-5",
        api_key=os.environ.get("ATHROPIC_CLAUDE_KEY"),  # Optional if ANTHROPIC_API_KEY is set in environment
    )

    server_params = StdioServerParams(
        command="npx",
        args=[
            "@playwright/mcp@latest",
            "--headless",
        ],
    )

    async with McpWorkbench(server_params) as mcp:

        agent = AssistantAgent(
            "web_browsing_assistant",
            model_client=anthropic_client,
            workbench=mcp, # For multiple MCP servers, put them in a list.
            model_client_stream=True,
            max_tool_iterations=10,
        )
        
        await Console(agent.run_stream(task="Find out how many contributors for the microsoft/autogen repository"))


asyncio.run(main())