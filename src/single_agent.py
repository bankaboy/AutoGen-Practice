import asyncio
from autogen_ext.models.anthropic import AnthropicChatCompletionClient
from autogen_agentchat.agents import AssistantAgent

import os
from dotenv import load_dotenv




# load the keys from the .env file
load_dotenv()

async def main():
    anthropic_client = AnthropicChatCompletionClient(
        model="claude-3-5-haiku-20241022",
        api_key=os.environ.get("ATHROPIC_CLAUDE_KEY"),  # Optional if ANTHROPIC_API_KEY is set in environment
    )

    agent = AssistantAgent(
        name = "programming_langs_expert",
        model_client = anthropic_client,
        description = "An agent that answers questions about different programmning languages",
        system_message = "You are an expert on different programming languages, their strengths and weakness and where they are best used."
    )

    result = await agent.run(task="What is the best programming language for web development and why?")  # type: ignore
    print(result.messages[-1].to_text()) # extract and print the last message

    await anthropic_client.close()


if __name__ == "__main__":
    asyncio.run(main())