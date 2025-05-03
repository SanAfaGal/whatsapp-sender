"""
Main application window module for the WhatsApp Sender application.
"""
import os
import threading
import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox, filedialog
from typing import List, Optional

from src.components.ui_components import create_header, create_footer
from src.config.styles import AppStyles
from src.services.json_service import load_messages_from_json, filter_messages_by_vendor
from src.services.message_service import send_messages_batch
from src.ui.components.delay_config import DelayConfig
from src.ui.components.log_manager import LogManager
from src.ui.panels.settings_panel import SettingsPanel
from src.ui.panels.vendor_panel import VendorPanel
from src.utils.browser_utils import get_browser_path
from src.utils.sound_utils import play_completion_sound
from src.utils.time_utils import estimate_total_time, format_time_estimate


class WhatsAppSenderApp:
    """Main application class for WhatsApp Message Sender"""

    def __init__(self, root: tk.Tk):
        self.root = root
        self.root.title("WhatsApp Message Sender")
        self.root.geometry("800x900")
        self.root.minsize(600, 600)

        # Set window icon
        icon_path = os.path.join(os.path.dirname(__file__), "..", "assets", "icon.ico")
        if os.path.exists(icon_path):
            self.root.iconbitmap(icon_path)

        self.styles = AppStyles()
        self.setup_styles()

        self.main_frame = ttk.Frame(root, padding="20")
        self.main_frame.pack(fill=tk.BOTH, expand=True)

        self.setup_ui()

        self.json_data: List[dict] = []
        self.vendors: List[str] = []

    def setup_styles(self) -> None:
        """Initialize and configure all styles"""
        self.style = ttk.Style()
        for style_name, config in self.styles.get_styles().items():
            self.style.configure(style_name, **config)

    def setup_ui(self) -> None:
        """Set up all UI components"""
        create_header(self.main_frame, "WhatsApp Message Sender", self.styles.colors)

        self.settings_panel = SettingsPanel(self.main_frame, self.styles)
        self.settings_panel.browse_button.config(command=self.browse_json)

        self.vendor_panel = VendorPanel(self.main_frame, self.styles)

        self.setup_log_area()
        self.setup_status_bar()

        create_footer(self.main_frame, self.styles.colors)

    def setup_log_area(self) -> None:
        """Set up logging area"""
        self.log_frame = ttk.LabelFrame(
            self.main_frame,
            text="Activity Log",
            style="Settings.TLabelframe"
        )
        self.log_frame.pack(fill=tk.BOTH, expand=True, pady=(0, 16))

        self.log_area = scrolledtext.ScrolledText(
            self.log_frame,
            height=12,
            wrap=tk.WORD,
            font=("Consolas", 10)
        )
        self.log_area.pack(fill=tk.BOTH, expand=True, pady=8)
        self.log_area.config(state=tk.DISABLED)

        self.log_manager = LogManager(self.log_area, self.styles.colors)

    def setup_status_bar(self) -> None:
        """Set up status bar"""
        self.status_var = tk.StringVar(value="Ready")
        self.status_bar = ttk.Label(
            self.main_frame,
            textvariable=self.status_var,
            anchor=tk.W,
            foreground=self.styles.colors["light_text"]
        )
        self.status_bar.pack(fill=tk.X, pady=(0, 8))

    def browse_json(self) -> None:
        """Open file dialog to select JSON file and load it"""
        file_path = filedialog.askopenfilename(
            title="Select JSON File",
            filetypes=[("JSON files", "*.json"), ("All files", "*.*")]
        )
        if file_path:
            self.settings_panel.json_path_var.set(file_path)
            self.load_json()

    def load_json(self) -> None:
        """Load messages from JSON file"""
        try:
            json_path = self.settings_panel.json_path_var.get()
            if not json_path:
                self.log_manager.log("Please select a JSON file first", "error")
                return

            self.json_data, self.vendors = load_messages_from_json(json_path)

            self.vendor_panel.update_vendors(
                self.vendors,
                self.send_messages_for_vendor
            )

            count = len(self.json_data)
            vendor_count = len(self.vendors)
            self.status_var.set(f"Loaded {count} messages for {vendor_count} vendors")
            self.log_manager.log(f"Successfully loaded {json_path}")
            self.log_manager.log(f"Found {count} messages for vendors: {', '.join(self.vendors)}")

        except Exception as e:
            self.log_manager.log(f"Error loading JSON: {str(e)}", "error")
            messagebox.showerror("Error", f"Failed to load JSON file: {str(e)}")
            self.status_var.set("Error loading JSON file")

    def send_messages_for_vendor(self, vendor: str) -> None:
        """Send messages for selected vendor in a separate thread"""
        if not self.json_data:
            self.log_manager.log("No data loaded. Please load a JSON file first.", "error")
            return

        messages = filter_messages_by_vendor(self.json_data, vendor)
        if not messages:
            self.log_manager.log(f"No messages found for vendor {vendor}", "error")
            return

        delays = DelayConfig.from_vars(self.settings_panel.delay_vars)
        browser_path = get_browser_path(vendor)

        # Calculate time estimate
        total_time = estimate_total_time(len(messages), vars(delays))
        time_estimate = format_time_estimate(total_time)

        # Show confirmation dialog with time estimate
        message = f"Estimated time to send {len(messages)} messages: {time_estimate}\n\nDo you want to proceed?"
        if not messagebox.askyesno("Confirm Send", message):
            self.log_manager.log("Operation cancelled by user")
            return

        self.vendor_panel.set_buttons_state(tk.DISABLED)
        self.status_var.set(f"Sending messages for {vendor}...")

        threading.Thread(
            target=self._send_messages_thread,
            args=(messages, vendor, delays, browser_path),
            daemon=True
        ).start()

    def _send_messages_thread(
            self,
            messages: List[dict],
            vendor: str,
            delays: DelayConfig,
            browser_path: Optional[str]
    ) -> None:
        """Thread function to send messages"""
        try:
            total = len(messages)
            self.log_manager.log(f"Starting to send {total} messages for {vendor}")
            if browser_path:
                self.log_manager.log(f"Using browser: {browser_path}")

            results = send_messages_batch(
                messages,
                vars(delays),
                browser_path=browser_path,
                progress_callback=self.log_manager.log
            )

            success_count = sum(1 for r in results if r["success"])
            fail_count = total - success_count

            self.log_manager.log(f"Completed sending messages for {vendor}")
            self.log_manager.log(f"Summary: {success_count} successful, {fail_count} failed out of {total}")
            self.status_var.set(f"Completed: {success_count} sent, {fail_count} failed")

            # Play completion sound
            play_completion_sound()

        except Exception as e:
            self.log_manager.log(f"Error in message sending thread: {str(e)}", "error")
            self.status_var.set("Error sending messages")

        finally:
            self.root.after(0, lambda: self.vendor_panel.set_buttons_state(tk.NORMAL))
