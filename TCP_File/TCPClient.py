import socket
import threading
import tkinter as tk
from tkinter import scrolledtext, messagebox

HOST = '127.0.0.1'
PORT = 1234

# Colors
DARK_GREY = '#121212'
MEDIUM_GREY = '#1F1B24'
OCEAN_BLUE = '#464EB8'
WHITE = "white"
FONT = ("Helvetica", 17)
BUTTON_FONT = ("Helvetica", 15)
SMALL_FONT = ("Helvetica", 13)

class MessengerClient:
    def __init__(self, root):
        self.root = root
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.setup_gui()

    def setup_gui(self):
        self.root.grid_rowconfigure(0, weight=1)
        self.root.grid_rowconfigure(1, weight=4)
        self.root.grid_rowconfigure(2, weight=1)

        top_frame = tk.Frame(self.root, width=600, height=100, bg=DARK_GREY)
        top_frame.grid(row=0, column=0, sticky=tk.NSEW)

        middle_frame = tk.Frame(self.root, width=600, height=400, bg=MEDIUM_GREY)
        middle_frame.grid(row=1, column=0, sticky=tk.NSEW)

        bottom_frame = tk.Frame(self.root, width=600, height=100, bg=DARK_GREY)
        bottom_frame.grid(row=2, column=0, sticky=tk.NSEW)

        username_label = tk.Label(top_frame, text="Enter username:", font=FONT, bg=DARK_GREY, fg=WHITE)
        username_label.pack(side=tk.LEFT, padx=10)

        self.username_textbox = tk.Entry(top_frame, font=FONT, bg=MEDIUM_GREY, fg=WHITE, width=23)
        self.username_textbox.pack(side=tk.LEFT)

        username_button = tk.Button(top_frame, text="Join", font=BUTTON_FONT, bg=OCEAN_BLUE, fg=WHITE, command=self.connect_to_server)
        username_button.pack(side=tk.LEFT, padx=15)

        self.message_textbox = tk.Entry(bottom_frame, font=FONT, bg=MEDIUM_GREY, fg=WHITE, width=38)
        self.message_textbox.pack(side=tk.LEFT, padx=10)

        message_button = tk.Button(bottom_frame, text="Send", font=BUTTON_FONT, bg=OCEAN_BLUE, fg=WHITE, command=self.send_message)
        message_button.pack(side=tk.LEFT, padx=10)

        self.message_box = scrolledtext.ScrolledText(middle_frame, font=SMALL_FONT, bg=MEDIUM_GREY, fg=WHITE, width=67, height=26.5)
        self.message_box.config(state=tk.DISABLED)
        self.message_box.pack(side=tk.TOP)

    def add_message(self, message):
        self.message_box.config(state=tk.NORMAL)
        self.message_box.insert(tk.END, message + '\n')
        self.message_box.config(state=tk.DISABLED)

    def connect_to_server(self):
        username = self.username_textbox.get()
        if username:
            try:
                self.client.connect((HOST, PORT))
                self.add_message("[SERVER] Successfully connected to the server")
                self.client.sendall(username.encode())
                threading.Thread(target=self.listen_for_messages_from_server).start()
                self.username_textbox.config(state=tk.DISABLED)
            except (ConnectionRefusedError, ConnectionError):
                messagebox.showerror("Connection Error", "Failed to connect to the server.")
        else:
            messagebox.showerror("Invalid username", "Username cannot be empty")

    def send_message(self):
        message = self.message_textbox.get()
        if message:
            try:
                self.client.sendall(message.encode())
                self.message_textbox.delete(0, tk.END)
            except ConnectionError:
                messagebox.showerror("Error", "Failed to send message. Lost connection to the server.")
        else:
            messagebox.showerror("Empty message", "Message cannot be empty")

    def listen_for_messages_from_server(self):
        while True:
            try:
                message = self.client.recv(2048).decode('utf-8')
                if message:
                    username, content = message.split("~")
                    self.add_message(f"[{username}] {content}")
                else:
                    messagebox.showerror("Error", "Received empty message from the server")
            except ConnectionResetError:
                messagebox.showerror("Connection Error", "Lost connection to the server.")
                self.root.quit()
                break

    def close_connection(self):
        self.client.close()
        self.root.quit()

def main():
    root = tk.Tk()
    root.geometry("600x600")
    root.title("Messenger Client")
    root.resizable(False, False)
    client_app = MessengerClient(root)
    root.protocol("WM_DELETE_WINDOW", client_app.close_connection)
    root.mainloop()

if __name__ == '__main__':
    main()
