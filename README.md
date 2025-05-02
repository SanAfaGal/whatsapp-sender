# WhatsApp Message Sender

A Python desktop application that automates sending WhatsApp messages to multiple recipients using WhatsApp Web. Built with Tkinter and PyAutoGUI, this tool helps streamline the process of sending bulk messages while maintaining a user-friendly interface.

![WhatsApp Message Sender](https://images.pexels.com/photos/267350/pexels-photo-267350.jpeg?auto=compress&cs=tinysrgb&w=1260&h=750&dpr=1)

## Key Features

- 📱 Send WhatsApp messages automatically from JSON data
- 🔄 Support for multiple vendors/users with separate message queues
- ⏱️ Configurable timing delays for message sending
- 🌐 Multiple browser support (Default, Edge, Brave)
- 📝 Real-time activity logging
- 🎨 Modern and intuitive user interface

## Technologies Used

- Python 3.x
- Tkinter (GUI framework)
- PyAutoGUI (Automation)
- JSON (Data format)
- WhatsApp Web API

## Prerequisites

Before installing the application, ensure you have:

- Python 3.x installed
- pip (Python package manager)
- A modern web browser
- Active WhatsApp account
- WhatsApp Web access

## Installation

1. Clone the repository or download the source code:
```bash
git clone https://github.com/sanafagal/whatsapp-sender.git
cd whatsapp-sender
```

2. Create a virtual environment (recommended):
```bash
python -m venv venv
source venv\Scripts\activate  # On Windows
```

3. Install required dependencies:
```bash
pip install -r requirements.txt
```

## Configuration

1. Browser Paths (Optional)
   - Update browser paths in `src/utils/browser_utils.py` if needed:
   ```python
   BROWSER_PATHS = {
       "edge": r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe",
       "brave": r"C:\Program Files\BraveSoftware\Brave-Browser\Application\brave.exe"
   }
   ```

2. Timing Settings (Optional)
   - Modify default delays in `src/config/constants.py`:
   ```python
   DEFAULT_DELAYS = {
       "load_delay": {"default": 10, "min": 5, "max": 30},
       "msg_delay": {"default": 3, "min": 1, "max": 10},
       "close_delay": {"default": 3, "min": 1, "max": 10}
   }
   ```

## Usage

1. Start the application:
```bash
python src/app.py
```

2. Prepare your JSON data file with the following structure:
```json
[
    {
        "VENDEDOR": "BGL",
        "TELEFONO": "+573001002000",
        "MENSAJE": "Hello, this is a test message!"
    }
]
```

3. Using the Application:
   - Click "Browse & Load" to select your JSON file
   - Configure timing settings if needed
   - Select the appropriate browser
   - Click on a vendor button to start sending messages
   - Monitor progress in the activity log

## JSON File Format

The application expects a JSON file with the following structure:

| Field    | Type   | Description                    |
|----------|--------|--------------------------------|
| VENDEDOR | string | Vendor/user identifier         |
| TELEFONO | string | Recipient's phone number       |
| MENSAJE  | string | Message content to be sent     |

## Best Practices

1. Phone Numbers:
   - It does not include country code
   - Remove spaces and special characters
   - Ensure proper formatting

2. Messages:
   - Keep messages concise
   - Avoid excessive special characters
   - Test with small batches first

3. Timing:
   - Adjust delays based on your internet speed
   - Allow sufficient time for WhatsApp Web to load
   - Don't set delays too low to avoid rate limiting

## Troubleshooting

Common issues and solutions:

1. WhatsApp Web not loading:
   - Increase the page load delay
   - Check internet connection
   - Ensure browser path is correct

2. Messages not sending:
   - Verify phone number format
   - Check WhatsApp Web login status
   - Adjust timing settings

3. Browser issues:
   - Update browser paths in configuration
   - Try using the default browser
   - Clear browser cache/cookies

## Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Contact

For support or queries:
- Create an issue in the repository
- Email: afanadorgaleano@gmail.com

---

**Note**: This application is not affiliated with WhatsApp or Meta. Use responsibly and in accordance with WhatsApp's terms of service.