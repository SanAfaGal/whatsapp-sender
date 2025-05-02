"""Time estimation utilities for WhatsApp Sender"""
from typing import Dict


def estimate_total_time(message_count: int, delays: Dict[str, float]) -> float:
    """
    Calculate estimated total time for sending messages

    Args:
        message_count (int): Number of messages to send
        delays (dict): Dictionary containing delay settings

    Returns:
        float: Estimated total time in seconds
    """
    # Time per message = load time + send delay + close delay
    time_per_message = (
            delays["load_delay"] +
            delays["close_delay"]
    )

    # Add delay between messages for all except last message
    total_time = (time_per_message * message_count) + (
            delays["msg_delay"] * (message_count - 1)
    ) if message_count > 1 else time_per_message

    return total_time


def format_time_estimate(seconds: float) -> str:
    """
    Format time estimate in minutes and seconds

    Args:
        seconds (float): Time in seconds

    Returns:
        str: Formatted time string (e.g., "5 minutes 30 seconds")
    """
    minutes = int(seconds // 60)
    remaining_seconds = int(seconds % 60)

    if minutes > 0:
        return f"{minutes} minute{'s' if minutes != 1 else ''} {remaining_seconds} second{'s' if remaining_seconds != 1 else ''}"
    return f"{remaining_seconds} second{'s' if remaining_seconds != 1 else ''}"
