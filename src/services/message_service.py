"""WhatsApp message sending service"""
import os
import time
import webbrowser
from urllib.parse import quote

import pyautogui


def send_whatsapp_message(phone, message, browser_path=None, load_delay=10, close_delay=3):
    """
    Send a WhatsApp message using webbrowser and pyautogui
    
    Args:
        phone (str): Phone number to send the message to
        message (str): Message content
        browser_path (str, optional): Path to browser executable
        load_delay (int): Seconds to wait for WhatsApp Web to load
        close_delay (int): Seconds to wait before closing tab
        
    Returns:
        dict: Result containing success status and any error message
    """
    try:
        # Normalize phone number
        phone = phone.strip().replace(" ", "").replace("-", "")

        # Add country code if not present
        if not phone.startswith("+"):
            phone = "+" + phone

        # Validate phone number
        if len(phone) < 10:
            return {
                "success": False,
                "error": "Invalid phone number format"
            }

        # Validate browser path if provided
        if browser_path and not os.path.exists(browser_path):
            return {
                "success": False,
                "error": f"Browser not found at: {browser_path}"
            }

        # Prepare WhatsApp Web URL with phone and message
        encoded_message = quote(message)
        whatsapp_url = f"https://web.whatsapp.com/send?phone={phone}&text={encoded_message}"

        # Open URL in specified browser or default
        if browser_path:
            webbrowser.register('custom_browser', None,
                                webbrowser.BackgroundBrowser(browser_path))
            browser = webbrowser.get('custom_browser')
        else:
            browser = webbrowser.get()

        browser.open(whatsapp_url, new=2)

        # Wait for WhatsApp Web to load
        time.sleep(load_delay)

        # Press Enter to send message
        pyautogui.press('enter')

        # Wait before closing
        time.sleep(close_delay)

        # Close tab with Ctrl+W
        if close_delay > 0:
            pyautogui.hotkey('ctrl', 'w')

        return {
            "success": True,
            "error": None
        }

    except Exception as e:
        return {
            "success": False,
            "error": str(e)
        }


def send_messages_batch(messages, delays, browser_path=None, progress_callback=None):
    """
    Send multiple WhatsApp messages
    
    Args:
        messages (list): List of message objects
        delays (dict): Dictionary of delay settings
        browser_path (str, optional): Path to browser executable
        progress_callback (callable, optional): Callback for progress updates
        
    Returns:
        list: List of results for each message
    """
    results = []
    total = len(messages)

    for i, msg_data in enumerate(messages, 1):
        phone = msg_data["TELEFONO"]
        message = msg_data["MENSAJE"]

        if progress_callback:
            progress_callback(f"[{i}/{total}] Sending to {phone}...")

        try:
            result = send_whatsapp_message(
                phone,
                message,
                browser_path=browser_path,
                load_delay=delays["load_delay"],
                close_delay=delays["close_delay"]
            )

            if result["success"]:
                if progress_callback:
                    progress_callback(f"✓ Message sent to {phone}", "success")
            else:
                if progress_callback:
                    progress_callback(f"✗ Failed to send to {phone}: {result['error']}", "error")

            results.append(result)

        except Exception as e:
            if progress_callback:
                progress_callback(f"✗ Error sending to {phone}: {str(e)}", "error")
            results.append({
                "success": False,
                "error": str(e)
            })

        if i < total:
            time.sleep(delays["msg_delay"])

    return results
