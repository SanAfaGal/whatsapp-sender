"""
Log management component for the WhatsApp Sender application.
"""
import tkinter as tk
from datetime import datetime
from tkinter import scrolledtext


class LogManager:
    """Manages the application's logging functionality"""

    def __init__(self, log_area: scrolledtext.ScrolledText, colors: dict):
        self.log_area = log_area
        self.colors = colors
        self._configure_tags()

    def _configure_tags(self) -> None:
        """Configure text tags for different log levels"""
        self.log_area.tag_config("timestamp", foreground=self.colors["light_text"])
        self.log_area.tag_config("error", foreground=self.colors["error"])
        self.log_area.tag_config("success", foreground=self.colors["success"])
        self.log_area.tag_config("info", foreground=self.colors["text"])

    def log(self, message: str, level: str = "info") -> None:
        """Add a timestamped message to the log area"""
        timestamp = datetime.now().strftime("%H:%M:%S")

        self.log_area.config(state=tk.NORMAL)
        self.log_area.insert(tk.END, f"[{timestamp}] ", "timestamp")
        self.log_area.insert(tk.END, f"{message}\n", level)
        self.log_area.see(tk.END)
        self.log_area.config(state=tk.DISABLED)
