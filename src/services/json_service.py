"""
JSON handling service for the WhatsApp Sender application.
"""
import json
import os
from typing import List, Tuple, Dict


def load_messages_from_json(file_path: str) -> Tuple[List[Dict], List[str]]:
    """
    Load messages from a JSON file
    
    Args:
        file_path (str): Path to the JSON file
        
    Returns:
        tuple: (list of message objects, list of unique vendors)
    """
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"JSON file not found: {file_path}")

    with open(file_path, 'r', encoding='utf-8') as file:
        data = json.load(file)

    # Validate data structure
    if not isinstance(data, list):
        raise ValueError("JSON must contain a list of message objects")

    # Validate each message object
    for i, item in enumerate(data):
        if not isinstance(item, dict):
            raise ValueError(f"Item at index {i} is not a valid message object")

        # Check required fields
        required_fields = ["VENDEDOR", "TELEFONO", "MENSAJE"]
        for field in required_fields:
            if field not in item:
                raise ValueError(f"Item at index {i} is missing required field: {field}")

        # Ensure phone numbers are strings
        if not isinstance(item["TELEFONO"], str):
            item["TELEFONO"] = str(item["TELEFONO"])

    # Extract unique vendors
    vendors = sorted(list(set(item["VENDEDOR"] for item in data)))

    return data, vendors


def filter_messages_by_vendor(messages: List[Dict], vendor: str) -> List[Dict]:
    """
    Filter messages for a specific vendor
    
    Args:
        messages (list): List of message objects
        vendor (str): Vendor identifier
        
    Returns:
        list: Filtered messages for the specified vendor
    """
    return [msg for msg in messages if msg["VENDEDOR"] == vendor]
