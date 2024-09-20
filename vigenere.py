import tkinter as tk
from tkinter import messagebox

def encrypt_vigenere(plaintext, key):
    cipher_text = []
    key = key.upper()
    key_length = len(key)
    key_as_int = [ord(i) for i in key]
    plaintext_int = [ord(i) for i in plaintext]
    
    for i in range(len(plaintext_int)):
        value = (plaintext_int[i] + key_as_int[i % key_length]) % 26
        cipher_text.append(chr(value + 65))
    
    return ''.join(cipher_text)

def decrypt_vigenere(ciphertext, key):
    plain_text = []
    key = key.upper()
    key_length = len(key)
    key_as_int = [ord(i) for i in key]
    ciphertext_int = [ord(i) for i in ciphertext]
    
    for i in range(len(ciphertext_int)):
        value = (ciphertext_int[i] - key_as_int[i % key_length]) % 26
        plain_text.append(chr(value + 65))
    
    return ''.join(plain_text)

def process_text(mode):
    text = entry_text.get().upper()
    key = entry_key.get().upper()
    
    if not text.isalpha() or not key.isalpha():
        messagebox.showerror("Error")
        return
    
    if mode == 'encrypt':
        result = encrypt_vigenere(text, key)
    elif mode == 'decrypt':
        result = decrypt_vigenere(text, key)
    
    label_result.config(text=f"Hasil: {result}")

def copy_to_clipboard():
    result_text = label_result.cget("text")[7:] 
    if result_text:
        window.clipboard_clear() 
        window.clipboard_append(result_text) 
        messagebox.showinfo("Info", "berhasil disalin")

window = tk.Tk()
window.title("Vigenere")
window.geometry("400x400")

label_text = tk.Label(window, text="Text:")
label_text.pack(pady=10)
entry_text = tk.Entry(window, width=50)
entry_text.pack(pady=5)

label_key = tk.Label(window, text="key:")
label_key.pack(pady=10)
entry_key = tk.Entry(window, width=50)
entry_key.pack(pady=5)

button_encrypt = tk.Button(window, text="Enkripsi", command=lambda: process_text('encrypt'))
button_encrypt.pack(pady=5)

button_decrypt = tk.Button(window, text="Dekripsi", command=lambda: process_text('decrypt'))
button_decrypt.pack(pady=5)

label_result = tk.Label(window, text="Hasil", font=('Arial', 12))
label_result.pack(pady=10)

button_copy = tk.Button(window, text="Copy", command=copy_to_clipboard)
button_copy.pack(pady=10)

window.mainloop()
