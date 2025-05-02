"""
Vendor panel component for the WhatsApp Sender application.
"""
import tkinter as tk
from tkinter import ttk
from typing import Dict, List, Callable
from src.config.styles import AppStyles
from src.components.ui_components import apply_hover_style, create_tooltip

class VendorPanel:
    """Manages vendor selection UI components"""
    def __init__(self, parent: ttk.Frame, styles: AppStyles):
        self.parent = parent
        self.styles = styles
        self.vendor_buttons: Dict[str, ttk.Button] = {}
        
        self._create_panel()

    def _create_panel(self) -> None:
        """Create the vendor panel UI"""
        self.frame = ttk.LabelFrame(
            self.parent,
            text="Select Vendor",
            style="Settings.TLabelframe"
        )
        self.frame.pack(fill=tk.X, pady=(0, 16))
        
        self.buttons_frame = ttk.Frame(self.frame)
        self.buttons_frame.pack(fill=tk.X, pady=8)

    def update_vendors(self, vendors: List[str], callback: Callable[[str], None]) -> None:
        """Update vendor buttons based on loaded data"""
        for button in self.vendor_buttons.values():
            button.destroy()
        self.vendor_buttons.clear()
        
        for vendor in vendors:
            button = ttk.Button(
                self.buttons_frame,
                text=vendor,
                command=lambda v=vendor: callback(v)
            )
            button.pack(side=tk.LEFT, padx=5)
            self.vendor_buttons[vendor] = button
            apply_hover_style(button, self.styles.colors)
            create_tooltip(button, f"Send messages for vendor {vendor}")

    def set_buttons_state(self, state: str) -> None:
        """Enable or disable all vendor buttons"""
        for button in self.vendor_buttons.values():
            button.config(state=state)