# Pendências fora do texto — situação em 22/11/2026

## Status

Não há correção editorial acionável fora do texto nesta rodada. As limitações abaixo
permanecem registradas no TCC e não são pedidos de dados nem tarefas abertas de análise.

## Limitações registradas

- **Dados TECHS:** não houve acesso aos dados brutos de inventário das parcelas TECHS 9 e
  22. A série meteorológica específica da parcela TECHS 22 também não foi acessada; as
  simulações usam a série municipal NASA POWER. Os valores agregados publicados são usados
  somente como benchmarks adaptados, não como validação independente.
- **VPD:** o modelo mantém o cálculo padrão de `vpd_day` por Tmax e Tmin. A nova análise
  reproduzível compara essa entrada com uma estimativa alternativa baseada em RH2M nos
  mesmos cenários e controles. Ela mede sensibilidade às entradas climáticas, não valida
  VPD em campo nem explica causalmente os ganhos simulados.
- **Random Forest:** a análise filtra os cenários marcados como aptos antes do ajuste; usa
  fatores de cenário, água, fertilidade, local e material, mas não VPD. A validação cruzada
  mede a reprodução de saídas simuladas, não validação independente em campo.
- **Confirmação empírica:** comparações com publicações disponíveis são adaptadas. Sem
  inventários independentes compatíveis e dados de desfolha em campo, o TCC não declara
  validação empírica do módulo.

## Verificações

- `validar_docx.py` verifica a integridade do pacote DOCX, o XML, as relações internas e as
  imagens. Ele não implementa validação completa do esquema OOXML nem substitui a inspeção
  visual do PDF renderizado. O teste estrutural local foi executado; o PDF não foi gerado
  nesta sessão.
- O LibreOffice não está disponível nesta sessão; a renderização do PDF e a conferência
  visual de paginação ficam para a etapa de edição local do documento.
