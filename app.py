from autogen_agentchat.agents import AssistantAgent
from autogen_agentchat.conditions import MaxMessageTermination, TextMentionTermination
from autogen_agentchat.teams import RoundRobinGroupChat
from autogen_agentchat.ui import Console
from autogen_ext.models.openai import AzureOpenAIChatCompletionClient
from azure.identity import DefaultAzureCredential
from azure.ai.projects import AIProjectClient
# from azure.ai.projects.models import BingGroundingTool
import asyncio
from dotenv import load_dotenv
import os

load_dotenv(override=True)

# Initialize environment variables
API_KEY = os.getenv("api_key")
PROJECT_CONNECTION_STRING = os.getenv("PROJECT_CONNECTION_STRING")
MODEL_DEPLOYMENT_NAME = os.getenv("MODEL_DEPLOYMENT_NAME")
MODEL_API_VERSION = os.getenv("MODEL_API_VERSION")
AZURE_ENDPOINT = os.getenv("AZURE_ENDPOINT")
# BING_CONNECTION_NAME = os.getenv("BING_CONNECTION_NAME")

print("API_KEY: ", API_KEY)
print("PROJECT_CONNECTION_STRING: ", PROJECT_CONNECTION_STRING)
print("MODEL_DEPLOYMENT_NAME: ", MODEL_DEPLOYMENT_NAME)
print("MODEL_API_VERSION: ", MODEL_API_VERSION)
print("AZURE_ENDPOINT: ", AZURE_ENDPOINT)
# print("BING_CONNECTION_NAME: ", BING_CONNECTION_NAME)


###############################################################################
#                              Azure OpenAI Client
###############################################################################
az_model_client = AzureOpenAIChatCompletionClient(
    azure_deployment=MODEL_DEPLOYMENT_NAME,
    model=MODEL_DEPLOYMENT_NAME,
    api_version=MODEL_API_VERSION,
    azure_endpoint=AZURE_ENDPOINT,
    api_key=API_KEY
)
print("az_model_client: ", az_model_client)

###############################################################################
#                              AI Project Client
###############################################################################
project_client = AIProjectClient.from_connection_string(
    credential=DefaultAzureCredential(),
    conn_str=PROJECT_CONNECTION_STRING,
)
print("project_client: ", project_client)

# # Retrieve the Bing connection
# bing_connection = project_client.connections.get(connection_name=BING_CONNECTION_NAME)
# conn_id = bing_connection.id

###############################################################################
#                                TOOLS
###############################################################################


###############################################################################
#                              AGENT FUNCTIONS
###############################################################################
#
# These "agent functions" are how each assistant actually calls the above tools.
# The difference is that each AssistantAgent below will have 'tools=[...]'
# pointing to these Python functions. Then the agent can call them
# (directly or via the round-robin workflow).
#
###############################################################################