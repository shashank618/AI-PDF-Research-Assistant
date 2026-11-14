
from app.services.security import hash_password, verify_password


# Original password
password = "MySecurePassword123"

# Generate password hash
hashed_password = hash_password(password)

print("Original Password:", password)
print("Hashed Password:", hashed_password)

# Verify correct password
print("\nCorrect password:", verify_password(
    password,
    hashed_password
))

# Verify incorrect password
print("Incorrect password:", verify_password(
    "WrongPassword123",
    hashed_password
))
