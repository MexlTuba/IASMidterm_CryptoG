from vigenere import encrypt as vigenere_encrypt, decrypt as vigenere_decrypt
from columnar import encrypt as columnar_encrypt, decrypt as columnar_decrypt
from aes import encrypt as aes_encrypt, decrypt as aes_decrypt
from des import encrypt as des_encrypt, decrypt as des_decrypt
from rc4 import encrypt as rc4_encrypt, decrypt as rc4_decrypt

def main_menu():
    print("\nIAS 2 Midterm Group Output")
    print("by Berame, Ceniza, Tuba")
    print("BSIT - 3")
    while True:
        print("\nChoose an Encryption/Decryption Algorithm:\n")
        print("1. Vigenere Cipher (PolyAlphabetic - Substitution)")
        print("2. Columnar Cipher (Transposition)")
        print("3. AES")
        print("4. DES")
        print("5. RC4")
        print("6. Exit")
        choice = input("> ")

        if choice == "1":
            cipher_menu("Vigenere Cipher", vigenere_encrypt, vigenere_decrypt)
            
        elif choice == "2":
            cipher_menu("Columnar Cipher", columnar_encrypt, columnar_decrypt)
            
        elif choice == "3":
            cipher_menu("AES", aes_encrypt, aes_decrypt)
            
        elif choice == "4":
            cipher_menu("DES", des_encrypt, des_decrypt)
            
        elif choice == "5":
            cipher_menu("RC4", rc4_encrypt, rc4_decrypt)
            
        elif choice == "6":
            print("Exiting...")
            break
            
        else:
            print("Invalid choice, please try again.")

def cipher_menu(cipher_name, encrypt_func, decrypt_func):
    while True:
        print(f"\n{cipher_name} Menu")
        print("1. Encrypt")
        print("2. Decrypt")
        print("3. Back to Main Menu")
        choice = input("> ")

        if choice == "1":
            message = input("Enter message to encrypt: ")
            key = input("Enter key: ")
            print("Encrypted message:", encrypt_func(message, key))
            
        elif choice == "2":
            message = input("Enter message to decrypt: ")
            key = input("Enter key: ")
            print("Decrypted message:", decrypt_func(message, key))
            
        elif choice == "3":
            return
        
        else:
            print("Invalid choice, please try again.")

if __name__ == "__main__":
    main_menu()
