# ANEXO A — Tutorial do simulador e glossário

> Para quem nunca usou o 3-PG. Este anexo explica o que cada campo faz e como rodar um primeiro cenário em poucos minutos. O simulador está em https://claude.ai/artifact/5tJe3WvFVU4g45kgZLszoE (abre no celular e no computador, com internet).

## A.1 O que o simulador faz, em uma frase
Ele mostra como um plantio de eucalipto cresce ao longo de 7 a 8 anos e quanto de madeira se perde quando uma parte das folhas é retirada por insetos.

## A.2 Primeiro uso (cinco passos)
1. **Abra o simulador** e toque em **Tutorial guiado**. Ele explica a tela passo a passo.
2. **Escolha o local** no campo **Local**. Os locais disponíveis devem incluir Indianópolis-MG, Imperatriz-MA e Telêmaco Borba-PR, os três sítios deste trabalho **[CONFERIR nomes exatos no menu]**.
3. **Escolha a espécie e o material genético** nos campos **Espécie** e **Material genético**. Para o TCC, use o material A1 de *Eucalyptus urophylla*.
4. **Escolha o cenário de desfolha**: em **Intensidade, d** (de 0 a 95% das folhas da copa retiradas por ataque) e em **Agente (catálogo do TCC)** (o tipo de inseto ou doença). Os campos **Perda de eficiência, r** e **Mortalidade de árvores, m** descrevem o efeito do ataque: r é a perda de eficiência fotossintética por 4 meses a cada evento; m é a mortalidade no primeiro evento.
5. **Toque em Simular.** O resultado mostra o volume do plantio no controle e no cenário desfolhado **[CONFERIR o gráfico na versão publicada]**. Use **Exportar** para salvar a tabela e **Copiar tabela** para colar em outro programa.

Para ver o que cada termo significa, toque em **Conceitos**. Para ver como o cálculo é feito, use **Modo explicar**.

## A.3 Como ler o resultado
- **Controle:** o plantio sem ataque. É a referência.
- **Desfolhado:** o plantio com o cenário escolhido.
- **Perda (%):** a diferença **[CONFERIR o nome do campo na tela]** de volume entre os dois, em relação ao controle. Um número positivo indica perda; um número negativo indica ganho, que aparece em alguns cenários da versão calibrada e precisa ser discutido no texto.
- **Volume:** madeira do tronco, em metros cúbicos por hectare.

Os resultados são cenários simulados. Não são medições de campo e não indicam a frequência real de ataques.

## A.4 Cuidados
- Os números do simulador são os do modelo, não os de um talhão específico.
- Não compare resultados de locais diferentes sem olhar o clima e a água disponível de cada um.
- Os oito parâmetros de *E. globulus* ainda usados no modelo estão marcados no simulador; eles ficam fora da análise principal (seção 3.2).

---

## A.5 Glossário

**3-PG (Physiological Principles Predicting Growth).** Modelo matemático que calcula o crescimento de um plantio mês a mês, a partir da luz que as folhas recebem, da temperatura, da chuva e da água disponível no solo. É um modelo de processos: cada passo representa uma parte do funcionamento da planta.

**Desfolha.** Retirada de folhas, por insetos, doenças ou por corte experimental. Reduz a área que capta luz e, portanto, a produção de madeira.

**Intensidade (d).** Fração da copa retirada em um ataque, de 0 a 1 (ou de 0 a 100%).

**Compensação.** Quando perde folhas, a planta restante passa a fazer mais fotossíntese por folha. Este trabalho modela essa resposta com parâmetros calibrados.

**Recuperação da copa.** Retorno da área foliar após o ataque. Medida pelo índice de área foliar (IAF).

**IAF (índice de área foliar).** Área de folhas por área de solo. Um IAF de 3 significa três metros quadrados de folha para cada metro quadrado de terreno.

**ASW (água disponível).** Quantidade de água que o solo guarda e a planta consegue usar, em milímetros, até 2 m de profundidade.

**FR (fertility rating).** Índice de fertilidade do solo, de 0 (muito pobre) a 1 (sem limitação nutricional). Neste trabalho, é estimado a partir de análises de solo e não medido diretamente.

**Calibração.** Ajuste dos parâmetros do modelo para que ele reproduza dados já conhecidos.

**Validação.** Teste do modelo com dados que não foram usados no ajuste. Por isso, a validação é mais forte que a calibração.

**Cenário.** Uma combinação de local, material, intensidade, frequência e época do ataque.

**Volume.** Madeira do tronco por hectare, em m³ ha⁻¹.

**DAP (diâmetro à altura do peito).** Diâmetro do tronco medido a 1,3 m do solo.

**Sítio.** Local com clima e solo definidos.

**TECHS.** Rede de experimentos de *Eucalyptus* clonais em Brasil e Uruguai, de onde vêm dados de crescimento e de água disponível usados neste trabalho.
