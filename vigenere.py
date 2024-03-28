def encrypt(plaintext, key):
    encrypted_text = ""
    key_index = 0
    key_length = len(key)
    key = key.upper()
    plaintext = plaintext.upper() 
    
    key_as_int = [ord(i) - ord('A') for i in key]  # Normalize key: A=0, B=1, ...

    for char in plaintext:
        if char.isalpha():  # Encrypt ONLY alphabetic characters!!!
            char_code = ord(char) - ord('A')
            # Normalizing to alphabetical index by "- 65" or "ord('A')"
            # Encryption formula: (plaintext_char + key_char) mod 26
            value = (char_code + key_as_int[key_index % key_length]) % 26
            # (%)modulo key_length so that it repeats back to first char when key is shorter than plaintext ex: 4%4 = 0
            encrypted_char = chr(value + ord('A'))
            #adding "+ 65" via ord('A') to convert back to Uppercase ASCII
            encrypted_text += encrypted_char
            key_index += 1  # Advance key index ONLY if char was alphabetic!!!
        else:
            encrypted_text += char  # Non-alphabetic characters are appended as is

    return encrypted_text

def decrypt(ciphertext, key):
    decrypted_text = ""
    key_index = 0
    key_length = len(key)
    key = key.upper()
    ciphertext = ciphertext.upper()
    
    key_as_int = [ord(i) - ord('A') for i in key]  # Normalize key: A=0, B=1, ...

    for char in ciphertext:
        if char.isalpha():  # Decrypt only alphabetic characters
            char_code = ord(char) - ord('A')
            # Normalizing to alphabetical index by "- 65" or "ord('A')"
            # Decryption formula: (ciphertext_char - key_char + 26) % 26
            value = (char_code - key_as_int[key_index % key_length] + 26) % 26
            # (%)modulo key_length so that it repeats back to first char when key is shorter than plaintext ex: 4%4 = 0
            decrypted_char = chr(value + ord('A'))
            decrypted_text += decrypted_char
            key_index += 1  # Advance key index ONLY if char was alphabetic!!!
        else:
            decrypted_text += char  # Non-alphabetic characters are appended as is

    return decrypted_text
