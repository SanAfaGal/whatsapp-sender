import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox, filedialog
import threading
import time
from datetime import datetime

from services.message_service import send_messages_batch
from utils.json_handler import load_messages_from_json, filter_messages_by_vendor
from utils.browser_utils import get_browser_path, BROWSER_PATHS
from components.ui_components import create_header, create_footer, apply_hover_style, create_tooltip
from config.styles import AppStyles
from config.constants import DEFAULT_DELAYS

class WhatsAppSenderApp:
    def __init__(self, root):
        self.root = root
        self.root.title("WhatsApp Message Sender")
        self.root.geometry("800x700")
        self.root.minsize(600, 600)
        
        # Initialize styles
        self.styles = AppStyles()
        self.setup_styles()
        
        # Create main container
        self.main_frame = ttk.Frame(root, padding="20")
        self.main_frame.pack(fill=tk.BOTH, expand=True)
        
        self.setup_ui()
        
        # Data storage
        self.json_data = []
        self.vendors = []
        self.vendor_buttons = {}

    def setup_styles(self):
        """Initialize and configure all styles"""
        self.style = ttk.Style()
        for style_name, config in self.styles.get_styles().items():
            self.style.configure(style_name, **config)

    def setup_ui(self):
        """Set up all UI components"""
        # Create header
        create_header(self.main_frame, "WhatsApp Message Sender", self.styles.colors)
        
        # Settings section
        self.create_settings_section()
        
        # Vendor section
        self.create_vendor_section()
        
        # Log section
        self.create_log_section()
        
        # Status bar
        self.create_status_bar()
        
        # Footer
        create_footer(self.main_frame, self.styles.colors)

    def create_settings_section(self):
        """Create the settings section of the UI"""
        self.settings_frame = ttk.LabelFrame(
            self.main_frame,
            text="Configuration",
            style="Settings.TLabelframe"
        )
        self.settings_frame.pack(fill=tk.X, pady=(0, 16))
        
        # File selection
        self.create_file_selection()
        
        # Browser selection
        self.create_browser_selection()
        
        # Delays configuration
        self.create_delays_config()

    def create_file_selection(self):
        """Create file selection controls"""
        file_frame = ttk.Frame(self.settings_frame)
        file_frame.pack(fill=tk.X, pady=8)
        
        ttk.Label(file_frame, text="JSON File:").pack(side=tk.LEFT, padx=(0, 10))
        
        self.json_path_var = tk.StringVar()
        self.json_entry = ttk.Entry(file_frame, textvariable=self.json_path_var)
        self.json_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 10))
        
        self.browse_button = ttk.Button(
            file_frame,
            text="Browse & Load",
            command=self.browse_json
        )
        self.browse_button.pack(side=tk.LEFT)
        apply_hover_style(self.browse_button, self.styles.colors)
        create_tooltip(self.browse_button, "Select and load messages from a JSON file")

    def create_browser_selection(self):
        """Create browser selection controls"""
        browser_frame = ttk.Frame(self.settings_frame)
        browser_frame.pack(fill=tk.X, pady=8)
        
        ttk.Label(browser_frame, text="Browser:").pack(side=tk.LEFT, padx=(0, 10))
        
        self.browser_var = tk.StringVar(value="default")
        for browser in ["Default", "Edge", "Brave"]:
            ttk.Radiobutton(
                browser_frame,
                text=browser,
                value=browser.lower(),
                variable=self.browser_var
            ).pack(side=tk.LEFT, padx=5)

    def create_delays_config(self):
        """Create delay configuration controls"""
        delays_frame = ttk.LabelFrame(
            self.settings_frame,
            text="Timing Settings",
            style="Settings.TLabelframe"
        )
        delays_frame.pack(fill=tk.X, pady=(16, 8))
        
        # Create spinboxes for each delay type
        self.delay_vars = {}
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

    def create_vendor_section(self):
        """Create vendor selection section"""
        self.vendor_frame = ttk.LabelFrame(
            self.main_frame,
            text="Select Vendor",
            style="Settings.TLabelframe"
        )
        self.vendor_frame.pack(fill=tk.X, pady=(0, 16))
        
        self.buttons_frame = ttk.Frame(self.vendor_frame)
        self.buttons_frame.pack(fill=tk.X, pady=8)

    def create_log_section(self):
        """Create logging section"""
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

    def create_status_bar(self):
        """Create status bar"""
        self.status_var = tk.StringVar(value="Ready")
        self.status_bar = ttk.Label(
            self.main_frame,
            textvariable=self.status_var,
            anchor=tk.W,
            foreground=self.styles.colors["light_text"]
        )
        self.status_bar.pack(fill=tk.X, pady=(0, 8))

    def browse_json(self):
        """Open file dialog to select JSON file and load it"""
        file_path = filedialog.askopenfilename(
            title="Select JSON File",
            filetypes=[("JSON files", "*.json"), ("All files", "*.*")]
        )
        if file_path:
            self.json_path_var.set(file_path)
            self.load_json()

    def load_json(self):
        """Load messages from JSON file"""
        try:
            json_path = self.json_path_var.get()
            if not json_path:
                self.log("Please select a JSON file first", "error")
                return
                
            self.json_data, self.vendors = load_messages_from_json(json_path)
            
            # Clear existing buttons
            for button in self.vendor_buttons.values():
                button.destroy()
            self.vendor_buttons = {}
            
            # Create buttons for each vendor
            for vendor in self.vendors:
                button = ttk.Button(
                    self.buttons_frame,
                    text=vendor,
                    command=lambda v=vendor: self.send_messages_for_vendor(v)
                )
                button.pack(side=tk.LEFT, padx=5)
                self.vendor_buttons[vendor] = button
                apply_hover_style(button, self.styles.colors)
                create_tooltip(button, f"Send messages for vendor {vendor}")
            
            # Update status
            count = len(self.json_data)
            vendor_count = len(self.vendors)
            self.status_var.set(f"Loaded {count} messages for {vendor_count} vendors")
            self.log(f"Successfully loaded {json_path}")
            self.log(f"Found {count} messages for vendors: {', '.join(self.vendors)}")
            
        except Exception as e:
            self.log(f"Error loading JSON: {str(e)}", "error")
            messagebox.showerror("Error", f"Failed to load JSON file: {str(e)}")
            self.status_var.set("Error loading JSON file")

    def send_messages_for_vendor(self, vendor):
        """Send messages for selected vendor in a separate thread"""
        if not self.json_data:
            self.log("No data loaded. Please load a JSON file first.", "error")
            return
            
        # Filter messages for selected vendor
        messages = filter_messages_by_vendor(self.json_data, vendor)
        if not messages:
            self.log(f"No messages found for vendor {vendor}", "error")
            return
            
        # Get delays
        try:
            delays = {
                key: float(var.get())
                for key, var in self.delay_vars.items()
            }
        except ValueError:
            self.log("Invalid delay values. Using defaults.", "error")
            delays = {
                key: config["default"]
                for key, config in DEFAULT_DELAYS.items()
            }
            for key, value in delays.items():
                self.delay_vars[key].set(str(value))
        
        # Get browser path
        browser_path = get_browser_path(vendor)
        
        # Disable buttons during sending
        for button in self.vendor_buttons.values():
            button.config(state=tk.DISABLED)
        
        # Start sending in a separate thread
        self.status_var.set(f"Sending messages for {vendor}...")
        threading.Thread(
            target=self._send_messages_thread,
            args=(messages, vendor, delays, browser_path),
            daemon=True
        ).start()

    def _send_messages_thread(self, messages, vendor, delays, browser_path):
        """Thread function to send messages"""
        try:
            total = len(messages)
            self.log(f"Starting to send {total} messages for {vendor}")
            if browser_path:
                self.log(f"Using browser: {browser_path}")
            
            results = send_messages_batch(
                messages,
                delays=delays,
                browser_path=browser_path,
                progress_callback=lambda msg, level="info": self.log(msg, level)
            )
            
            # Summary
            success_count = sum(1 for r in results if r["success"])
            fail_count = total - success_count
            
            self.log(f"Completed sending messages for {vendor}")
            self.log(f"Summary: {success_count} successful, {fail_count} failed out of {total}")
            self.status_var.set(f"Completed: {success_count} sent, {fail_count} failed")
            
        except Exception as e:
            self.log(f"Error in message sending thread: {str(e)}", "error")
            self.status_var.set("Error sending messages")
            
        finally:
            # Re-enable buttons
            def enable_buttons():
                for button in self.vendor_buttons.values():
                    button.config(state=tk.NORMAL)
            self.root.after(0, enable_buttons)

    def log(self, message, level="info"):
        """Add message to log area with timestamp"""
        timestamp = datetime.now().strftime("%H:%M:%S")
        
        # Set color based on level
        if level == "error":
            tag = "error"
            color = self.styles.colors["error"]
        elif level == "success":
            tag = "success"
            color = self.styles.colors["success"]
        else:
            tag = "info"
            color = self.styles.colors["text"]
        
        # Enable editing, add text, then disable again
        self.log_area.config(state=tk.NORMAL)
        self.log_area.insert(tk.END, f"[{timestamp}] ", "timestamp")
        self.log_area.insert(tk.END, f"{message}\n", tag)
        
        # Configure tags
        self.log_area.tag_config("timestamp", foreground=self.styles.colors["light_text"])
        self.log_area.tag_config(tag, foreground=color)
        
        # Scroll to end
        self.log_area.see(tk.END)
        self.log_area.config(state=tk.DISABLED)