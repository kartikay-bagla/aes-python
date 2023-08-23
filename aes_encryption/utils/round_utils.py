from typing import Optional
import numpy as np

from aes_encryption.utils.math import galois_multiplication as gmul


def get_array_for_str(string: str) -> np.ndarray:
    """Get array for an ascii string.

    :param string: Input string. Must be all ascii characters. And of length 16.
    :type string: str
    :return: Numpy array (4x4, uint8).
    :rtype: np.ndarray
    """
    assert len(string) == 16
    ords = [ord(char) for char in string]
    for num in ords:
        if num > 255:
            raise ValueError(f"Char `{chr(num)}` in string is not valid ASCII.")
    return np.array(ords, dtype=np.uint8).reshape((4, 4))


def add_round_key(
    state: np.ndarray, key: np.ndarray, inplace: bool = True
) -> Optional[np.ndarray]:
    """Add round key to state.

    Length of state and key must be same.
    :param state: State to add round key to, must be a 4x4, uint8 ndarray
    :type state: np.ndarray
    :param key: Round key, must be a 4x4, uint8 ndarray
    :type key: bytes
    :param inplace: Whether to do inplace addition, defaults to True
    :type inplace: bool, optional
    :return: State with round key added
    :rtype: np.ndarray
    """
    if inplace:
        state ^= key
        return None
    else:
        return state ^ key


def shift_rows(state: np.ndarray, inplace: bool = True) -> Optional[np.ndarray]:
    """Shift each row by its index.

    :param state: State to shift rows in
    :type state: ndarray
    :param inplace: Whether to do inplace shifting, defaults to True
    :type inplace: bool, optional
    :return: State with shifted rows
    :rtype: np.ndarray
    """
    if inplace:
        for i in range(len(state)):
            state[i] = np.roll(state[i], -i)
        return None
    else:
        return np.array(
            [np.roll(row, -i) for i, row in enumerate(state)], dtype=state.dtype
        )


def inv_shift_rows(state: np.ndarray, inplace: bool = True) -> Optional[np.ndarray]:
    """Shift each row by its index.

    :param state: State to shift rows in
    :type state: ndarray
    :param inplace: Whether to do inplace shifting, defaults to True
    :type inplace: bool, optional
    :return: State with shifted rows
    :rtype: np.ndarray
    """
    if inplace:
        for i in range(len(state)):
            state[i] = np.roll(state[i], i)
        return None
    else:
        return np.array(
            [np.roll(row, i) for i, row in enumerate(state)], dtype=state.dtype
        )


def mix_columns(state: np.ndarray, inplace: bool = True) -> Optional[np.ndarray]:
    """Mix columns of state.

    :param state: State to mix columns in, must be a 4x4, uint8 ndarray
    :type state: np.ndarray
    :param inplace: Whether to do inplace mixing, defaults to True
    :type inplace: bool, optional
    :return: State with mixed columns
    :rtype: np.ndarray
    """
    out = np.zeros_like(state)
    for i in range(len(out)):
        out[i, 0] = np.array(
            gmul(2, state[i, 0]) ^ gmul(3, state[i, 1]) ^ state[i, 2] ^ state[i, 3]
        ).astype(np.uint8)
        out[i, 1] = np.array(
            state[i, 0] ^ gmul(2, state[i, 1]) ^ gmul(3, state[i, 2]) ^ state[i, 3]
        ).astype(np.uint8)
        out[i, 2] = np.array(
            state[i, 0] ^ state[i, 1] ^ gmul(2, state[i, 2]) ^ gmul(3, state[i, 3])
        ).astype(np.uint8)
        out[i, 3] = np.array(
            gmul(3, state[i, 0]) ^ state[i, 1] ^ state[i, 2] ^ gmul(2, state[i, 3])
        ).astype(np.uint8)
    if inplace:
        state[:] = out
        return None
    else:
        return out


def inv_mix_columns(state: np.ndarray, inplace: bool = True) -> Optional[np.ndarray]:
    """Mix columns of state.

    :param state: State to mix columns in, must be a 4x4, uint8 ndarray
    :type state: np.ndarray
    :param inplace: Whether to do inplace mixing, defaults to True
    :type inplace: bool, optional
    :return: State with mixed columns
    :rtype: np.ndarray
    """
    out = np.zeros_like(state)
    for i in range(len(out)):
        out[i, 0] = np.array(
            gmul(0x0E, state[i, 0])
            ^ gmul(0x0B, state[i, 1])
            ^ gmul(0x0D, state[i, 2])
            ^ gmul(0x09, state[i, 3])
        ).astype(np.uint8)
        out[i, 1] = np.array(
            gmul(0x09, state[i, 0])
            ^ gmul(0x0E, state[i, 1])
            ^ gmul(0x0B, state[i, 2])
            ^ gmul(0x0D, state[i, 3])
        ).astype(np.uint8)
        out[i, 2] = np.array(
            gmul(0x0D, state[i, 0])
            ^ gmul(0x09, state[i, 1])
            ^ gmul(0x0E, state[i, 2])
            ^ gmul(0x0B, state[i, 3])
        ).astype(np.uint8)
        out[i, 3] = np.array(
            gmul(0x0B, state[i, 0])
            ^ gmul(0x0D, state[i, 1])
            ^ gmul(0x09, state[i, 2])
            ^ gmul(0x0E, state[i, 3])
        ).astype(np.uint8)
    if inplace:
        state[:] = out
        return None
    else:
        return out
