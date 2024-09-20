import tkinter as tk
from tkinter import messagebox
import string

def generate_playfair_key_matrix(key):
    key = key.upper().replace("J", "I")
    matrix = []
    seen = set()
    
    for char in key:
        if char not in seen and char in string.ascii_uppercase:
            seen.add(char)
            matrix.append(char)
    
    for char in string.ascii_uppercase:
        if char not in seen and char != 'J':
            seen.add(char)
            matrix.append(char)
    
    return [matrix[i:i+5] for i in range(0, 25, 5)]

def find_position(matrix, char):
    for i, row in enumerate(matrix):
        if char in row:
            return i, row.index(char)
    return None

# Fungsi untuk mengenkripsi menggunakan Playfair Cipher
def encrypt_playfair(plaintext, key):
    matrix = generate_playfair_key_matrix(key)
    plaintext = plaintext.upper().replace("J", "I").replace(" ", "")
    
    # Membuat pasangan-pasangan huruf
    pairs = []
    i = 0
    while i < len(plaintext):
        char1 = plaintext[i]
        char2 = plaintext[i + 1] if i + 1 < len(plaintext) else 'X'
        
        if char1 == char2:
            pairs.append((char1, 'X'))
            i += 1
        else:
            pairs.append((char1, char2))
            i += 2
    
    ciphertext = ""
    for char1, char2 in pairs:
        row1, col1 = find_position(matrix, char1)
        row2, col2 = find_position(matrix, char2)
        
        if row1 == row2:
            ciphertext += matrix[row1][(col1 + 1) % 5]
            ciphertext += matrix[row2][(col2 + 1) % 5]
        elif col1 == col2:
            ciphertext += matrix[(row1 + 1) % 5][col1]
            ciphertext += matrix[(row2 + 1) % 5][col2]
        else:
            ciphertext += matrix[row1][col2]
            ciphertext += matrix[row2][col1]
    
    return ciphertext

# dekripsi Playfair Cipher
def decrypt_playfair(ciphertext, key):
    matrix = generate_playfair_key_matrix(key)
    ciphertext = ciphertext.upper().replace(" ", "")
    
    pairs = [(ciphertext[i], ciphertext[i + 1]) for i in range(0, len(ciphertext), 2)]
    
    plaintext = ""
    for char1, char2 in pairs:
        row1, col1 = find_position(matrix, char1)
        row2, col2 = find_position(matrix, char2)
        
        if row1 == row2:
            plaintext += matrix[row1][(col1 - 1) % 5]
            plaintext += matrix[row2][(col2 - 1) % 5]
        elif col1 == col2:
            plaintext += matrix[(row1 - 1) % 5][col1]
            plaintext += matrix[(row2 - 1) % 5][col2]
        else:
            plaintext += matrix[row1][col2]
            plaintext += matrix[row2][col1]
    
    return plaintext

# hasil enkripsi/dekripsi
def process_text(mode):
    text = entry_text.get().upper()
    key = entry_key.get().upper()
    
    if not text.isalpha() or not key.isalpha():
        messagebox.showerror("Error")
        return
    
    if mode == 'encrypt':
        result = encrypt_playfair(text, key)
    elif mode == 'decrypt':
        result = decrypt_playfair(text, key)
    
    label_result.config(text=f"Hasil: {result}")

window = tk.Tk()
window.title("Playfair")
window.geometry("400x400")

label_text = tk.Label(window, text="Text:")
label_text.pack(pady=10)
entry_text = tk.Entry(window, width=50)
entry_text.pack(pady=5)

label_key = tk.Label(window, text="Key:")
label_key.pack(pady=10)
entry_key = tk.Entry(window, width=50)
entry_key.pack(pady=5)

# tombol enkripsi dan dekripsi
button_encrypt = tk.Button(window, text="encrypt", command=lambda: process_text('encrypt'))
button_encrypt.pack(pady=5)

button_decrypt = tk.Button(window, text="decrypt", command=lambda: process_text('decrypt'))
button_decrypt.pack(pady=5)

# menampilkan hasil
label_result = tk.Label(window, text="Hasil:")
label_result.pack(pady=20)

# antarmuka
window.mainloop()
