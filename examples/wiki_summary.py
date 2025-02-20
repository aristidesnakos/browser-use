from browser_use import Agent
from langchain_openai import ChatOpenAI
import asyncio
import time
import argparse
from typing import Optional, Dict, Any


async def main(url: str) -> Optional[Dict[str, str]]:
    """
    Main function to run the agent with URLs from CSV.
    
    Args:
        url: Wikipedia article URL to process
        
    Returns:
        JSON string with article name and summary or None if failed
    """
    max_retries = 3
    retry_delay = 60  # seconds
    
    for attempt in range(max_retries):
        try:
            task = (
                f"Visit this URL and provide a comprehensive summary in 7-8 "
                f"sentences: {url} in English. Return a JSON with the keys "
                f"'name' and 'summary'."
            )
            
            agent = Agent(
                task=task,
                llm=ChatOpenAI(model="gpt-4o"),
            )
            
            result = await agent.run()
            
            if result and result.final_result():
                return result.final_result()
                
        except Exception as e:
            print(f"Attempt {attempt + 1} failed: {str(e)}")
            if "Rate limit" in str(e):
                print(f"Rate limit hit. Waiting {retry_delay} seconds...")
                time.sleep(retry_delay)
                continue
            
        if attempt < max_retries - 1:
            print(f"Retrying in {retry_delay} seconds...")
            time.sleep(retry_delay)
    
    print(f"Failed to process URL after {max_retries} attempts: {url}")
    return None


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '--url',
        required=True,
        help='URL of the Wikipedia article'
    )
    args = parser.parse_args()
    result = asyncio.run(main(url=args.url))
    print(result) 
