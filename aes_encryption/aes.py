import numpy as np

from aes_encryption.constants.aes_constants import AES_Type
from aes_encryption.utils.block_utils import encrypt_block, decrypt_block


def encrypt(input_string: bytes, key: bytes, aes_type: AES_Type) -> bytes:
    assert len(key) == aes_type.value.key_length * 4
    padding_required = 16 - len(input_string) % 16
    if padding_required != 0:
        input_string += bytes([0] * padding_required)

    input_array = np.array(list(input_string), dtype=np.uint8).reshape((-1, 4, 4))
    key_numpy = np.array(list(key), dtype=np.uint8).reshape(
        (aes_type.value.key_length, 4)
    )

    cipher_text = np.zeros_like(input_array, dtype=np.uint8)
    for i, block in enumerate(input_array):
        cipher_text[i] = encrypt_block(block, key_numpy, aes_type)

    return cipher_text.tobytes() + np.array(padding_required).astype(np.uint8).tobytes()


def decrypt(cipher_text: bytes, key: bytes, aes_type: AES_Type) -> bytes:
    assert len(key) == aes_type.value.key_length * 4

    padded_bytes = int(cipher_text[-1])
    cipher_text_numpy = np.array(list(cipher_text[:-1]), dtype=np.uint8).reshape(
        (-1, 4, 4)
    )
    key_numpy = np.array(list(key), dtype=np.uint8).reshape(
        (aes_type.value.key_length, 4)
    )

    plain_text = np.zeros_like(cipher_text_numpy, dtype=np.uint8)
    for i, block in enumerate(cipher_text_numpy):
        plain_text[i] = decrypt_block(block, key_numpy, aes_type)

    return plain_text.tobytes()[:-padded_bytes]
