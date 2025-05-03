"""Browser utility functions for WhatsApp Sender"""
import json
import os
import sys
import winreg
from dataclasses import dataclass
from typing import Optional, Dict, List, Any, Tuple


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
        self.config_paths: List[str] = self._get_config_paths()
        self.load_config()

    def _get_config_paths(self) -> List[str]:
        """Get possible config file locations"""
        paths = []

        # PyInstaller bundled path
        if getattr(sys, 'frozen', False):
            bundle_dir = sys._MEIPASS
            paths.append(os.path.join(bundle_dir, "config", "browsers.json"))

        # Development path
        current_dir = os.path.dirname(os.path.abspath(__file__))
        paths.append(os.path.join(current_dir, "..", "config", "browsers.json"))

        # User config directory
        user_config_dir = os.path.join(os.getenv('APPDATA', ''), 'WhatsAppSender')
        if os.path.exists(user_config_dir):
            paths.append(os.path.join(user_config_dir, "browsers.json"))

        return paths

    def _validate_browser_config(self, config: Any) -> bool:
        """Validate browser configuration structure"""
        if not isinstance(config, dict):
            return False

        if "browsers" not in config or not isinstance(config["browsers"], list):
            return False

        for browser in config["browsers"]:
            if not isinstance(browser, dict):
                return False
            if "name" not in browser or "id" not in browser:
                return False

        return True

    def load_config(self) -> Tuple[bool, str]:
        """Load browser configurations from JSON file"""
        for config_path in self.config_paths:
            try:
                if not os.path.exists(config_path):
                    continue

                with open(config_path, 'r', encoding='utf-8') as f:
                    config = json.load(f)

                if not self._validate_browser_config(config):
                    continue

                self.browsers.clear()
                loaded_browsers = []

                for browser_data in config["browsers"]:
                    executable = self._resolve_browser_path(browser_data)
                    browser = Browser(
                        name=browser_data["name"],
                        id=browser_data["id"],
                        executable=executable,
                        args=browser_data.get("args", []),
                        icon=self._resolve_icon_path(browser_data.get("icon")),
                        description=browser_data.get("description")
                    )
                    self.browsers[browser.id] = browser
                    if executable or browser.id == "default":
                        loaded_browsers.append(browser.name)

                return True, f"Successfully loaded {len(loaded_browsers)} browsers: {', '.join(loaded_browsers)}"

            except json.JSONDecodeError:
                continue
            except Exception as e:
                continue

        # Fallback to default browser if no config could be loaded
        self.browsers["default"] = Browser(
            name="Default Browser",
            id="default",
            description="System default web browser"
        )
        return False, "Failed to load browser configuration. Using default browser only."

    def _resolve_browser_path(self, browser_data: dict) -> Optional[str]:
        """Resolve browser executable path using multiple methods"""
        if not browser_data.get("executable"):
            return None

        # Try direct path first
        direct_path = browser_data["executable"]
        if os.path.exists(direct_path):
            return direct_path

        # Try Windows registry for common browsers
        try:
            if browser_data["id"] in ["chrome", "edge", "firefox", "opera"]:
                registry_path = self._get_browser_registry_path(browser_data["id"])
                if registry_path:
                    return registry_path
        except Exception:
            pass

        # Try common installation paths
        common_paths = self._get_common_browser_paths(browser_data["id"])
        for path in common_paths:
            if os.path.exists(path):
                return path

        return None

    def _get_browser_registry_path(self, browser_id: str) -> Optional[str]:
        """Get browser path from Windows registry"""
        registry_paths = {
            "chrome": (winreg.HKEY_LOCAL_MACHINE, r"SOFTWARE\Microsoft\Windows\CurrentVersion\App Paths\chrome.exe"),
            "edge": (winreg.HKEY_LOCAL_MACHINE, r"SOFTWARE\Microsoft\Windows\CurrentVersion\App Paths\msedge.exe"),
            "firefox": (winreg.HKEY_LOCAL_MACHINE, r"SOFTWARE\Microsoft\Windows\CurrentVersion\App Paths\firefox.exe"),
            "opera": (winreg.HKEY_LOCAL_MACHINE, r"SOFTWARE\Microsoft\Windows\CurrentVersion\App Paths\opera.exe")
        }

        if browser_id not in registry_paths:
            return None

        try:
            hkey, subkey = registry_paths[browser_id]
            with winreg.OpenKey(hkey, subkey, 0, winreg.KEY_READ) as key:
                path, _ = winreg.QueryValueEx(key, "")
                if os.path.exists(path):
                    return path
        except Exception:
            return None

        return None

    def _get_common_browser_paths(self, browser_id: str) -> List[str]:
        """Get list of common installation paths for browsers"""
        program_files = os.environ.get("ProgramFiles", "C:\\Program Files")
        program_files_x86 = os.environ.get("ProgramFiles(x86)", "C:\\Program Files (x86)")

        paths = {
            "chrome": [
                os.path.join(program_files, "Google", "Chrome", "Application", "chrome.exe"),
                os.path.join(program_files_x86, "Google", "Chrome", "Application", "chrome.exe")
            ],
            "edge": [
                os.path.join(program_files, "Microsoft", "Edge", "Application", "msedge.exe"),
                os.path.join(program_files_x86, "Microsoft", "Edge", "Application", "msedge.exe")
            ],
            "firefox": [
                os.path.join(program_files, "Mozilla Firefox", "firefox.exe"),
                os.path.join(program_files_x86, "Mozilla Firefox", "firefox.exe")
            ],
            "opera": [
                os.path.join(program_files, "Opera", "launcher.exe"),
                os.path.join(program_files_x86, "Opera", "launcher.exe")
            ],
            "brave": [
                os.path.join(program_files, "BraveSoftware", "Brave-Browser", "Application", "brave.exe"),
                os.path.join(program_files_x86, "BraveSoftware", "Brave-Browser", "Application", "brave.exe")
            ]
        }

        return paths.get(browser_id, [])

    def _resolve_icon_path(self, icon_name: Optional[str]) -> Optional[str]:
        """Resolve icon path relative to assets directory"""
        if not icon_name:
            return None

        if getattr(sys, 'frozen', False):
            icon_path = os.path.join(sys._MEIPASS, "assets", icon_name)
        else:
            icon_path = os.path.join(os.path.dirname(__file__), "..", "assets", icon_name)

        return icon_path if os.path.exists(icon_path) else None

    def get_browser_path(self, browser_id: str) -> Optional[str]:
        """Get the executable path for the specified browser"""
        browser = self.browsers.get(browser_id.lower())
        if not browser or browser.id == "default":
            return None
        return browser.executable

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
