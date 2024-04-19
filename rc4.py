def rc4_key_setup(key):
    S = list(range(256))
    j = 0
    for i in range(256):
        j = (j + S[i] + key[i % len(key)]) % 256
        S[i], S[j] = S[j], S[i]
    return S

def rc4_keystream(S, data_length):
    i = 0
    j = 0
    keystream = []
    for _ in range(data_length):
        i = (i + 1) % 256
        j = (j + S[i]) % 256
        S[i], S[j] = S[j], S[i]
        k = S[(S[i] + S[j]) % 256]
        keystream.append(k)
    return keystream

def encrypt(data, key):
    try:
        key_bytes = bytes.fromhex(key)  # Convert hexadecimal key to bytes
    except ValueError:
        print("Error: Key must be a valid hexadecimal string.")
        return None  # Return None if key format is invalid

    data_bytes = data.encode('utf-8')  # Convert data to bytes
    S = rc4_key_setup(key_bytes)
    keystream = rc4_keystream(S, len(data_bytes))
    encrypted_data = [data_byte ^ keystream_byte for data_byte, keystream_byte in zip(data_bytes, keystream)]
    encrypted_hex = ''.join(f'{byte:02x}' for byte in encrypted_data)  # Convert bytes to hexadecimal string
    return encrypted_hex

def decrypt(data, key):
    try:
        key_bytes = bytes.fromhex(key)  # Convert hexadecimal key to bytes
    except ValueError:
        print("Error: Key must be a valid hexadecimal string.")
        return None  # Return None if key format is invalid

    data_bytes = bytes.fromhex(data)  # Convert hexadecimal string to bytes
    S = rc4_key_setup(key_bytes)
    keystream = rc4_keystream(S, len(data_bytes))
    decrypted_data = bytes([data_byte ^ keystream_byte for data_byte, keystream_byte in zip(data_bytes, keystream)])
    return decrypted_data.decode('utf-8', errors='replace')  # Replace invalid bytes with '?'