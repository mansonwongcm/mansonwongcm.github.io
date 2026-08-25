import tkinter as tk
from tkinter import messagebox
import os

def load_dictionary(file_path):
    """Reads the raw text file and maps Chinese characters to their Wu romanizations."""
    char_to_wu = {}
    if not os.path.exists(file_path):
        return None
        
    with open(file_path, 'r', encoding='utf-8') as f:
        in_data_section = False
        for line in f:
            line = line.strip()
            
            # Detects where metadata header ends and the actual list starts
            if line == "...":
                in_data_section = True
                continue
                
            # Automatically skips comments and empty spaces
            if not line or line.startswith('#'):
                continue
            if not in_data_section:
                continue
                
            # Safely splits your character column from the romanization column
            parts = [p for p in line.replace('\t', ' ').split(' ') if p]
            
            if len(parts) >= 2:
                char = parts[0]
                romanization = parts[1]
                
                # Handles multiple readings (polyphones) per single character
                if char not in char_to_wu:
                    char_to_wu[char] = []
                if romanization not in char_to_wu[char]:
                    char_to_wu[char].append(romanization)
    return char_to_wu

def convert_text():
    """Triggered on button click. Looks up input character and writes output."""
    input_text = entry_input.get("1.0", tk.END).strip()
    if not input_text:
        output_text.delete("1.0", tk.END)
        return
        
    result = []
    for char in input_text:
        if char in wu_dict:
            # Slashes separate different pronunciations of the same character
            pronunciations = "/".join(wu_dict[char])
            result.append(f"{char}[{pronunciations}]")
        else:
            # Keeps normal english characters, numbers, and punctuations untouched
            result.append(char)
            
    # Clear the layout output window and print updated translations
    output_text.delete("1.0", tk.END)
    output_text.insert(tk.END, " ".join(result))

# --- Main App Execution Layer ---
# Ensure this text name exactly matches your local text document file name
TEXT_FILE = "wugniu_zaonhe_revised.txt" 
wu_dict = load_dictionary(TEXT_FILE)

if wu_dict is None:
    root = tk.Tk()
    root.withdraw()
    messagebox.showerror("Error", f"Could not find dictionary text file named: '{TEXT_FILE}'\nPlease make sure it is in the same folder.")
else:
    # Build GUI window window frames
    window = tk.Tk()
    window.title("Interactive Chinese to Wu Romanization Dictionary")
    window.geometry("550x450")
    
    # Input label and multiline text input box
    label_in = tk.Label(window, text="Input Chinese Characters Below:", font=("Arial", 11, "bold"))
    label_in.pack(pady=5)
    
    entry_input = tk.Text(window, height=6, font=("Arial", 11))
    entry_input.pack(padx=15, pady=5, fill=tk.X)
    
    # Submission button
    btn_convert = tk.Button(window, text="Lookup Romanization ➔", bg="#2196F3", fg="white", 
                            font=("Arial", 11, "bold"), command=convert_text)
    btn_convert.pack(pady=10)
    
    # Output labels and locked/shaded textbox display fields
    label_out = tk.Label(window, text="Romanization Output Results:", font=("Arial", 11, "bold"))
    label_out.pack(pady=5)
    
    output_text = tk.Text(window, height=8, font=("Arial", 12), bg="#f9f9f9")
    output_text.pack(padx=15, pady=5, fill=tk.X)
    
    window.mainloop()
