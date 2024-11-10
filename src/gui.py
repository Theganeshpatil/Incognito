import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from PIL import Image, ImageTk
from steganography import SteganographyTool
import os
import cv2
import logging

class SteganographyGUI:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Incognito - Image Steganography Tool")
        self.root.geometry("900x700")  # Increased size for preview
        
        self.steg_tool = SteganographyTool()
        self.current_image = None
        self.photo = None
        
        # Configure logging
        self.setup_logging()
        self.setup_ui()
        
        self.logger.info("Application started")
    
    def setup_logging(self):
        self.logger = logging.getLogger('Incognito')
        self.logger.setLevel(logging.INFO)
        
        # Create logs directory if it doesn't exist
        if not os.path.exists('logs'):
            os.makedirs('logs')
    
    def setup_ui(self):
        # Create main frame with proper weight configuration
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky="nsew")
        main_frame.grid_columnconfigure(1, weight=1)
        
        # Left panel for image preview and metadata
        left_panel = ttk.LabelFrame(main_frame, text="Image Information", padding="5")
        left_panel.grid(row=0, column=0, padx=(0, 10), sticky="nsew")
        
        # Image preview
        self.preview_label = ttk.Label(left_panel, text="No image selected")
        self.preview_label.grid(row=0, column=0, padx=5, pady=5)
        
        # Image metadata
        self.metadata_text = tk.Text(left_panel, height=10, width=40, wrap=tk.WORD)
        self.metadata_text.grid(row=1, column=0, padx=5, pady=5)
        self.metadata_text.config(state=tk.DISABLED)
        
        # Right panel
        right_panel = ttk.Frame(main_frame)
        right_panel.grid(row=0, column=1, sticky="nsew")
        
        # Image selection
        ttk.Label(right_panel, text="Select Image:").grid(row=0, column=0, sticky=tk.W)
        self.image_path = tk.StringVar()
        self.image_entry = ttk.Entry(right_panel, textvariable=self.image_path, width=50)
        self.image_entry.grid(row=0, column=1, padx=5)
        ttk.Button(right_panel, text="Browse", command=self.browse_image).grid(row=0, column=2)
        
        # Message input
        ttk.Label(right_panel, text="Message:").grid(row=1, column=0, sticky=tk.W, pady=10)
        self.message_text = tk.Text(right_panel, height=5, width=50)
        self.message_text.grid(row=1, column=1, columnspan=2, pady=10)
        
        # Password input
        ttk.Label(right_panel, text="Password:").grid(row=2, column=0, sticky=tk.W)
        self.password_var = tk.StringVar()
        self.password_entry = ttk.Entry(right_panel, textvariable=self.password_var, show="*", width=50)
        self.password_entry.grid(row=2, column=1, columnspan=2, pady=10)
        
        # Action buttons
        button_frame = ttk.Frame(right_panel)
        button_frame.grid(row=3, column=0, columnspan=3, pady=20)
        
        ttk.Button(button_frame, text="Embed Message", command=self.embed_message).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Extract Message", command=self.extract_message).pack(side=tk.LEFT, padx=5)
        
        # Status label
        self.status_var = tk.StringVar()
        ttk.Label(right_panel, textvariable=self.status_var).grid(row=4, column=0, columnspan=3)
    
    def update_image_preview(self, image_path):
        """Update the image preview and metadata"""
        try:
            # Load and resize image for preview
            image = Image.open(image_path)
            # Calculate resize ratio while maintaining aspect ratio
            display_size = (300, 300)
            image.thumbnail(display_size, Image.Resampling.LANCZOS)
            
            # Convert to PhotoImage for display
            self.photo = ImageTk.PhotoImage(image)
            self.preview_label.config(image=self.photo)
            
            # Update metadata
            self.update_metadata(image_path)
            
        except Exception as e:
            self.preview_label.config(text="Error loading image preview")
            messagebox.showerror("Error", f"Failed to load image preview: {str(e)}")
    
    def update_metadata(self, image_path):
        """Update the metadata display"""
        try:
            image = Image.open(image_path)
            cv_image = cv2.imread(image_path)
            
            metadata = f"Filename: {os.path.basename(image_path)}\n"
            metadata += f"Format: {image.format}\n"
            metadata += f"Mode: {image.mode}\n"
            metadata += f"Size: {image.size[0]}x{image.size[1]} pixels\n"
            metadata += f"File size: {os.path.getsize(image_path)/1024:.2f} KB\n"
            metadata += f"Color channels: {cv_image.shape[2]}\n"
            
            # Calculate maximum message size
            max_bytes = (cv_image.shape[0] * cv_image.shape[1] * 3) // 8
            metadata += f"Max message size: {max_bytes} bytes\n"
            
            self.metadata_text.config(state=tk.NORMAL)
            self.metadata_text.delete(1.0, tk.END)
            self.metadata_text.insert(tk.END, metadata)
            self.metadata_text.config(state=tk.DISABLED)
            
        except Exception as e:
            self.metadata_text.config(state=tk.NORMAL)
            self.metadata_text.delete(1.0, tk.END)
            self.metadata_text.insert(tk.END, f"Error loading metadata: {str(e)}")
            self.metadata_text.config(state=tk.DISABLED)
    
    def browse_image(self):
        filename = filedialog.askopenfilename(
            filetypes=[("Image files", "*.png *.jpg *.jpeg *.bmp")]
        )
        if filename:
            self.image_path.set(filename)
            self.update_image_preview(filename)
    
    def embed_message(self):
        if not self.image_path.get():
            messagebox.showerror("Error", "Please select an image first")
            return
            
        message = self.message_text.get("1.0", tk.END).strip()
        if not message:
            messagebox.showerror("Error", "Please enter a message to embed")
            return
            
        password = self.password_var.get()
        if not password:
            messagebox.showerror("Error", "Please enter a password")
            return
            
        output_path = filedialog.asksaveasfilename(
            defaultextension=".png",
            filetypes=[("PNG files", "*.png")]
        )
        if output_path:
            success, result = self.steg_tool.embed_message(
                self.image_path.get(),
                message,
                password,
                output_path
            )
            
            if success:
                messagebox.showinfo("Success", result)
                self.message_text.delete("1.0", tk.END)
                self.password_var.set("")
            else:
                messagebox.showerror("Error", result)
    
    def extract_message(self):
        if not self.image_path.get():
            messagebox.showerror("Error", "Please select an image first")
            return
            
        password = self.password_var.get()
        if not password:
            messagebox.showerror("Error", "Please enter a password")
            return
            
        success, result = self.steg_tool.extract_message(self.image_path.get(), password)
        
        if success:
            self.message_text.delete("1.0", tk.END)
            self.message_text.insert("1.0", result)
            messagebox.showinfo("Success", "Message extracted successfully")
        else:
            messagebox.showerror("Error", result)
    
    def run(self):
        self.root.mainloop()