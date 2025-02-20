from typing import List
import argparse

def validate_topics(topics: str) -> List[str]:
    """Validate and split topics into a list."""
    if not topics or not isinstance(topics, str):
        raise ValueError("Topics must be a non-empty string")
    return [topic.strip() for topic in topics.split(",")]

def parse_arguments() -> argparse.Namespace:
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(
        description='Search Wikipedia articles using AI agents'
    )
    parser.add_argument(
        'topics',
        type=str,
        help='Comma-separated list of topics to search for'
    )
    return parser.parse_args()