"""
Configuration class for timing delays in the WhatsApp Sender application.
"""
import tkinter as tk
from dataclasses import dataclass
from typing import Dict

from src.config.constants import DEFAULT_DELAYS


@dataclass
class DelayConfig:
    """Configuration for timing delays"""
    load_delay: float
    msg_delay: float
    close_delay: float

    @classmethod
    def from_vars(cls, delay_vars: Dict[str, tk.StringVar]) -> 'DelayConfig':
        """Create DelayConfig from tkinter variables"""
        try:
            return cls(**{
                key: float(var.get())
                for key, var in delay_vars.items()
            })
        except ValueError:
            return cls(**{
                key: config["default"]
                for key, config in DEFAULT_DELAYS.items()
            })
