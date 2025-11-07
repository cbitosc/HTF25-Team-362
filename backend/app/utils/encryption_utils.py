from cryptography.fernet import Fernet
import base64
from app.config import settings


def get_cipher():
    """Get Fernet cipher with encryption key"""
    # Ensure key is properly formatted (32 bytes base64 encoded)
    key = settings.ENCRYPTION_KEY.encode()
    
    # If key is not in base64 format, encode it
    if len(key) < 32:
        key = base64.urlsafe_b64encode(key.ljust(32)[:32])
    
    return Fernet(key)


def encrypt_data(data: str) -> str:
    """Encrypt sensitive data"""
    if not data:
        return data
    
    cipher = get_cipher()
    encrypted = cipher.encrypt(data.encode())
    return encrypted.decode()


def decrypt_data(encrypted_data: str) -> str:
    """Decrypt sensitive data"""
    if not encrypted_data:
        return encrypted_data
    
    cipher = get_cipher()
    decrypted = cipher.decrypt(encrypted_data.encode())
    return decrypted.decode()


def encrypt_dict_fields(data_dict: dict, fields_to_encrypt: list) -> dict:
    """Encrypt specific fields in a dictionary"""
    encrypted_dict = data_dict.copy()
    
    for field in fields_to_encrypt:
        if field in encrypted_dict and encrypted_dict[field]:
            encrypted_dict[field] = encrypt_data(str(encrypted_dict[field]))
    
    return encrypted_dict


def decrypt_dict_fields(data_dict: dict, fields_to_decrypt: list) -> dict:
    """Decrypt specific fields in a dictionary"""
    decrypted_dict = data_dict.copy()
    
    for field in fields_to_decrypt:
        if field in decrypted_dict and decrypted_dict[field]:
            decrypted_dict[field] = decrypt_data(decrypted_dict[field])
    
    return decrypted_dict
