import numpy as np


def test_sub_bytes_mapping():
    from ..utils.s_box_mapping import sub_bytes, inv_sub_bytes

    start = np.arange(16, dtype=np.uint8).reshape(4, 4)
    subbed = sub_bytes(state=start, inplace=False)
    end = inv_sub_bytes(state=subbed, inplace=False)

    assert (start == end).all()
