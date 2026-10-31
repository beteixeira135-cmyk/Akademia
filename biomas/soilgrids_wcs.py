"""Textura SoilGrids 2.0 (Poggio et al., 2021) por WCS (maps.isric.org), 6 camadas 0–200 cm, em 8 pontos a
±0,08° (~9 km) da sede (grade 3×3 sem o centro), mesmo desenho usado para Imperatriz. Unidade WCS: g/kg -> %.
CAD 0–2 m = Σ AD_PTF-ZARC(camada) × espessura."""
import sys, io, json, time, urllib.request
import numpy as np, tifffile
sys.path.insert(0, __file__.rsplit("/", 1)[0]); from ptf_zarc import ad_mm_cm
CAM = [("0-5cm", 0, 5), ("5-15cm", 5, 15), ("15-30cm", 15, 30), ("30-60cm", 30, 60), ("60-100cm", 60, 100), ("100-200cm", 100, 200)]
def valor(prop, prof, lon, lat, d=0.003):
    url = (f"https://maps.isric.org/mapserv?map=/map/{prop}.map&SERVICE=WCS&VERSION=2.0.1&REQUEST=GetCoverage"
           f"&COVERAGEID={prop}_{prof}_mean&FORMAT=image/tiff&SUBSET=long({lon-d},{lon+d})&SUBSET=lat({lat-d},{lat+d})"
           "&SUBSETTINGCRS=http://www.opengis.net/def/crs/EPSG/0/4326&OUTPUTCRS=http://www.opengis.net/def/crs/EPSG/0/4326")
    for t in range(4):
        try:
            a = tifffile.imread(io.BytesIO(urllib.request.urlopen(url, timeout=90).read())).astype(float)
            a = a[(a > 0) & (a < 1000)]
            return float(np.median(a)) / 10 if a.size else None
        except Exception as e:
            time.sleep(5)
    return None
def sitio(cod, lon0, lat0):
    out = []
    for i, dx in enumerate([-0.08, 0, 0.08]):
        for j, dy in enumerate([-0.08, 0, 0.08]):
            if dx == 0 and dy == 0: continue
            lon, lat = round(lon0 + dx, 4), round(lat0 + dy, 4); cam = []
            for prof, a, b in CAM:
                v = {p: valor(p, prof, lon, lat) for p in ("clay", "sand", "silt")}
                cam.append(dict(prof=prof, top=a, bot=b, **v))
            ok = all(None not in (c["clay"], c["sand"], c["silt"]) for c in cam)
            asw = sum(ad_mm_cm(c["sand"], c["silt"], c["clay"]) * (c["bot"] - c["top"]) for c in cam) if ok else None
            out.append(dict(sitio=cod, lon=lon, lat=lat, camadas=cam, asw=asw))
            print(cod, lon, lat, None if asw is None else round(asw, 1), [c["clay"] for c in cam], flush=True)
    return out
if __name__ == "__main__":
    res = sitio(sys.argv[1], float(sys.argv[2]), float(sys.argv[3]))
    json.dump(res, open(f"/home/claude/tcc/solos_fontes/soilgrids_wcs_{sys.argv[1]}.json", "w"), indent=1)
