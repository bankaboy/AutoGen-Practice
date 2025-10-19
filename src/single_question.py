import asyncio
from autogen_ext.models.anthropic import AnthropicChatCompletionClient
from autogen_core.models import UserMessage

import os
from dotenv import load_dotenv

# load the keys from the .env file
load_dotenv()



async def main():
    anthropic_client = AnthropicChatCompletionClient(
        model="claude-3-5-haiku-20241022",
        api_key=os.environ.get("ATHROPIC_CLAUDE_KEY"),  # Optional if ANTHROPIC_API_KEY is set in environment
    )

    result = await anthropic_client.create([UserMessage(content="What is the capital of France?", source="user")])  # type: ignore
    print(result)


if __name__ == "__main__":
    asyncio.run(main())