"""Estrutura para estimar fertilidade a partir de C e B do solo.

A forma funcional e os coeficientes ainda não estão disponíveis; por isso, este
módulo não estima fN e não altera o comportamento padrão do 3-PG.
"""
from __future__ import annotations

import warnings
from collections.abc import Mapping

import numpy as np


FN_COEF = None


def fN_forma(C: np.ndarray, B: np.ndarray, coef: Mapping) -> np.ndarray:
    """Ponto reservado à forma funcional, a definir quando houver fonte verificável."""
    raise NotImplementedError(
        "A forma funcional de fN para carbono e boro ainda não foi definida."
    )


def fN_soil(C, B, coef=FN_COEF) -> np.ndarray:
    """Retorna fN em [0, 1]; sem forma e coeficientes, retorna NaN e avisa.

    C e B devem ser vetores numéricos de mesmo comprimento, em unidades
    previamente harmonizadas. Entradas NaN permanecem NaN.
    """
    c = np.asarray(C)
    b = np.asarray(B)
    for nome, valores in (("C", c), ("B", b)):
        if not np.issubdtype(valores.dtype, np.number) or np.issubdtype(
            valores.dtype, np.complexfloating
        ):
            raise TypeError(f"fN_soil: {nome} deve ser numérico.")
    if c.size != b.size:
        raise ValueError("fN_soil: C e B devem ter o mesmo comprimento.")

    c = c.astype(float, copy=False).reshape(-1)
    b = b.astype(float, copy=False).reshape(-1)
    if np.any((c < 0) | (b < 0)):
        raise ValueError("fN_soil: teores de C e B não podem ser negativos.")
    if np.any(~np.isfinite(c) & ~np.isnan(c)) or np.any(
        ~np.isfinite(b) & ~np.isnan(b)
    ):
        raise ValueError("fN_soil: teores de C e B devem ser finitos ou NaN.")

    out = np.full(c.size, np.nan, dtype=float)
    valid = ~np.isnan(c) & ~np.isnan(b)
    if not np.any(valid):
        return out.reshape(np.asarray(C).shape)

    if coef is None or len(coef) == 0:
        warnings.warn(
            "fN_soil: forma funcional e coeficientes não disponíveis; retornando NaN.",
            RuntimeWarning,
            stacklevel=2,
        )
        return out.reshape(np.asarray(C).shape)

    estimate = np.asarray(fN_forma(c[valid], b[valid], coef), dtype=float)
    if estimate.size != int(valid.sum()):
        raise ValueError("fN_soil: a forma funcional retornou comprimento inesperado.")
    if not np.all(np.isfinite(estimate)):
        raise ValueError("fN_soil: a forma funcional deve retornar valores finitos.")
    out[valid] = np.clip(estimate.reshape(-1), 0.0, 1.0)
    return out.reshape(np.asarray(C).shape)


def species_with_soil_fertility(
    species: Mapping,
    C,
    B,
    *,
    enabled: bool = False,
    coef=FN_COEF,
) -> dict:
    """Copia a espécie e, se habilitado, substitui `fertility` pelo fN do sítio.

    O dicionário retornado pode ser passado a `run_3pg_pjs`. O modo padrão
    preserva a fertilidade manual existente sem modificar o dicionário original.
    """
    updated = dict(species)
    if not enabled:
        return updated

    modifier = fN_soil(C, B, coef)
    if modifier.size != 1 or not np.isfinite(modifier.item()):
        raise ValueError(
            "fN indisponível para este sítio; mantenha a fertility manual."
        )
    updated["fertility"] = float(modifier.item())
    return updated
