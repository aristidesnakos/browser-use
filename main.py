from utils.helpers import validate_topics, parse_arguments
from langchain_openai import ChatOpenAI
from browser_use import Agent
import asyncio

async def main(topics: str) -> str | None:
    """Main function to run the agent."""
    
    topic_list = validate_topics(topics)
    task = (
        f"Find the urls for the following topics: {', '.join(topic_list)} "
        "on Reddit. Return me a JSON with the keys 'name' and 'url'."
    )
    
    agent = Agent(
        task=task,
        llm=ChatOpenAI(model="gpt-4o"),
    )
    result = await agent.run()
    
    if result and result.final_result():
        return result.final_result()
    
    return None

if __name__ == "__main__":
    parsed_args = parse_arguments()
    asyncio.run(main(topics=parsed_args.topics))
    