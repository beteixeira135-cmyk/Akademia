"""PTF-ZARC (Teixeira et al., 2021, Equação 9): água disponível AD (mm cm-1) a partir de areia total (AT),
silte (SIL) e argila (ARG), em %. CAD 0–2 m = AD × 200 cm."""
def ad_mm_cm(at, sil, arg):
    x = (-0.02128887 * at - 0.01005814 * sil - 0.01901894 * arg + 0.0001171219 * at * sil
         + 0.0002073924 * at * arg + 0.00006118707 * sil * arg - 0.000006373789 * at * sil * arg)
    return (1 + 0.35941 * x) ** 2.78474 * 10
def cad_2m(at, sil, arg):
    return ad_mm_cm(at, sil, arg) * 200
if __name__ == "__main__":
    # conferência com SOLOS_LOCAIS.md: TECHS 22 (21/23/56) -> 213 mm; TECHS 9 (11/9/80) -> 160 mm
    print(round(cad_2m(21, 23, 56)), round(cad_2m(11, 9, 80)))
