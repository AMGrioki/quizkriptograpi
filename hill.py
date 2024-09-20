import numpy as np
import tkinter as tk
from tkinter import messagebox

# Fungsi untuk memproses kunci menjadi matriks
def create_key_matrix(key, size):
    key_matrix = []
    key = key.upper().replace(" ", "")
    
    if len(key) < size * size:
        messagebox.showerror("Error", "Kunci terlalu pendek!")
        return None
    
    for i in range(size):
        row = [ord(key[i * size + j]) % 65 for j in range(size)]
        key_matrix.append(row)
    
    return np.array(key_matrix)

# Fungsi untuk mengenkripsi menggunakan Hill Cipher
def encrypt_hill(plaintext, key):
    size = int(len(key) ** 0.5)
    key_matrix = create_key_matrix(key, size)
    
    if key_matrix is None:
        return
    
    plaintext = plaintext.upper().replace(" ", "")
    
    if len(plaintext) % size != 0:
        padding = size - (len(plaintext) % size)
        plaintext += 'X' * padding  # Isi padding dengan X

    ciphertext = ""
    for i in range(0, len(plaintext), size):
        block = [ord(char) % 65 for char in plaintext[i:i+size]]
        encrypted_block = np.dot(key_matrix, block) % 26
        ciphertext += ''.join(chr(int(num) + 65) for num in encrypted_block)
    
    return ciphertext

# Fungsi untuk mencari invers dari matriks (untuk dekripsi)
def mod_inverse(matrix, modulus):
    determinant = int(np.round(np.linalg.det(matrix))) % modulus
    determinant_inv = pow(determinant, -1, modulus)
    matrix_inv = determinant_inv * np.round(determinant * np.linalg.inv(matrix)).astype(int) % modulus
    return matrix_inv

# Fungsi untuk mendekripsi menggunakan Hill Cipher
def decrypt_hill(ciphertext, key):
    size = int(len(key) ** 0.5)
    key_matrix = create_key_matrix(key, size)
    
    if key_matrix is None:
        return
    
    inverse_key_matrix = mod_inverse(key_matrix, 26)
    
    ciphertext = ciphertext.upper().replace(" ", "")
    
    plaintext = ""
    for i in range(0, len(ciphertext), size):
        block = [ord(char) % 65 for char in ciphertext[i:i+size]]
        decrypted_block = np.dot(inverse_key_matrix, block) % 26
        plaintext += ''.join(chr(int(num) + 65) for num in decrypted_block)
    
    return plaintext

# Fungsi untuk memproses teks dan menampilkan hasil enkripsi/dekripsi
def process_text(mode):
    text = entry_text.get().upper()
    key = entry_key.get().upper().replace(" ", "")
    
    if not text.isalpha() or not key.isalpha():
        messagebox.showerror("Error", "Teks dan kunci hanya boleh mengandung huruf!")
        return
    
    size = int(len(key) ** 0.5)
    
    if len(key) != size * size:
        messagebox.showerror("Error", "Kunci harus berupa string yang panjangnya adalah kuadrat sempurna (contoh: 4, 9, 16, dst).")
        return
    
    if mode == 'encrypt':
        result = encrypt_hill(text, key)
    elif mode == 'decrypt':
        result = decrypt_hill(text, key)
    
    if result:
        label_result.config(text=f"Hasil: {result}")

# Membuat jendela utama
window = tk.Tk()
window.title("Hill Cipher")
window.geometry("400x300")

# Membuat label dan entry untuk teks yang akan dienkripsi/dekripsi
label_text = tk.Label(window, text="Teks:")
label_text.pack(pady=10)
entry_text = tk.Entry(window, width=50)
entry_text.pack(pady=5)

# Membuat label dan entry untuk kunci
label_key = tk.Label(window, text="Kunci (Contoh: GYBNQKURP):")
label_key.pack(pady=10)
entry_key = tk.Entry(window, width=50)
entry_key.pack(pady=5)

# Membuat tombol enkripsi dan dekripsi
button_encrypt = tk.Button(window, text="Enkripsi", command=lambda: process_text('encrypt'))
button_encrypt.pack(pady=5)

button_decrypt = tk.Button(window, text="Dekripsi", command=lambda: process_text('decrypt'))
button_decrypt.pack(pady=5)

# Label untuk menampilkan hasil
label_result = tk.Label(window, text="Hasil:", font=('Arial', 12))
label_result.pack(pady=20)

# Menjalankan antarmuka
window.mainloop()
