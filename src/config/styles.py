"""Application styles configuration"""

class AppStyles:
    def __init__(self):
        self.colors = {
            "primary": "#25D366",  # WhatsApp green
            "primary_dark": "#128C7E",
            "success": "#2ecc71",
            "error": "#e74c3c",
            "background": "#f5f5f5",
            "text": "#2c3e50",
            "light_text": "#7f8c8d",
            "border": "#dcdde1"
        }

    def get_styles(self):
        """Return all application styles"""
        return {
            "TFrame": {
                "background": self.colors["background"]
            },
            "TButton": {
                "font": ("Helvetica", 11),
                "padding": 5
            },
            "TLabel": {
                "background": self.colors["background"],
                "foreground": self.colors["text"],
                "font": ("Helvetica", 11)
            },
            "Header.TLabel": {
                "font": ("Helvetica", 20, "bold"),
                "foreground": self.colors["primary_dark"]
            },
            "Settings.TLabelframe": {
                "background": self.colors["background"],
                "padding": 10
            },
            "Settings.TLabelframe.Label": {
                "font": ("Helvetica", 11, "bold"),
                "background": self.colors["background"],
                "foreground": self.colors["primary_dark"]
            }
        }