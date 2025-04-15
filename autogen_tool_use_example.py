import asyncio
import os
from azure.core.credentials import AzureKeyCredential
from autogen_ext.models.azure import AzureAIChatCompletionClient
from autogen_core.models import UserMessage, ModelFamily

from typing import Dict, List, Optional   
from dotenv import load_dotenv
load_dotenv(override=True)

from autogen_core.tools import FunctionTool
from autogen_agentchat.agents import AssistantAgent
from autogen_agentchat.messages import TextMessage
from autogen_core import CancellationToken

# Step1: Create the tool function
def vacation_destinations(city: str) -> tuple[str, str]:
    """
    Checks if a specific vacation destination is available
    
    Args:
        city (str): Name of the city to check
        
    Returns:
        tuple: Contains city name and availability status ('Available' or 'Unavailable')
    """
    destinations = {
        "Barcelona": "Available",
        "Tokyo": "Unavailable",
        "Cape Town": "Available",
        "Vancouver": "Available",
        "Dubai": "Unavailable",
        "Beijing": "Available",
    }

    if city in destinations:
        return city, destinations[city]
    else:
        return city, "City not found"

# # test the tool function
# city, status = vacation_destinations("Beijing")
# print(city, status)


# Step2: Create the client and Tool
client = AzureAIChatCompletionClient(
    model="gpt-4o",
    endpoint="https://models.inference.ai.azure.com",
    credential=AzureKeyCredential(os.environ["GITHUB_TOKEN"]),
    model_info={
        "json_output": True,
        "function_calling": True,
        "vision": True,
        "structured_output": True,
        "family": ModelFamily.GPT_4O,
    },
)

# # test the client
# async def main():
#     result = await client.create([UserMessage(content="What is the capital of China?", source="user")])
#     print(result)
# if __name__ == "__main__":
#     asyncio.run(main())

# Define the tool
get_vacations = FunctionTool(
vacation_destinations, description="Search for vacation destinations and if they are available or not.")

# # test function tool
# print("Defined function tool: ", get_vacations)

# Step 3: Create and run the agent
agent = AssistantAgent(
    name="travel_assistant",
    model_client=client,
    tools=[get_vacations],
    system_message="You are a travel agent that helps users find vacation destinations.",
    reflect_on_tool_use=True,
)

# # test agent
# print("agent: ", agent)

# Step 4: Run the agent
async def assistant_run() -> None:
    response = await agent.on_messages(
        [TextMessage(content="I would like to take a trip to Beijing and Tokyo", source="user")],
        cancellation_token=CancellationToken(),
    )
    print("inner_messages: ", response.inner_messages)
    print("================================================")
    print("chat_message: ", response.chat_message)


if __name__ == "__main__":
    asyncio.run(assistant_run())



