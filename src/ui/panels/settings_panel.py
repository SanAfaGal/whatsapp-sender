"""
Settings panel component for the WhatsApp Sender application.
"""
import tkinter as tk
from tkinter import ttk, messagebox
from typing import Dict

from src.components.ui_components import apply_hover_style, create_tooltip
from src.config.constants import DEFAULT_DELAYS
from src.config.styles import AppStyles
from src.utils.browser_utils import browser_manager


class SettingsPanel:
    """Manages application settings UI components"""

    def __init__(self, parent: ttk.Frame, styles: AppStyles):
        self.parent = parent
        self.styles = styles
        self.delay_vars: Dict[str, tk.StringVar] = {}
        self.json_path_var = tk.StringVar()
        self.browser_var = tk.StringVar(value="default")

        self._create_panel()

    def _create_panel(self) -> None:
        """Create the settings panel UI"""
        self.frame = ttk.LabelFrame(
            self.parent,
            text="Configuration",
            style="Settings.TLabelframe"
        )
        self.frame.pack(fill=tk.X, pady=(0, 16))

        self._create_file_selection()
        self._create_browser_selection()
        self._create_delays_config()

    def _create_file_selection(self) -> None:
        """Create file selection controls"""
        file_frame = ttk.Frame(self.frame)
        file_frame.pack(fill=tk.X, pady=8)

        ttk.Label(file_frame, text="JSON File:").pack(side=tk.LEFT, padx=(0, 10))

        self.json_entry = ttk.Entry(file_frame, textvariable=self.json_path_var)
        self.json_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 10))

        self.browse_button = ttk.Button(file_frame, text="Browse & Load")
        self.browse_button.pack(side=tk.LEFT)
        apply_hover_style(self.browse_button, self.styles.colors)
        create_tooltip(self.browse_button, "Select and load messages from a JSON file")

    def _create_browser_selection(self) -> None:
        """Create browser selection dropdown"""
        browser_frame = ttk.Frame(self.frame)
        browser_frame.pack(fill=tk.X, pady=8)

        ttk.Label(browser_frame, text="Browser:").pack(side=tk.LEFT, padx=(0, 10))

        # Get available browsers from manager
        browsers = browser_manager.get_available_browsers()
        browser_names = [b["name"] for b in browsers]
        browser_ids = [b["id"] for b in browsers]

        self.browser_combobox = ttk.Combobox(
            browser_frame,
            textvariable=self.browser_var,
            values=browser_names,
            state="readonly"
        )
        self.browser_combobox.pack(side=tk.LEFT, fill=tk.X, expand=True)

        # Set default browser
        self.browser_combobox.set(browser_names[0])

        # Create mapping for name to id
        self.browser_name_to_id = dict(zip(browser_names, browser_ids))

        def on_browser_select(event):
            browser_name = self.browser_combobox.get()
            browser_id = self.browser_name_to_id[browser_name]
            if browser_id != "default" and not browser_manager.validate_browser(browser_id):
                messagebox.showwarning(
                    "Browser Not Found",
                    f"The selected browser was not found at the expected location.\n"
                    f"The system will use the default browser instead."
                )

        self.browser_combobox.bind('<<ComboboxSelected>>', on_browser_select)
        create_tooltip(self.browser_combobox, "Select which browser to use for sending messages")

    def _create_delays_config(self) -> None:
        """Create delay configuration controls"""
        delays_frame = ttk.LabelFrame(
            self.frame,
            text="Timing Settings",
            style="Settings.TLabelframe"
        )
        delays_frame.pack(fill=tk.X, pady=(16, 8))

        for delay_type, config in DEFAULT_DELAYS.items():
            frame = ttk.Frame(delays_frame)
            frame.pack(fill=tk.X, pady=8)

            ttk.Label(frame, text=config["label"]).pack(side=tk.LEFT, padx=(0, 10))

            var = tk.StringVar(value=str(config["default"]))
            self.delay_vars[delay_type] = var

            spinbox = ttk.Spinbox(
                frame,
                from_=config["min"],
                to=config["max"],
                width=5,
                textvariable=var
            )
            spinbox.pack(side=tk.LEFT)
            create_tooltip(spinbox, config["tooltip"])

    def get_selected_browser_id(self) -> str:
        """Get the ID of the currently selected browser"""
        browser_name = self.browser_combobox.get()
        return self.browser_name_to_id.get(browser_name, "default")
