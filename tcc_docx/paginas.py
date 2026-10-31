import json, re, subprocess, sys
pdf = sys.argv[1]; E = json.load(open("estrutura.json"))
n = int(re.search(r"Pages:\s+(\d+)", subprocess.run(["pdfinfo", pdf], capture_output=True, text=True).stdout).group(1))
T = [subprocess.run(["pdftotext", "-f", str(i), "-l", str(i), "-layout", pdf, "-"], capture_output=True, text=True).stdout for i in range(1, n + 1)]
norm = lambda s: re.sub(r"\s+", " ", s).strip()
ini = next(i for i, t in enumerate(T) if norm(t).startswith("SUMÁRIO")) + 1   # 1ª página textual (índice 0-based)
P = {}
for k, h in enumerate(E["sum"]):
    for i in range(ini, n):
        if any(norm(l) == norm(h) for l in T[i].splitlines()):
            P[f"sum{k}"] = i  # físico (0-based) -> exibido = (i+1) - 1 = i
            break
for kind, tot, lab in [("fig", E["nfig"], "Figura"), ("tab", E["ntab"], "Tabela")]:
    for j in range(1, tot + 1):
        for i in range(ini, n):
            if re.search(rf"^\s*{lab} {j}\. ", T[i], re.M):
                P[f"{kind}{j}"] = i; break
falt = [f"sum{k}" for k in range(len(E["sum"])) if f"sum{k}" not in P] + [f"fig{j}" for j in range(1, E["nfig"] + 1) if f"fig{j}" not in P] + [f"tab{j}" for j in range(1, E["ntab"] + 1) if f"tab{j}" not in P]
json.dump(P, open("paginas.json", "w"), indent=1); print("primeira textual (exibida):", ini, "| faltando:", falt); print(P)
