import base64
import re

Nb = 4 #* Number of Columns
Nk = 4 #* Key Length
Nr = 10

SBOX = [
    0x63, 0x7c, 0x77, 0x7b, 0xf2, 0x6b, 0x6f, 0xc5, 0x30, 0x01, 0x67, 0x2b, 0xfe, 0xd7, 0xab, 0x76, 
    0xca, 0x82, 0xc9, 0x7d, 0xfa, 0x59, 0x47, 0xf0, 0xad, 0xd4, 0xa2, 0xaf, 0x9c, 0xa4, 0x72, 0xc0,
    0xb7, 0xfd, 0x93, 0x26, 0x36, 0x3f, 0xf7, 0xcc, 0x34, 0xa5, 0xe5, 0xf1, 0x71, 0xd8, 0x31, 0x15, 
    0x04, 0xc7, 0x23, 0xc3, 0x18, 0x96, 0x05, 0x9a, 0x07, 0x12, 0x80, 0xe2, 0xeb, 0x27, 0xb2, 0x75, 
    0x09, 0x83, 0x2c, 0x1a, 0x1b, 0x6e, 0x5a, 0xa0, 0x52, 0x3b, 0xd6, 0xb3, 0x29, 0xe3, 0x2f, 0x84, 
    0x53, 0xd1, 0x00, 0xed, 0x20, 0xfc, 0xb1, 0x5b, 0x6a, 0xcb, 0xbe, 0x39, 0x4a, 0x4c, 0x58, 0xcf, 
    0xd0, 0xef, 0xaa, 0xfb, 0x43, 0x4d, 0x33, 0x85, 0x45, 0xf9, 0x02, 0x7f, 0x50, 0x3c, 0x9f, 0xa8,
    0x51, 0xa3, 0x40, 0x8f, 0x92, 0x9d, 0x38, 0xf5, 0xbc, 0xb6, 0xda, 0x21, 0x10, 0xff, 0xf3, 0xd2, 
    0xcd, 0x0c, 0x13, 0xec, 0x5f, 0x97, 0x44, 0x17, 0xc4, 0xa7, 0x7e, 0x3d, 0x64, 0x5d, 0x19, 0x73, 
    0x60, 0x81, 0x4f, 0xdc, 0x22, 0x2a, 0x90, 0x88, 0x46, 0xee, 0xb8, 0x14, 0xde, 0x5e, 0x0b, 0xdb, 
    0xe0, 0x32, 0x3a, 0x0a, 0x49, 0x06, 0x24, 0x5c, 0xc2, 0xd3, 0xac, 0x62, 0x91, 0x95, 0xe4, 0x79,
    0xe7, 0xc8, 0x37, 0x6d, 0x8d, 0xd5, 0x4e, 0xa9, 0x6c, 0x56, 0xf4, 0xea, 0x65, 0x7a, 0xae, 0x08, 
    0xba, 0x78, 0x25, 0x2e, 0x1c, 0xa6, 0xb4, 0xc6, 0xe8, 0xdd, 0x74, 0x1f, 0x4b, 0xbd, 0x8b, 0x8a, 
    0x70, 0x3e, 0xb5, 0x66, 0x48, 0x03, 0xf6, 0x0e, 0x61, 0x35, 0x57, 0xb9, 0x86, 0xc1, 0x1d, 0x9e, 
    0xe1, 0xf8, 0x98, 0x11, 0x69, 0xd9, 0x8e, 0x94, 0x9b, 0x1e, 0x87, 0xe9, 0xce, 0x55, 0x28, 0xdf, 
    0x8c, 0xa1, 0x89, 0x0d, 0xbf, 0xe6, 0x42, 0x68, 0x41, 0x99, 0x2d, 0x0f, 0xb0, 0x54, 0xbb, 0x16
]

INV_SBOX = [0] * 256
for i in range(256):
    INV_SBOX[SBOX[i]] = i #* Since SBOX[x] = y, then INV_SBOX[y] = x
    
#* Round Constant
Rcon = [
    0x01, 0x02, 0x04, 0x08, 0x10, 0x20, 0x40, 0x80, 0x1B, 0x36
]

#* Perform multiplication by x (polynomial of x) in GF(2^8)
def xtime(a): #* Polynomials: Module x^8 + x^4 + x^3 + x +1
    return ((a << 1) ^ 0x1B if a & 0x80 else a << 1) & 0xFF #* Check if the MSB of `a` is within the bounds of the GF(2^8), if not reduce it within the bounds of GF(2^8)

