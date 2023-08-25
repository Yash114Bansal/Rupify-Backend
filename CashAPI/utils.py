import requests
from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
from Crypto.Util.Padding import pad
from uvicorn import run
import base64

otp_api_key = "5bf09b65-4327-11ee-addf-0200cd936042"
key_hex = '12345678901234567890123456789ABC'
key = bytes.fromhex(key_hex)

def SendOTP(otp,mobile_number):
    requests.get(f"https://2factor.in/API/V1/{otp_api_key}/SMS/{mobile_number}/{otp}/RupifyOTP")

def encrypt_note(note_number,aadhar,purpose):
    note = f"{aadhar}::{note_number}".encode()
    iv = get_random_bytes(AES.block_size)
    cipher = AES.new(key, AES.MODE_CBC, iv)
    padded_note = pad(note, AES.block_size)
    ciphertext = cipher.encrypt(padded_note)
    encrypted_note = base64.b64encode(iv + ciphertext).decode('utf-8')
    return f"{encrypted_note}::{purpose}"

def decrypt_note(ciphertext_b64):
    ciphertext = base64.b64decode(ciphertext_b64)
    iv = ciphertext[:AES.block_size]
    cipher = AES.new(key, AES.MODE_CBC, iv)
    plaintext = cipher.decrypt(ciphertext[AES.block_size:])
    return plaintext.decode('utf-8')
