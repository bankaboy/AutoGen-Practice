import asyncio
from autogen_ext.models.anthropic import AnthropicChatCompletionClient
from autogen_agentchat.agents import AssistantAgent
from autogen_agentchat.tools import AgentTool
from autogen_agentchat.ui import Console

import os
from dotenv import load_dotenv




# load the keys from the .env file
load_dotenv()

async def main():
    anthropic_client = AnthropicChatCompletionClient(
        model="claude-sonnet-4-5",
        api_key=os.environ.get("ATHROPIC_CLAUDE_KEY"),  # Optional if ANTHROPIC_API_KEY is set in environment
    )

    writer_agent = AssistantAgent(
        name = "writer_agent",
        model_client = anthropic_client,
        description = "An agent that produces code for a task",
        system_message = "You are an expert at writing code for the task that is provided to you",
        model_client_stream=True
    )
    writer_agent_tool = AgentTool(writer_agent, return_value_as_last_message = True)

    review_agent = AssistantAgent(
        name = "review_agent",
        model_client = anthropic_client,
        description = "An agent that reviews the code",
        system_message = "You are an expert at performing code reviews.",
        model_client_stream=True,
    )
    review_agent_tool = AgentTool(review_agent, return_value_as_last_message = True)


    coding_agent  = AssistantAgent(
        name = "coder",
        system_message = "You are a coding assistant. Use expert tools when needed.",
        model_client = anthropic_client,
        model_client_stream = True,
        tools = [writer_agent_tool, review_agent_tool],
        max_tool_iterations = 10
    )

    result = await coding_agent.run(task="Write python code that takes two numbers from the user and returns the sum")  # type: ignore
    print(result.messages[-1].to_model_text()) # extract and print the last message

    await anthropic_client.close()


if __name__ == "__main__":
    asyncio.run(main())