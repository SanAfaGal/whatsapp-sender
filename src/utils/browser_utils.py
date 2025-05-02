"""Browser utility functions"""

# Default browser paths - update these according to typical installation paths
BROWSER_PATHS = {
    "edge": r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe",
    "brave": r"C:\Program Files\BraveSoftware\Brave-Browser\Application\brave.exe"
}

def get_browser_path(vendor):
    """Get default browser path based on vendor"""
    if vendor == "BGL":
        return BROWSER_PATHS["edge"]
    elif vendor == "SAG":
        return BROWSER_PATHS["brave"]
    return None