import asyncio
from buffett_indicator_agent import agent
from autogen_agentchat.messages import TextMessage
from autogen_core import CancellationToken

async def chat_with_agent():
    print("Welcome to the Buffett Indicator Chat!")
    print("Type 'exit' to quit")
    
    while True:
        user_input = input("\nYou: ")
        
        if user_input.lower() == 'exit':
            print("Goodbye!")
            break
            
        print("\nProcessing...")
        response = await agent.on_messages(
            [TextMessage(content=user_input, source="user")],
            cancellation_token=CancellationToken(),
        )
        print(f"\nThinking...: {response.inner_message}")
        print(f"\nBuffett Indicator Agent: {response.chat_message.content}")

if __name__ == "__main__":
    asyncio.run(chat_with_agent())


# example query:
# What is the current Buffett Indicator for the U.S. market? 