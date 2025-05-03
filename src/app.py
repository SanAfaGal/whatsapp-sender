import tkinter as tk

from src.components.app_window import WhatsAppSenderApp


def main():
    root = tk.Tk()
    WhatsAppSenderApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()
