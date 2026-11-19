"""Transferência exploratória do modificador nutricional proposto por Bown et al. (2013).

A equação foi ajustada para Pinus radiata na Nova Zelândia. Sua aplicação a
Eucalyptus no Brasil é uma hipótese de transferência, não uma calibração validada.
"""
from __future__ import annotations

import numpy as np


def fN_bown(N_pct, cn_ratio) -> np.ndarray:
    """Calcula a predição publicada de fN, sem truncar valores extrapolados.

    N_pct é nitrogênio total do solo em porcentagem numérica (por exemplo, 0.2
    significa 0,2%); cn_ratio é a razão C:N adimensional. Bown et al. mediram
    ambos no solo mineral de 0-10 cm.
    """
    nitrogen = np.asarray(N_pct)
    ratio = np.asarray(cn_ratio)
    for name, values in (("N_pct", nitrogen), ("cn_ratio", ratio)):
        if not np.issubdtype(values.dtype, np.number) or np.issubdtype(
            values.dtype, np.complexfloating
        ):
            raise TypeError(f"fN_bown: {name} deve ser numérico.")
    if nitrogen.size != ratio.size:
        raise ValueError("fN_bown: N_pct e cn_ratio devem ter o mesmo comprimento.")

    nitrogen = nitrogen.astype(float, copy=False).reshape(-1)
    ratio = ratio.astype(float, copy=False).reshape(-1)
    for name, values in (("N_pct", nitrogen), ("cn_ratio", ratio)):
        if np.any(values < 0):
            raise ValueError(f"fN_bown: {name} não pode ser negativo.")
        if np.any(~np.isfinite(values) & ~np.isnan(values)):
            raise ValueError(f"fN_bown: {name} deve ser finito ou NaN.")

    result = np.full(nitrogen.size, np.nan, dtype=float)
    valid = ~np.isnan(nitrogen) & ~np.isnan(ratio)
    result[valid] = 1.32 + 0.99 * nitrogen[valid] - 0.04 * ratio[valid]
    return result.reshape(np.asarray(N_pct).shape)
