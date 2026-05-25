# gui.py
# Simple desktop GUI for the File Organizer tool using Tkinter

import tkinter as tk
from tkinter import filedialog, messagebox, scrolledtext
import threading
import sys
import os

# Add current directory to path so we can import our modules
sys.path.insert(0, os.path.dirname(__file__))

from organizer import Organizer

class FileOrganizerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("File Organizer")
        self.root.geometry("600x500")
        self.root.configure(bg="#1e1e2e")
        self.root.resizable(False, False)

        # Title
        tk.Label(root, text="🗂 File Organizer", font=("Arial", 20, "bold"),
                 bg="#1e1e2e", fg="#cdd6f4").pack(pady=20)

        # Folder selection
        frame = tk.Frame(root, bg="#1e1e2e")
        frame.pack(pady=5, padx=20, fill="x")

        self.folder_var = tk.StringVar()
        tk.Entry(frame, textvariable=self.folder_var, font=("Arial", 11),
                 bg="#313244", fg="#cdd6f4", insertbackground="white",
                 relief="flat", width=45).pack(side="left", ipady=6, padx=(0, 10))

        tk.Button(frame, text="Browse", command=self.browse_folder,
                  bg="#89b4fa", fg="#1e1e2e", font=("Arial", 10, "bold"),
                  relief="flat", padx=10).pack(side="left")

        # Dry run checkbox
        self.dry_run = tk.BooleanVar(value=True)
        tk.Checkbutton(root, text="Dry Run (preview only, don't move files)",
                       variable=self.dry_run, bg="#1e1e2e", fg="#a6e3a1",
                       selectcolor="#313244", font=("Arial", 10)).pack(pady=5)

        # Organize button
        tk.Button(root, text="Organize Files", command=self.run_organizer,
                  bg="#a6e3a1", fg="#1e1e2e", font=("Arial", 12, "bold"),
                  relief="flat", padx=20, pady=8).pack(pady=10)

        # Output log
        tk.Label(root, text="Output:", bg="#1e1e2e", fg="#cdd6f4",
                 font=("Arial", 10)).pack(anchor="w", padx=20)

        self.log = scrolledtext.ScrolledText(root, height=12, font=("Courier", 9),
                                              bg="#313244", fg="#cdd6f4",
                                              insertbackground="white", relief="flat")
        self.log.pack(padx=20, pady=5, fill="both")

    def browse_folder(self):
        folder = filedialog.askdirectory()
        if folder:
            self.folder_var.set(folder)

    def run_organizer(self):
        folder = self.folder_var.get().strip()
        if not folder:
            messagebox.showwarning("No Folder", "Please select a folder first!")
            return

        self.log.delete("1.0", tk.END)
        self.log.insert(tk.END, f"📁 Target: {folder}\n")
        self.log.insert(tk.END, f"🔍 Mode: {'Dry Run' if self.dry_run.get() else 'Live'}\n\n")

        def organize():
            try:
                org = Organizer(folder, dry_run=self.dry_run.get(), verbose=True)
                result = org.organize()

                self.log.insert(tk.END, f"✅ Moved: {result.moved}\n")
                self.log.insert(tk.END, f"⏭ Skipped: {result.skipped}\n")
                self.log.insert(tk.END, f"❌ Errors: {result.errors}\n\n")

                for action in result.actions:
                    self.log.insert(tk.END, f"  {action}\n")

                if self.dry_run.get():
                    self.log.insert(tk.END, "\n⚠️ Dry run complete. No files were moved.\n")
                else:
                    self.log.insert(tk.END, "\n🎉 Done! Files have been organized.\n")

            except Exception as e:
                self.log.insert(tk.END, f"\n❌ Error: {str(e)}\n")

        threading.Thread(target=organize, daemon=True).start()

if __name__ == "__main__":
    root = tk.Tk()
    app = FileOrganizerApp(root)
    root.mainloop()