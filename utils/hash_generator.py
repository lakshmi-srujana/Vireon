import hashlib

password = input("Enter password: ")

hashed_password = hashlib.sha256(password.encode()).hexdigest()

print("\nSHA-256 Hash:\n")
print(hashed_password)