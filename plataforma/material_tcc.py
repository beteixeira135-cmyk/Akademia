#!/usr/bin/env python3
"""Monta plataforma/material_tcc.js: o 'Material do TCC' da Akademia, com as tabelas densas do TCC
(extraídas de tcc_docx/gerar.js por extrair_material_tcc.js, sem redigitar números) e dados extras lidos das saídas
(validação cruzada por observação e ganhos por tipo de dano). Rode depois de extrair_material_tcc.js."""
import json
from pathlib import Path
import pandas as pd

A = Path(__file__).resolve().parent; R = A.parent
T = json.load(open(A / "material_tabelas.json"))
VC = pd.read_csv(R / "calibracao/saida/validacao_cruzada_previsoes.csv")
PS = json.load(open(R / "experimentos/saida/possibilidades/resumo_possibilidades.json"))
f1 = lambda x: f"{x:.1f}".replace(".", ",")

vc = dict(titulo="Previsão de cada observação de Bertulio et al. (2008) deixada fora do ajuste (perda, %)",
          cab=["Esquema", "Clone", "Variável", "Observado", "Original", "Calibrado"],
          linhas=[[r.esquema, "urograndis (C5)" if r.material == "C5" else "urocam (A1)", r.variavel, f1(r.observado), f1(r.original), f1(r.calibrado)]
                  for r in VC.itertuples()],
          nota="Calibrado: média preditiva da distribuição a posteriori recalculada sem a observação (k = 5) ou sem o clone (k = 2).")
gt = dict(titulo="Ganho de volume sobre o controle por tipo de dano isolado ou combinado (cenários aptos)",
          cab=["Tipo de dano", "Versão", "Cenários", "Com ganho", "% com ganho", "Maior ganho (%)"],
          linhas=[[k.split(" | ")[0], k.split(" | ")[1], str(v["n"]), str(v["n_ganho"]), f1(v["frac"]), f1(v["ganho_max"])] for k, v in PS["ganho_por_tipo"].items()],
          nota="Ganho: volume do povoamento aos 84 meses maior que o do controle.")
im = dict(titulo="Importância dos fatores no metamodelo do espaço de possibilidades (%)",
          cab=["Fator", "Importância (%)"], linhas=[[k, f1(v)] for k, v in PS["importancia_pct"].items()], nota="Importância por permutação, Random Forest com 5.688 cenários.")

S = [
    ("mt-locais", "Locais, clima e solo", "3.1", "Os seis locais simulados, com o clima de 2015 a 2024 e a água que o solo consegue guardar até 2 m.", [T["clima"]]),
    ("mt-materiais", "Materiais genéticos", "3.3", "Os números que distinguem cada clone no modelo. O A1 é o principal; os de Borges (2009) servem de comparação.", [T["materiais"]]),
    ("mt-verificacao", "Verificação do código", "4.1", "Comparação, variável por variável, entre o código deste trabalho e o r3PG original. R² = 1 e erro próximo de zero significam que os dois dão o mesmo resultado.", [T["verificacao"]]),
    ("mt-controles", "Crescimento sem desfolha", "4.1", "O que cada material produz em cada local quando não há ataque, e a comparação com medições da rede TECHS.", [T["controles"]]),
    ("mt-perdas", "Perdas por intensidade, frequência e época", "4.2", "A tabela completa por trás dos gráficos de perda: cada combinação de local, material, intensidade e calendário.", [T["principal"]]),
    ("mt-solo", "Efeito da água e da fertilidade", "4.2", "Média e amplitude da perda entre os 16 cenários de solo. A variação é pequena perto do efeito da intensidade e da frequência.", [T["materialclima"]]),
    ("mt-rf", "Metamodelo Random Forest", "4.3", "Quanto o metamodelo acerta a perda simulada em cada forma de validação cruzada. Deixar um local de fora é o teste mais duro.", [T["rf"]]),
    ("mt-bertulio", "Bertulio et al. (2008) e calibração", "4.4", "Perdas observadas no experimento de Campo Verde-MT e simuladas pelas duas versões do módulo.", [T["bertulio"], T["calibracao"]]),
    ("mt-vc", "Validação cruzada da calibração", "4.4", "Cada observação foi escondida do ajuste e depois prevista. Erro menor na versão calibrada significa que a compensação prevê bem dentro desse experimento.", [T["validacaocruzada"], vc]),
    ("mt-danos", "Outros danos de pragas e doenças", "4.5", "Perda de volume para cada agente do catálogo, com a fonte de cada magnitude.", [T["danos"]]),
    ("mt-biomas", "Resposta nos biomas", "4.5", "Produtividade e perda com 50% de desfolha nos seis locais, nas duas versões, com a faixa de 90% da calibração.", [T["biomas"]]),
    ("mt-possibilidades", "Espaço de possibilidades", "4.6", "Resumo dos 5.688 cenários de danos combinados: quando o talhão atacado supera o controle e o que se recupera.", [T["possibilidades"], gt, im]),
]
M = [dict(id=i, titulo=t, secao=s, intro=x, tabelas=tb) for i, t, s, x, tb in S]
(A / "material_tcc.js").write_text("const MATERIAL_TCC = " + json.dumps(M, ensure_ascii=False) + ";\n", encoding="utf8")
print(len(M), "seções;", sum(len(m["tabelas"]) for m in M), "tabelas")
