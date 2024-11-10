import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from steganography import SteganographyTool
import os

class SteganographyGUI:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Incognito - Image Steganography Tool")
        self.root.geometry("600x400")
        
        self.steg_tool = SteganographyTool()
        
        self.setup_ui()
    
    def setup_ui(self):
        # Create main frame
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Image selection
        ttk.Label(main_frame, text="Select Image:").grid(row=0, column=0, sticky=tk.W)
        self.image_path = tk.StringVar()
        self.image_entry = ttk.Entry(main_frame, textvariable=self.image_path, width=50)
        self.image_entry.grid(row=0, column=1, padx=5)
        ttk.Button(main_frame, text="Browse", command=self.browse_image).grid(row=0, column=2)
        
        # Message input
        ttk.Label(main_frame, text="Message:").grid(row=1, column=0, sticky=tk.W, pady=10)
        self.message_text = tk.Text(main_frame, height=5, width=50)
        self.message_text.grid(row=1, column=1, columnspan=2, pady=10)
        
        # Action buttons
        button_frame = ttk.Frame(main_frame)
        button_frame.grid(row=2, column=0, columnspan=3, pady=20)
        
        ttk.Button(button_frame, text="Embed Message", command=self.embed_message).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Extract Message", command=self.extract_message).pack(side=tk.LEFT, padx=5)
        
        # Status label
        self.status_var = tk.StringVar()
        ttk.Label(main_frame, textvariable=self.status_var).grid(row=3, column=0, columnspan=3)
    
    def browse_image(self):
        filename = filedialog.askopenfilename(
            filetypes=[("Image files", "*.png *.jpg *.jpeg *.bmp")]
        )
        if filename:
            self.image_path.set(filename)
    
    def embed_message(self):
        if not self.image_path.get():
            messagebox.showerror("Error", "Please select an image first")
            return
            
        message = self.message_text.get("1.0", tk.END).strip()
        if not message:
            messagebox.showerror("Error", "Please enter a message to embed")
            return
            
        output_path = filedialog.asksaveasfilename(
            defaultextension=".png",
            filetypes=[("PNG files", "*.png")]
        )
        if output_path:
            success, result = self.steg_tool.embed_message(
                self.image_path.get(),
                message,
                output_path
            )
            
            if success:
                messagebox.showinfo("Success", result)
            else:
                messagebox.showerror("Error", result)
    
    def extract_message(self):
        if not self.image_path.get():
            messagebox.showerror("Error", "Please select an image first")
            return
            
        success, result = self.steg_tool.extract_message(self.image_path.get())
        
        if success:
            self.message_text.delete("1.0", tk.END)
            self.message_text.insert("1.0", result)
            messagebox.showinfo("Success", "Message extracted successfully")
        else:
            messagebox.showerror("Error", result)
    
    def run(self):
        self.root.mainloop() 