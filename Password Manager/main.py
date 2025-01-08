from cryptography.fernet import Fernet
import os
import json

# Generate and save a key
def generate_key():
    return Fernet.generate_key()

# Load the key
def load_key():
    return open("key.key", "rb").read()

# Save the key to a file
def save_key(key):
    with open("key.key", "wb") as key_file:
        key_file.write(key)

# Encrypt the password
def encrypt_password(password, key):
    f = Fernet(key)
    encrypted_password = f.encrypt(password.encode())
    return encrypted_password

# Decrypt the password
def decrypt_password(encrypted_password, key):
    f = Fernet(key)
    decrypted_password = f.decrypt(encrypted_password).decode()
    return decrypted_password

# Save passwords to a file
def save_passwords(passwords):
    with open("passwords.json", "w") as file:
        json.dump(passwords, file, indent=4)

# Load passwords from a file
def load_passwords():
    if os.path.exists("passwords.json"):
        with open("passwords.json", "r") as file:
            return json.load(file)
    return {}

# Main program
def main():
    # Check if the key file exists, if not, generate one
    if not os.path.exists("key.key"):
        key = generate_key()
        save_key(key)
    else:
        key = load_key()

    print("Welcome to the Password Manager!")
    while True:
        choice = input("\n1. Add Password\n2. View Passwords\n3. Exit\nChoose an option: ")
        
        if choice == "1":
            website = input("Enter the website: ")
            username = input("Enter your username: ")
            password = input("Enter your password: ")
            
            # Encrypt the password
            encrypted_password = encrypt_password(password, key)
            
            # Load existing passwords or create an empty dictionary
            passwords = load_passwords()
            
            # Save the new password
            passwords[website] = {
                "username": username,
                "password": encrypted_password.decode()  # Store as a string
            }
            
            # Save updated password list to file
            save_passwords(passwords)
            print(f"Password for {website} saved successfully!")
        
        elif choice == "2":
            passwords = load_passwords()
            if not passwords:
                print("No passwords saved.")
            else:
                for website, info in passwords.items():
                    decrypted_password = decrypt_password(info["password"].encode(), key)
                    print(f"Website: {website}")
                    print(f"Username: {info['username']}")
                    print(f"Password: {decrypted_password}\n")
        
        elif choice == "3":
            print("Exiting password manager.")
            break
        else:
            print("Invalid option. Please choose again.")

if __name__ == "__main__":
    main()
