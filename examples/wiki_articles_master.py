import sys
import json
import os
import argparse
import asyncio
from datetime import datetime
from typing import List

from parse_wiki_to_csv import parse_wiki_results
from chain_of_agents import main as agent_main
from wiki_summary import main as wiki_summary_main


def get_urls_from_csv(csv_path: str) -> List[str]:
    """
    Read URLs from a CSV file in the output directory.
    
    Args:
        csv_path: Path to the CSV file
        
    Returns:
        List of URLs from the CSV file
    """
    import csv
    urls = []
    with open(csv_path, 'r', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        for row in reader:
            if 'url' in row:
                urls.append(row['url'])
    return urls


async def process_wiki_articles(topics: str, query_type: str) -> None:
    """
    Process Wikipedia articles for given topics and save to CSV.
    
    Args:
        topics: Comma-separated string of topics
        query_type: Type of query ('urls' or 'summary')
    """
    try:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        
        if query_type == "urls":
            output_file = f"wiki_articles_{timestamp}.csv"
            json_result = await agent_main(topics)
            
            # Ensure we have a valid JSON string
            if not isinstance(json_result, str):
                json_result = json.dumps(json_result)
                
            # Parse results to CSV
            csv_path = parse_wiki_results(json_result, output_file, query_type)
            print(f"Successfully created CSV file at: {csv_path}")
            
        elif query_type == "summary":
            output_dir = "output"
            csv_files = [
                f for f in os.listdir(output_dir) 
                if f.endswith('.csv')
            ]
            
            if not csv_files:
                print("No CSV files found in output directory")
                return
                
            # Process the most recent CSV file
            latest_csv = sorted(csv_files)[-1]
            csv_path = os.path.join(output_dir, latest_csv)
            urls = get_urls_from_csv(csv_path)
            
            for url in urls:
                json_result = await wiki_summary_main(url)
                if json_result:  # Only process if we got a valid result
                    output_file = f"wiki_summary_{timestamp}.csv"
                    csv_path = parse_wiki_results(
                        json.dumps(json_result), 
                        output_file, 
                        query_type
                    )
                    print(f"Created summary CSV file at: {csv_path}")
                
    except Exception as e:
        print(f"Error processing Wikipedia articles: {str(e)}")
        sys.exit(1)


def main():
    """Main entry point with argument parsing."""
    parser = argparse.ArgumentParser(
        description='Search Wikipedia articles and save results to CSV'
    )
    parser.add_argument(
        'topics',
        type=str,
        help='Comma-separated list of topics to search for'
    )
    parser.add_argument(
        'query_type',
        type=str,
        choices=['urls', 'summary'],
        help='Type of query to perform (urls or summary)'
    )
    
    args = parser.parse_args()
    
    # Run the async process
    asyncio.run(process_wiki_articles(args.topics, args.query_type))


if __name__ == "__main__":
    main() 