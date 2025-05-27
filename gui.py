import tkinter as tk
from tkinter import filedialog, ttk, messagebox
import threading
import os
from compressor import compress_and_save
from decompressor import decompress_received_file, RECEIVED_FILE
from sender import send_file
from receiver import receive_file
from voice_bot import listen_command, speak

class HuffmanApp:
    def __init__(self, root):
        self.root = root
        self.root.title("📦 Hybrid Huffman File Transfer")
        self.root.geometry("700x500")
        self.root.configure(bg="#1e1e1e")

        self.selected_file = None

        self.status_label = tk.Label(root, text="Status: Idle", fg="#88f", bg="#1e1e1e", font=("Segoe UI", 12))
        self.status_label.pack(pady=10)

        self.file_label = tk.Label(root, text="No file selected", fg="gray", bg="#1e1e1e", font=("Segoe UI", 10))
        self.file_label.pack()

        tk.Button(root, text="📁 Browse File", command=self.browse_file, bg="#444", fg="white").pack(pady=5)
        tk.Button(root, text="📤 Compress & Send", command=self.compress_and_send, bg="#2a2", fg="white", font=("Segoe UI", 11)).pack(pady=5)
        tk.Button(root, text="📥 Receive & Decompress", command=self.receive_and_decompress, bg="#229", fg="white", font=("Segoe UI", 11)).pack(pady=5)
        tk.Button(root, text="🎤 Talk to Assistant", command=self.voice_assistant, bg="#666", fg="white", font=("Segoe UI", 11)).pack(pady=5)

        self.progress = ttk.Progressbar(root, mode='indeterminate')
        self.progress.pack(pady=10, fill=tk.X, padx=20)

        self.log_window = tk.Text(root, height=12, bg="#121212", fg="#0f0", insertbackground="#0f0")
        self.log_window.pack(padx=20, pady=10, fill=tk.BOTH, expand=True)

        style = ttk.Style()
        style.theme_use('clam')
        style.configure("TProgressbar", foreground='green', background='green')

    def log(self, msg):
        self.log_window.insert(tk.END, msg + '\n')
        self.log_window.see(tk.END)

    def update_status(self, msg):
        self.status_label.config(text=f"Status: {msg}")

    def browse_file(self):
        filepath = filedialog.askopenfilename(filetypes=[("All Files", "*.*")])
        if not filepath:
            self.log("No file selected.")
            return
        self.selected_file = filepath
        self.file_label.config(text=filepath)
        self.log(f"Selected: {filepath}")

    def compress_and_send(self):
        if not self.selected_file:
            self.log("Error: No file selected")
            return
        self.update_status("Compressing & Sending...")
        self.progress.start()
        self.log("Compressing file...")

        def task():
            compress_and_save(self.selected_file)
            self.log("Sending file...")
            send_file()
            self.update_status("Idle")
            self.progress.stop()
            self.log("✅ File sent.")

        threading.Thread(target=task).start()

    def receive_and_decompress(self):
        self.update_status("Receiving & Decompressing...")
        self.progress.start()
        self.log("Receiving file...")

        def task():
            receive_file()
            self.log("Decompressing...")
            if os.path.exists(RECEIVED_FILE):
                result = decompress_received_file()
                self.log(f"✅ File received and saved to: {result}")
            else:
                self.log("❌ No received file found")
            self.update_status("Idle")
            self.progress.stop()

        threading.Thread(target=task).start()

    def voice_assistant(self):
        def handle():
            command = listen_command()
            self.log(f"🎤 You said: {command}")

            if "select" in command:
                self.browse_file()
            elif "compress" in command or "send" in command:
                self.compress_and_send()
            elif "receive" in command or "decompress" in command:
                self.receive_and_decompress()
            elif "exit" in command or "quit" in command:
                speak("Exiting application.")
                self.root.quit()
            else:
                self.log("❓ Unknown command")
                speak("Sorry, I did not understand that.")

        threading.Thread(target=handle).start()

if __name__ == '__main__':
    root = tk.Tk()
    app = HuffmanApp(root)
    root.mainloop()
