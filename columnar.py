def encrypt(plaintext, key):
    # Remove spaces from key and plaintext for uniformity, convert to uppercase
    key = key.replace(" ", "").upper()
    plaintext = plaintext.replace(" ", "").upper()
    
    # Convert key to numbers based on alphabetical order, considering repeating characters like "T" in "test"
    # Sort first, sorted list determines left to right key sequence integer
    key_order = sorted(list(key))
    key_sequence = []
    
    print(key_order)
    print(key_sequence)
    
    for char in key:
        # take index from base key, not sorted key
        index = key_order.index(char)
        key_sequence.append(index)
        key_order[index] = "/"  # Replace used char to handle repeats correctly
        
        print(key_order)
        print(key_sequence)
    
    # Create the grid for plaintext input
    columns = len(key)
    # "//"" is floor division or round down, if plaintext length / columns = 0, add 1 else 0
    rows = len(plaintext) // columns + (1 if len(plaintext) % columns else 0)
    grid = [['X' for _ in range(columns)] for _ in range(rows)]  # Fill with placeholder 'X' for all empty cells
    # print(grid)
    
    # Fill the grid with plaintext
    for i, char in enumerate(plaintext):
        # from enumerated plaintext, i = index#, char = char from text
        row = i // columns # rounding down ensures that only complete rows are counted, from 0 onwards.
        col = i % columns # wraps the index around within the bounds of the number of columns
        grid[row][col] = char
        # print(grid)
    
    # Encrypt by reading columns in key sequence order
    encrypted_text = ""
    for num in sorted(set(key_sequence)): #sorts the new key sequence set [2 0 1 3] becomes [0 1 2 3] so that left to right starts from 0
        for col in [i for i, x in enumerate(key_sequence) if x == num]: 
        #For each index-value pair produced by enumerating key_sequence, include the index# (i) in a new LIST for columns that should be read next if the value (x) matches the current num. Here, first column to be read "0" is at index 1 so i = 1, x = 0.
            print([i for i, x in enumerate(key_sequence) if x == num])
            for row in range(rows): #read all rows from selected column, write into encrypted_text
                encrypted_text += grid[row][col]
    
    return encrypted_text

def decrypt(message, key):
    # Placeholder for decryption logic
    return "Decrypted with Vigenere: " + message
