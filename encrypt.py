import os
from cryptography.fernet import Fernet, InvalidToken

# Collect files except scripts + key
def get_files():
    files = []
    for f in os.listdir():
        if f in ("thekey.key", "decryptor.py", "encrypt.py", "testd.py"):
            continue
        if os.path.isfile(f):
            files.append(f)
    return files

files = get_files()
print("Files:", files)

# ---------------------------
# 1. DECRYPT WITH OLD KEY
# ---------------------------
if os.path.exists("thekey.key"):
    print("Decrypting old files...")
    old_key = open("thekey.key", "rb").read()
    fernet_old = Fernet(old_key)

    for file in files:
        data = open(file, "rb").read()
        try:
            decrypted = fernet_old.decrypt(data)
            open(file, "wb").write(decrypted)
        except InvalidToken:
            print(f"[!] {file} was not encrypted with the old key (skipping)")
else:
    print("No old key found, skipping decryption.")

# ---------------------------
# 2. GENERATE NEW KEY
# ---------------------------
print("Generating NEW key...")
new_key = Fernet.generate_key()
open("thekey.key", "wb").write(new_key)
fernet_new = Fernet(new_key)

# ---------------------------
# 3. ENCRYPT WITH NEW KEY
# ---------------------------
print("Encrypting files with new key...")
for file in files:
    data = open(file, "rb").read()
    encrypted = fernet_new.encrypt(data)
    open(file, "wb").write(encrypted)

print("Done! Files re-encrypted with a new key.")


