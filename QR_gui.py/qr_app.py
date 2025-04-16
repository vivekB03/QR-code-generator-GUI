import qrcode
from PIL import Image, ImageTk
import tkinter as tk
from tkinter import filedialog, messagebox

# Initialize the main window
root = tk.Tk()
root.title("QR Code Generator")
root.geometry("400x550")
root.resizable(False, False)
root.configure(bg="white")

# Title label
tk.Label(root, text="QR Code Generator", font=("Arial", 20, "bold"), bg="white", fg="#2d3436").pack(pady=20)

# Instruction label
tk.Label(root, text="Enter text or URL:", font=("Arial", 14), bg="white").pack(pady=5)

# Input field for user data
entry = tk.Entry(root, font=("Arial", 12), width=35, justify="center")
entry.pack(pady=5)

# Placeholder to show the QR code image
qr_display = tk.Label(root, bg="white")
qr_display.pack(pady=20)

# Function to create a QR code image (with optional logo in the center)
def create_qr_image(data):
    qr = qrcode.QRCode(error_correction=qrcode.constants.ERROR_CORRECT_H)
    qr.add_data(data)
    qr.make(fit=True)
    
    # Create the QR code image
    img = qr.make_image(fill_color="#0984e3", back_color="white").convert('RGB')
    
    # Optional: Add a logo to the center of the QR code
    try:
        logo = Image.open("logo.png")  # Make sure this file exists in your folder
        logo = logo.resize((60, 60))   # Resize logo to fit inside QR
        pos = ((img.size[0] - 60) // 2, (img.size[1] - 60) // 2)  # Center it
        img.paste(logo, pos)
    except Exception as e:
        print("Logo not added:", e)

    return img

# When the user clicks "Generate", create and display the QR code
def generate_qr():
    data = entry.get().strip()
    if not data:
        messagebox.showwarning("Warning", "Please enter some data to generate QR code.")
        return

    img = create_qr_image(data)
    img.save("qr_temp.png")  # Temporary image for display

    # Resize for GUI preview
    img_resized = img.resize((200, 200))
    tk_img = ImageTk.PhotoImage(img_resized)

    # Show it in the label
    qr_display.config(image=tk_img)
    qr_display.image = tk_img

# Let the user save the generated QR code to a file
def save_qr():
    data = entry.get().strip()
    if not data:
        messagebox.showwarning("Warning", "Please generate a QR code before saving.")
        return

    # Ask user where to save the file
    file_path = filedialog.asksaveasfilename(
        defaultextension=".png",
        filetypes=[("PNG files", "*.png")],
        title="Save QR Code As"
    )

    if file_path:
        img = create_qr_image(data)
        img.save(file_path)
        messagebox.showinfo("Saved", f"QR Code saved to:\n{file_path}")

# Optional: Clear the input and preview area
def clear_input():
    entry.delete(0, tk.END)
    qr_display.config(image="")
    qr_display.image = None

# Buttons for the user to interact with
tk.Button(root, text="Generate QR Code", command=generate_qr,
          font=("Arial", 12), bg="#0984e3", fg="white", width=20).pack(pady=10)

tk.Button(root, text="Save QR Code As...", command=save_qr,
          font=("Arial", 12), bg="#00b894", fg="white", width=20).pack(pady=5)

tk.Button(root, text="Clear", command=clear_input,
          font=("Arial", 12), bg="#d63031", fg="white", width=20).pack(pady=5)

# Run the application
root.mainloop()
