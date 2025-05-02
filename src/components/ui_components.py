import tkinter as tk
from tkinter import ttk

def create_header(parent, title, colors):
    """Create a header with title and decoration"""
    header_frame = ttk.Frame(parent)
    header_frame.pack(fill=tk.X, pady=(0, 16))
    
    # Create a decorative line above the title
    canvas = tk.Canvas(header_frame, height=4, bg=colors["primary"], highlightthickness=0)
    canvas.pack(fill=tk.X, pady=(0, 10))
    
    # Title
    title_label = ttk.Label(header_frame, text=title, style="Header.TLabel")
    title_label.pack(anchor=tk.W)
    
    # Subtitle
    subtitle = "Send WhatsApp messages automatically from JSON data"
    subtitle_label = ttk.Label(header_frame, text=subtitle, foreground=colors["light_text"])
    subtitle_label.pack(anchor=tk.W)
    
    return header_frame

def create_footer(parent, colors):
    """Create a footer with status info"""
    footer_frame = ttk.Frame(parent)
    footer_frame.pack(fill=tk.X, pady=(16, 0))
    
    # Create a decorative line above the footer
    canvas = tk.Canvas(footer_frame, height=1, bg=colors["light_text"], highlightthickness=0)
    canvas.pack(fill=tk.X, pady=(0, 8))
    
    # Footer text
    footer_text = "© 2023 WhatsApp Sender | Built with Python & Tkinter"
    footer_label = ttk.Label(
        footer_frame,
        text=footer_text,
        foreground=colors["light_text"],
        font=("Helvetica", 9)
    )
    footer_label.pack(side=tk.RIGHT)
    
    return footer_frame

def apply_hover_style(button, colors):
    """Apply hover effect to buttons"""
    def on_enter(e):
        button['style'] = 'Hover.TButton'
    
    def on_leave(e):
        button['style'] = 'TButton'
    
    # Create hover style
    style = ttk.Style()
    style.configure('Hover.TButton', background=colors["primary_dark"])
    
    # Bind events
    button.bind("<Enter>", on_enter)
    button.bind("<Leave>", on_leave)

def create_tooltip(widget, text):
    """Create a tooltip for a widget"""
    tooltip = tk.Label(
        widget.winfo_toplevel(),
        text=text,
        background="#ffffe0",
        relief="solid",
        borderwidth=1
    )
    tooltip.configure(padx=5, pady=2)
    
    def enter(event):
        x = y = 0
        x, y, _, _ = widget.bbox("insert")
        x += widget.winfo_rootx() + 25
        y += widget.winfo_rooty() + 20
        tooltip.lift()
        tooltip.place(x=x, y=y)
        
    def leave(event):
        tooltip.place_forget()
        
    widget.bind('<Enter>', enter)
    widget.bind('<Leave>', leave)