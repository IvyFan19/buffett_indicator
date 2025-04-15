import asyncio
import os
from azure.core.credentials import AzureKeyCredential
from autogen_ext.models.azure import AzureAIChatCompletionClient
from autogen_core.models import UserMessage, ModelFamily

from typing import Dict, List, Optional   
from dotenv import load_dotenv

from autogen_core.tools import FunctionTool
from autogen_agentchat.agents import AssistantAgent
from autogen_agentchat.messages import TextMessage
from autogen_core import CancellationToken

# Load environment variables
load_dotenv(override=True)

# Step 1: Create the tool functions
def get_us_gdp() -> float:
    """
    Returns the current U.S. GDP value in trillions of dollars
    
    Returns:
        float: U.S. GDP value
    """
    return 29.7

def get_total_market_cap() -> float:
    """
    Returns the current total U.S. stock market capitalization in trillions of dollars
    
    Returns:
        float: Total market capitalization value
    """
    return 57.05

def calculate_buffett_indicator() -> Dict[str, float]:
    """
    Calculates the Buffett Indicator (total market cap to GDP ratio)
    and provides an interpretation
    
    Returns:
        Dict: Contains raw values and the calculated indicator
    """
    gdp = get_us_gdp()
    market_cap = get_total_market_cap()
    indicator = market_cap / gdp * 100  # Convert to percentage
    
    result = {
        "gdp_trillion": gdp,
        "market_cap_trillion": market_cap,
        "buffett_indicator_percentage": indicator
    }
    
    return result

# Step 2: Create the client and Tools
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

# Define the tools
gdp_tool = FunctionTool(
    get_us_gdp, description="Get the current U.S. GDP value in trillions of dollars.")

market_cap_tool = FunctionTool(
    get_total_market_cap, description="Get the current total U.S. stock market capitalization in trillions of dollars.")

buffett_indicator_tool = FunctionTool(
    calculate_buffett_indicator, description="Calculate the Buffett Indicator (market cap to GDP ratio) and provide the raw values along with the calculated percentage.")

###############################################################################
#                            STEP 3: CREATE AGENT 
###############################################################################
#
# These "agent functions" are how each assistant actually calls the above tools.
# The difference is that each AssistantAgent below will have 'tools=[...]'
# pointing to these Python functions. Then the agent can call them
# (directly or via the round-robin workflow).
#
###############################################################################
agent = AssistantAgent(
    name="buffett_indicator_assistant",
    model_client=client,
    tools=[gdp_tool, market_cap_tool, buffett_indicator_tool],
    system_message="""You are a financial analysis assistant that helps users understand the Buffett Indicator.
                    The Buffett Indicator is the ratio of total market capitalization to GDP, expressed as a percentage.
                    Interpretation guidelines:
                    - Below 75%: Undervalued market
                    - 75-90%: Fairly valued market
                    - 90-115%: Moderately overvalued market
                    - Above 115%: Significantly overvalued market
                    Use the available tools to provide current data and interpretations when asked.""",
    reflect_on_tool_use=True,
)

# Step 4: Run the agent
async def assistant_run() -> None:
    response = await agent.on_messages(
        [TextMessage(content="What is the current Buffett Indicator for the U.S. market? What does it tell us about market valuation?", source="user")],
        cancellation_token=CancellationToken(),
    )
    print("inner_messages: ", response.inner_messages)
    print("================================================")
    print("chat_message: ", response.chat_message)


if __name__ == "__main__":
    asyncio.run(assistant_run()) 