from browser_use import Agent
from langchain_openai import ChatOpenAI 
import asyncio
import csv
import argparse


async def main(csv_path: str) -> str | None:
    """Main function to run the agent with URLs from CSV."""
    
    # Read URLs from CSV
    with open(csv_path, 'r') as file:
        reader = csv.DictReader(file)
        urls = [row['url'] for row in reader]
    
    task = (
        f"Visit these URLs and provide a comprehensive summary of each "
        f"article in 7-8 sentences: {', '.join(urls)} in English. "
        f"Return me a JSON with the keys 'name' and 'summary'."
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
    parser = argparse.ArgumentParser()
    parser.add_argument('--csv', required=True, help='Path to CSV file')
    args = parser.parse_args()
    
    result = asyncio.run(main(csv_path=args.csv))
    print(result) 