import numpy as np


def test_shift_rows():
    from ..utils.round_utils import inv_shift_rows, shift_rows

    start = np.arange(16, dtype=np.uint8).reshape(4, 4)
    shifted = shift_rows(state=start, inplace=False)
    end = inv_shift_rows(state=shifted, inplace=False)

    assert (start == end).all()


def test_add_round_key():
    from ..utils.round_utils import add_round_key

    start = np.arange(16, dtype=np.uint8).reshape(4, 4)
    key = np.arange(16, dtype=np.uint8).reshape(4, 4)
    added = add_round_key(state=start, key=key, inplace=False)
    end = add_round_key(state=added, key=key, inplace=False)

    assert (start == end).all()


def test_mix_columns():
    from ..utils.round_utils import inv_mix_columns, mix_columns

    start = np.arange(16, dtype=np.uint8).reshape(4, 4)
    mixed = mix_columns(state=start, inplace=False)
    end = inv_mix_columns(state=mixed, inplace=False)

    assert (start == end).all()


def test_multiple_ops():
    from ..utils.round_utils import (
        add_round_key,
        inv_mix_columns,
        inv_shift_rows,
        mix_columns,
        shift_rows,
    )

    start = np.arange(16, dtype=np.uint8).reshape(4, 4)
    key = np.arange(16, dtype=np.uint8).reshape(4, 4)

    state = start.copy()

    mix_columns(state)
    add_round_key(state, key)
    shift_rows(state)

    inv_shift_rows(state)
    add_round_key(state, key)
    inv_mix_columns(state)

    assert (start == state).all()
