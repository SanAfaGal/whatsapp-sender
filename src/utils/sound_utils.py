"""Sound notification utilities for WhatsApp Sender"""

import winsound


def play_completion_sound() -> None:
    """
    Emits a simple sound beep to notify completion (Windows only).
    """
    try:
        winsound.MessageBeep()
    except RuntimeError:
        print("⚠️ Unable to play sound. This feature is only supported on Windows.")
