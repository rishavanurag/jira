import bcrypt


def hash_password(plain_password: str) -> str:
    """
    Takes a plain text password, adds a random salt,
    hashes it, and returns a safe text string for the database.
    """
    # 1. Convert the plain text password into raw bytes
    password_bytes = plain_password.encode("utf-8")

    # 2. Generate a unique, random salt automatically
    salt = bcrypt.gensalt()

    # 3. Mix the password and salt together to create the hash bytes
    hashed_bytes = bcrypt.hashpw(password_bytes, salt)

    # 4. Turn the hash bytes back into a standard text string
    return hashed_bytes.decode("utf-8")


def verify_password(plain_password: str, stored_hash: str) -> bool:
    """
    Compares a typed password with the stored hash string.
    Returns True if they match, or False if they do not.
    """
    # 1. Convert the typed password into raw bytes
    password_bytes = plain_password.encode("utf-8")

    # 2. Convert the stored database hash string back into bytes
    hash_bytes = stored_hash.encode("utf-8")

    # 3. Check if they match (Bcrypt automatically finds the salt inside)
    return bcrypt.checkpw(password_bytes, hash_bytes)

