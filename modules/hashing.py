import hashlib

def calculate_hash(filepath):

    sha256 = hashlib.sha256()

    try:

        with open(filepath, "rb") as f:

            while True:

                data = f.read(4096)

                if not data:
                    break

                sha256.update(data)

        return sha256.hexdigest()

    except Exception as e:

        return f"ERROR: {str(e)}"


def verify_integrity(old_hash, new_hash):

    """
    Compare two SHA256 hashes.
    """

    if old_hash == new_hash:
        return "PASS"

    return "FAIL"
