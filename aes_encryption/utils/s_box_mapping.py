from typing import Optional
import numpy as np

from aes_encryption.constants import INV_S_BOX_MAPPING, S_BOX_MAPPING

S_BOX_MAPPING_NUMPY_FN = np.vectorize(S_BOX_MAPPING.get)
INV_S_BOX_MAPPING_NUMPY_FN = np.vectorize(INV_S_BOX_MAPPING.get)


def sub_bytes(state: np.ndarray, inplace: bool = True) -> Optional[np.ndarray]:
    """Substitute each byte in state with S Box.

    :param state: State to substitute bytes in
    :type state: np.ndarray
    :param inplace: Whether to do inplace substitution, defaults to True
    :type inplace: bool, optional
    :return: State with substituted bytes
    :rtype: np.ndarray
    """
    if inplace:
        state[:] = S_BOX_MAPPING_NUMPY_FN(state)
        return None
    else:
        return S_BOX_MAPPING_NUMPY_FN(state)


def inv_sub_bytes(state: np.ndarray, inplace: bool = True) -> Optional[np.ndarray]:
    """Substitute each byte in state with inverse S Box.

    :param state: State to substitute bytes in
    :type state: np.ndarray
    :param inplace: Whether to do inplace substitution, defaults to True
    :type inplace: bool, optional
    :return: State with substituted bytes
    :rtype: np.ndarray
    """
    if inplace:
        state[:] = INV_S_BOX_MAPPING_NUMPY_FN(state)
        return None
    else:
        return INV_S_BOX_MAPPING_NUMPY_FN(state)
