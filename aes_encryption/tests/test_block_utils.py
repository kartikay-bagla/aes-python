import numpy as np


def test_encrypt_decrypt_block():
    from ..constants import AES_Type
    from ..utils.block_utils import decrypt_block, encrypt_block

    plain_text = np.array(
        list("Two One Nine Two".encode(encoding="ascii")), dtype=np.uint8
    ).reshape((4, 4))
    key = np.array(
        list("Thats my Kung Fu".encode(encoding="ascii")), dtype=np.uint8
    ).reshape((4, 4))

    cipher_text = encrypt_block(
        plain_text=plain_text,
        key=key,
        aes_type=AES_Type.AES_128,
    )

    decrypted_text = decrypt_block(cipher_text, key, AES_Type.AES_128)

    assert (plain_text == decrypted_text).all()