#* Perform Multiplication in GF(2^8).
def gf_multiply(a, b):
    result = 0
    
    for _ in range(8):
        if b & 1: #* Check LSB of `b` 
            result ^= a #* `a` is XORed with the result.
            
        a = xtime(a) #* Multiply `a` by `x`
        b >>= 1 #* Shift `b` one bit to the right.
        
    return result

#* Pair each byte in the `state` with the byte in the `round_key`
def add_round_key(state, round_key):
    return [s ^ rk for s, rk in zip(state, round_key)] #* XOR first elements of state and round key.

#* Apply SubBytes
def substitute_bytes(word):
    return [SBOX[b] for b in word] #* Get the corresponding value in `SBOX`, and create a new list with the substituted values

#* Rotate Word
def rotate_word(word):
    return word[1:] + word[:1] #* Takes the elements from the second byte to the end, concatenate it with the first byte of the word

#* Generate a list of round keys from the cipher key.
def key_expansion(key):
    key_symbols = [key[i:i + 4] for i in range(0, len(key), 4)] #* Break down the key into 32-bit words (4 bytes each)
    
    while len(key_symbols) < Nb * (Nr + 1): #* Loop until `key_symbols` list contains enough 32-bit words for all round keys
        temp = key_symbols[-1] #* Retrieve the last element
        
        if len(key_symbols) % Nk == 0:
            temp_rotated = rotate_word(temp)
            temp_sub = substitute_bytes(temp_rotated)
            temp_sub[0] ^= Rcon[len(key_symbols) // Nk - 1] #* XOR the first byte of the substituted word with a value from the Rcon
            temp = temp_sub
            
        key_symbols.append([a ^ b for a, b in zip(key_symbols[-Nk], temp)]) #* XOR temp with the word `Nk` positions before it in key list, then append result to the key list. 
        #* Repeat until key list has expanded.
        
    return [item for sublist in key_symbols for item in sublist] #* Flatten into a single list of bytes, to be used in the encryption rounds (the same as flatMap in JS)

#*################################ Encryption Logic ##################################*#

def pad_message(message):
    padding_len = 16 - (len(message) % 16) #* Calculate padding length required to make the message length a multiple of 16 bytes
    padding = bytes([padding_len] * padding_len) #* Construct a list where `padding_len` is repeated `padding_len` times, convert list into a `bytes` object
    return message + padding

def mix_columns(state): #* MixColumns using GF(2^8) multiplication.
    for i in range(4):
        col = state[i * 4:(i + 1) * 4] #* Extract the current column from the state, extract one column at a time.
        state[i*4] = gf_multiply(0x02, col[0]) ^ gf_multiply(0x03, col[1]) ^ col[2] ^ col[3] #* Reassign the value of each byte in the column based on the GF(2^8) multiplication
        state[i*4+1] = col[0] ^ gf_multiply(0x02, col[1]) ^ gf_multiply(0x03, col[2]) ^ col[3]
        state[i*4+2] = col[0] ^ col[1] ^ gf_multiply(0x02, col[2]) ^ gf_multiply(0x03, col[3])
        state[i*4+3] = gf_multiply(0x03, col[0]) ^ col[1] ^ col[2] ^ gf_multiply(0x02, col[3])
        
    return state

def shift_rows(state):
    return [
        state[0], state[5], state[10], state[15], #* First row (no shift)
        state[4], state[9], state[14], state[3], #* Second row (one left shift)
        state[8], state[13], state[2], state[7], #* Third row (two left shifts)
        state[12], state[1], state[6], state[11], #* Fourth row (three left shifts)
    ]

def aes_encrypt(plaintext_bytes, key):
    state = list(plaintext_bytes) #* Convert into a list (state matrix)
    expanded_key = key_expansion(key) #* Expand into multiple round keys 

    #* Initial round key addition
    state = add_round_key(state, expanded_key[:16]) #* Add the first 16 bytes of the expanded key with the state matrix

    #* Main rounds
    for i in range(1, 10): #* 1 to 9 Main Rounds
        state = substitute_bytes(state)
        state = shift_rows(state)
        state = mix_columns(state)
        state = add_round_key(state, expanded_key[i * 16:(i + 1) * 16]) #* Selects the specific 16-byte segment of the expanded key to be used as the round key for the current round

    #* Final round (without MixColumns)
    state = substitute_bytes(state)
    state = shift_rows(state)
    state = add_round_key(state, expanded_key[160:176]) #* Use the 160th to the 175th position in the expanded key array

    return bytes(state)

def encrypt_ecb(plaintext, key):
    padded_plaintext = pad_message(plaintext) #* Apply padding to ensure length is a multiple of the block size (16 bytes)
    encrypted_blocks = []
    
    for i in range(0, len(padded_plaintext), 16): #* Iterate through each block of the padded plaintext in steps of 16 bytes
        block = padded_plaintext[i:i + 16] #* Slice 16-byte block from the padded plaintext starting at position `i`
        encrypted_block = aes_encrypt(block, key) #* Encrypt the current block with the given key
        encrypted_blocks.append(encrypted_block) #* Collect and store all the encrypted blocks as they are generated
        
    return b''.join(encrypted_blocks)

def encrypt(message, key):
    #* Convert key from string to bytes
    if isinstance(key, str):
        key = key.encode()
    if len(key) != 16:
        return "Error! Key must be exactly 16 bytes (128 bits) long."
    
    #* Make sure the message is in bytes format
    if isinstance(message, str):
        message = message.encode()
        
    encrypted = encrypt_ecb(message, key)
    base64_encoded = base64.b64encode(encrypted).decode()
    return base64_encoded

#*####################################################################################*#

#*################################ Decryption Logic ##################################*#
def unpad_message(padded_message): #* Remove PKCS#7 padding.
    padding_len = padded_message[-1]        
    return padded_message[:-padding_len]

def inv_mix_columns(state):
    for i in range(4):
        col = state[i * 4:(i + 1) * 4]
        state[i * 4] = gf_multiply(0x0e, col[0]) ^ gf_multiply(0x0b, col[1]) ^ gf_multiply(0x0d, col[2]) ^ gf_multiply(0x09, col[3])
        state[i * 4 + 1] = gf_multiply(0x09, col[0]) ^ gf_multiply(0x0e, col[1]) ^ gf_multiply(0x0b, col[2]) ^ gf_multiply(0x0d, col[3])
        state[i * 4 + 2] = gf_multiply(0x0d, col[0]) ^ gf_multiply(0x09, col[1]) ^ gf_multiply(0x0e, col[2]) ^ gf_multiply(0x0b, col[3])
        state[i * 4 + 3] = gf_multiply(0x0b, col[0]) ^ gf_multiply(0x0d, col[1]) ^ gf_multiply(0x09, col[2]) ^ gf_multiply(0x0e, col[3])
    
    return state

def inv_sub_bytes(state):
    return [INV_SBOX[b] for b in state]

def inv_shift_rows(state):
    return [
        state[0], state[13], state[10], state[7],
        state[4], state[1], state[14], state[11],
        state[8], state[5], state[2], state[15],
        state[12], state[9], state[6], state[3],
    ]
    
def aes_decrypt(ciphertext_bytes, key):
    state = list(ciphertext_bytes)
    expanded_key = key_expansion(key)
    
    #* Reverse the order of round keys for decryption
    expanded_key_reversed = [expanded_key[i * Nb * 4: (i + 1) * Nb * 4] for i in range(Nr + 1)][::-1]
    
    #* Initial AddRoundKey Step (Using the last round key)
    state = add_round_key(state, expanded_key_reversed[0])
    
    #* Main rounds in reverse
    for round in range(1, Nr):
        state = inv_shift_rows(state)
        state = inv_sub_bytes(state)
        state = add_round_key(state, expanded_key_reversed[round])
        
        if round < Nr:  #* InvMixColumns is not applied in the last round
            state = inv_mix_columns(state)

    #* Final Operation        
    state = inv_shift_rows(state)
    state = inv_sub_bytes(state)
    
    #* Final AddRoundKey (using the last key segment after reversal)
    state = add_round_key(state, expanded_key_reversed[-1])
    
    return bytes(state)

def decrypt_ecb(ciphertext, key):
    decrypted_blocks = []
    
    for i in range(0, len(ciphertext), 16):
        block = ciphertext[i: i + 16]
        decrypted_block = aes_decrypt(block, key)
        decrypted_blocks.append(decrypted_block)
        
    decrypted_message = b''.join(decrypted_blocks)
    unpadded_message = unpad_message(decrypted_message)
    
    return unpadded_message

def decrypt(encrypted, key):
    if isinstance(key, str):
        key = key.encode()
    if len(key) != 16:
        return "Error: Key must be exactly 16 bytes (128 bits) long."
    
    #* Encrypted Message Validation
    try:
        #* Check if encrypted input is a properly padded base64 string using regex
        if isinstance(encrypted, str) and re.match('^[A-Za-z0-9+/]+={0,2}$', encrypted) and len(encrypted) % 4 == 0: 
            encrypted = base64.b64decode(encrypted)
        else:
            return "Error: Invalid base64 encoded string."
        
    except Exception as e:
        return f"Decoding error: {str(e)}"

    #* Continue with Decryption
    try:
        decrypted = decrypt_ecb(encrypted, key)
        return decrypted.decode('utf-8')
    except Exception as e:
        return f"Decryption error: {str(e)}"

#*####################################################################################*#