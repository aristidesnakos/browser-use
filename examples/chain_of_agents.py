import os
import sys
import asyncio
from typing import List
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from utils.helpers import validate_topics, parse_arguments

# Third-party imports
from langchain_openai import ChatOpenAI

# Local imports

from browser_use import Agent, Controller


async def main(topics: str) -> str | None:
    """
    Create agents to search Wikipedia articles based on provided topics.
    
    Args:
        topics: Comma-separated string of topics to search for
    
    Returns:
        str: JSON string containing article names and URLs
    """
    try:
        # Validate topics
        topic_list = validate_topics(topics)
        
        # Initialize controller and model
        controller = Controller()
        model = ChatOpenAI(model='gpt-4o')
        
        # Create agents with properly formatted tasks
        agent1 = Agent(
            task=(
                'Open tabs with wikipedia articles for each of the '
                f'following topics: {", ".join(topic_list)}.'
            ),
            llm=model,
            controller=controller,
        )
        
        agent2 = Agent(
            task=(
                'Considering all open tabs give me the names and urls of the '
                'wikipedia articles in a JSON format with the keys "name" and '
                '"url". Return just the JSON string.'
            ),
            llm=model,
            controller=controller,
        )
        
        # Run agents
        await agent1.run()
        result = await agent2.run()
        
        # Simply return the result as it's already in the correct JSON format
        return result.final_result()
        
    except Exception as e:
        print(f"An error occurred: {str(e)}")
        raise
    finally:
        # Ensure browser is properly closed
        if 'controller' in locals():
            await controller.browser.close()

if __name__ == "__main__":
    args = parse_arguments()
    asyncio.run(main(topics=args.topics))
