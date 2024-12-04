import hashlib

def audible_hash(activation_bytes):
    fixed_key = bytes.fromhex('77214d4b196a87cd520045fd20a51d67')
    sha = hashlib.sha1()
    sha.update(fixed_key)
    sha.update(activation_bytes)
    intermediate_key = sha.digest()

    sha = hashlib.sha1()
    sha.update(fixed_key)
    sha.update(intermediate_key)
    sha.update(activation_bytes)
    intermediate_iv = sha.digest()

    sha = hashlib.sha1()
    sha.update(intermediate_key[:16])
    sha.update(intermediate_iv[:16])
    calculated_checksum = sha.digest()

    return calculated_checksum
