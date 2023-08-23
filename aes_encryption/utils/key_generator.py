import numpy as np

from aes_encryption.constants import AES_Type
from aes_encryption.utils.s_box_mapping import sub_bytes


RCON = np.array(
    [
        [0x00, 0x00, 0x00, 0x00],
        [0x01, 0x00, 0x00, 0x00],
        [0x02, 0x00, 0x00, 0x00],
        [0x04, 0x00, 0x00, 0x00],
        [0x08, 0x00, 0x00, 0x00],
        [0x10, 0x00, 0x00, 0x00],
        [0x20, 0x00, 0x00, 0x00],
        [0x40, 0x00, 0x00, 0x00],
        [0x80, 0x00, 0x00, 0x00],
        [0x1B, 0x00, 0x00, 0x00],
        [0x36, 0x00, 0x00, 0x00],
    ],
    dtype=np.uint8,
)


def _rot_word(word: np.ndarray) -> np.ndarray:
    """Rotate word by one byte.

    :param word: Word to rotate
    :type word: np.ndarray
    :return: Rotated word
    :rtype: np.ndarray
    """
    return np.roll(word, -1)


def get_round_keys(
    input_key: np.ndarray,
    aes_type: AES_Type,
) -> np.ndarray:
    """Get round keys from input key.

    :param input_key: Input key, must be a Nx4, uint8 ndarray
    :type input_key: np.ndarray
    :param aes_type: AES type
    :type aes_type: AES_Type
    :return: Round keys, 4x4R, uint8 ndarray
    :rtype: np.ndarray
    """
    N, R = aes_type.value.key_length, aes_type.value.num_round_keys
    assert input_key.shape == (N, 4)
    W = np.zeros((4 * R, 4), dtype=np.uint8)
    W[:N] = input_key
    for i in range(N, 4 * R - 1):
        if i % N == 0:
            W[i] = (
                W[i - N] ^ sub_bytes(_rot_word(W[i - 1]), inplace=False) ^ RCON[i // N]
            )
        elif N > 6 and i % N == 4:
            W[i] = W[i - N] ^ sub_bytes(W[i - 1], inplace=False)
        else:
            W[i] = W[i - N] ^ W[i - 1]
    return W
