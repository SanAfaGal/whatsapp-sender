import json
import os
from dataclasses import dataclass
from typing import Optional, Dict, List, Any


@dataclass
class Browser:
    """Browser configuration class"""
    name: str
    id: str
    executable: Optional[str] = None
    args: List[str] = None
    icon: Optional[str] = None
    description: Optional[str] = None


class BrowserManager:
    """Manages browser configurations"""

    def __init__(self):
        self.browsers: Dict[str, Browser] = {}
        self.load_config()

    def load_config(self) -> None:
        """Load browser configurations from JSON file"""
        # Use os.path.dirname to get the directory of the current script
        script_dir = os.path.dirname(os.path.abspath(__file__))
        # Construct the path to browsers.json relative to the script directory
        config_path = os.path.join(script_dir, "..", "config", "browsers.json")
        try:
            with open(config_path, 'r', encoding='utf-8') as f:
                config = json.load(f)

            self.browsers.clear()
            for browser_data in config.get("browsers", []):
                browser = Browser(
                    name=browser_data["name"],
                    id=browser_data["id"],
                    executable=browser_data.get("executable"),
                    args=browser_data.get("args", []),
                    icon=browser_data.get("icon"),
                    description=browser_data.get("description")
                )
                self.browsers[browser.id] = browser

        except Exception as e:
            print(f"Error loading browser config: {e}")
            # Load fallback default browser
            self.browsers["default"] = Browser(
                name="Default Browser",
                id="default",
                description="System default web browser"
            )

    def get_browser_path(self, browser_id: str) -> Optional[str]:
        """Get the executable path for the specified browser"""
        browser = self.browsers.get(browser_id.lower())
        if not browser or browser.id == "default":
            return None

        if browser.executable and os.path.exists(browser.executable):
            return browser.executable
        return None

    def get_browser_args(self, browser_id: str) -> List[str]:
        """Get command line arguments for the specified browser"""
        browser = self.browsers.get(browser_id.lower())
        return browser.args if browser and browser.args else []

    def get_available_browsers(self) -> List[Dict[str, Any]]:
        """Get list of available browsers with their details"""
        return [
            {
                "name": browser.name,
                "id": browser.id,
                "installed": bool(self.get_browser_path(browser.id)) if browser.id != "default" else True,
                "icon": browser.icon,
                "description": browser.description
            }
            for browser in self.browsers.values()
        ]

    def validate_browser(self, browser_id: str) -> bool:
        """Validate if the specified browser is available"""
        if browser_id.lower() == "default":
            return True
        return bool(self.get_browser_path(browser_id))


# Global instance
browser_manager = BrowserManager()
