import json
import csv
from typing import List, Dict
from pathlib import Path

def parse_wiki_results(json_str: str, output_file: str, query_type: str) -> str:
    """
    Parse Wikipedia article results from JSON to CSV.
    
    Args:
        json_str: JSON string containing Wikipedia article data
        output_file: Name of the output CSV file
    
    Returns:
        str: Path to the created CSV file
    """
    try:
        # Parse JSON string to Python object
        articles = json.loads(json_str)
        
        # Ensure output directory exists
        output_dir = Path('output')
        output_dir.mkdir(exist_ok=True)
        
        # Create full output path
        output_path = output_dir / output_file
        
        # Write to CSV
        with open(output_path, 'w', newline='', encoding='utf-8') as f:
            if query_type == "urls":
                writer = csv.DictWriter(f, fieldnames=['name', 'url'])
            else:
                writer = csv.DictWriter(f, fieldnames=['name', 'summary'])
            writer.writeheader()
            writer.writerows(articles)
            
        return str(output_path)
        
    except json.JSONDecodeError as e:
        raise ValueError(f"Invalid JSON string: {str(e)}")
    except Exception as e:
        raise Exception(f"Error writing CSV: {str(e)}")

if __name__ == "__main__":
    # Example usage
    sample_json = '''[
        {"name": "Pericles", "url": "https://en.wikipedia.org/wiki/Pericles"},
        {"name": "Plato", "url": "https://en.wikipedia.org/wiki/Plato"}
    ]'''
    output_file = parse_wiki_results(sample_json, "wiki_articles.csv", query_type)
    print(f"CSV file created at: {output_file}") 