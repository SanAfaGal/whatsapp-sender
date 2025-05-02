"""Application constants and configuration"""

DEFAULT_DELAYS = {
    "load_delay": {
        "label": "Page Load Delay (s):",
        "default": 15,
        "min": 5,
        "max": 30,
        "tooltip": "Time to wait for WhatsApp Web to load before sending message"
    },
    "msg_delay": {
        "label": "Delay Between Messages (s):",
        "default": 3,
        "min": 1,
        "max": 10,
        "tooltip": "Time to wait between sending consecutive messages"
    },
    "close_delay": {
        "label": "Tab Close Delay (s):",
        "default": 5,
        "min": 1,
        "max": 10,
        "tooltip": "Time to wait before closing the browser tab after sending"
    }
}