def rc4_key_setup(key):
    key_length = len(key)
    S = list(range(256))
    j = 0
    for i in range(256):
        j = (j + S[i] + ord(key[i % key_length])) % 256
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
    if isinstance(data, str):  # Check if data is a string
        data = data.encode('utf-8')  # Convert string to bytes
    S = rc4_key_setup(key)
    keystream = rc4_keystream(S, len(data))
    encrypted_data = [data_byte ^ keystream_byte for data_byte, keystream_byte in zip(data, keystream)]
    encrypted_hex = ''.join(f'{byte:02x}' for byte in encrypted_data)  # Convert bytes to hexadecimal string
    return encrypted_hex

def decrypt(data, key):
    if isinstance(data, str):  # Check if data is a string (hexadecimal format)
        data = bytes.fromhex(data)  # Convert hexadecimal string to bytes
    S = rc4_key_setup(key)
    keystream = rc4_keystream(S, len(data))
    decrypted_data = bytes([data_byte ^ keystream_byte for data_byte, keystream_byte in zip(data, keystream)])
    return decrypted_data.decode('utf-8', errors='replace')  # Replace invalid bytes with '?'
