import tkinter as tk
from components.app_window import WhatsAppSenderApp

def main():
    root = tk.Tk()
    app = WhatsAppSenderApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()