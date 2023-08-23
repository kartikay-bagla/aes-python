import numpy as np
from aes_encryption.constants import AES_Type
from aes_encryption.utils.key_generator import get_round_keys
from aes_encryption.utils.round_utils import (
    add_round_key,
    inv_mix_columns,
    inv_shift_rows,
    mix_columns,
    shift_rows,
)
from aes_encryption.utils.s_box_mapping import inv_sub_bytes, sub_bytes


def encrypt_block(
    plain_text: np.ndarray, key: np.ndarray, aes_type: AES_Type
) -> np.ndarray:
    assert plain_text.shape == (4, 4)
    state = plain_text.copy()
    assert key.shape == (aes_type.value.key_length, 4)
    num_rounds = aes_type.value.num_round_keys
    round_keys = get_round_keys(key, aes_type).reshape((num_rounds, 4, 4))

    # first round
    add_round_key(state, round_keys[0])

    # rounds 2 to n-1
    for i in range(1, num_rounds - 1):
        sub_bytes(state)
        shift_rows(state)
        mix_columns(state)
        add_round_key(state, round_keys[i])

    # last round
    sub_bytes(state)
    shift_rows(state)
    add_round_key(state, round_keys[-1])

    return state


def decrypt_block(
    cipher_text: np.ndarray, key: np.ndarray, aes_type: AES_Type
) -> np.ndarray:
    assert cipher_text.shape == (4, 4)
    state = cipher_text.copy()
    assert key.shape == (aes_type.value.key_length, 4)
    num_rounds = aes_type.value.num_round_keys
    round_keys = get_round_keys(key, aes_type).reshape((num_rounds, 4, 4))

    # first round
    add_round_key(state, round_keys[-1])

    # rounds 2 to n-1
    for i in range(num_rounds - 2, 0, -1):
        inv_shift_rows(state)
        inv_sub_bytes(state)
        add_round_key(state, round_keys[i])
        inv_mix_columns(state)

    # last round
    inv_shift_rows(state)
    inv_sub_bytes(state)
    add_round_key(state, round_keys[0])

    return state
