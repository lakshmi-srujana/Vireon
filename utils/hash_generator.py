import hashlib

full_name = input("Enter Student Name: ")
roll_no = input("Enter Roll Number: ")

# Generate automatic password
raw_password = (
    full_name.split()[0].lower()
    + "@"
    + roll_no
)

# Hash password
hashed_password = hashlib.sha256(
    raw_password.encode()
).hexdigest()

print("\nGenerated Password:")
print(raw_password)

print("\nSHA-256 Hash:")
print(hashed_password)