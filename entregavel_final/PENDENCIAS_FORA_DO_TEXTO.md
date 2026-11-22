# Pendências fora do texto — situação em 22/11/2026

## Status

Não há correção editorial acionável fora do texto nesta rodada. As limitações abaixo
permanecem registradas no TCC e não são pedidos de dados nem tarefas abertas de análise.

## Limitações registradas

- **Dados TECHS:** não houve acesso aos dados brutos de inventário das parcelas TECHS 9 e
  22. A série meteorológica específica da parcela TECHS 22 também não foi acessada; as
  simulações usam a série municipal NASA POWER. Os valores agregados publicados são usados
  somente como benchmarks adaptados, não como validação independente.
- **VPD:** o modelo calcula `vpd_day` com temperaturas mínima e máxima. Embora os arquivos
  municipais NASA POWER contenham RH2M, essa variável não entra no cálculo. O script
  `teste_vpd.py` citado em versões anteriores não está nesta versão do repositório, e não há
  análise reproduzível que isole causalmente o VPD com RH2M. O texto não afirma que VPD
  explica ou deixa de explicar os ganhos simulados.
- **Random Forest:** a análise filtra os cenários marcados como aptos antes do ajuste; usa
  fatores de cenário, água, fertilidade, local e material, mas não VPD. A validação cruzada
  mede a reprodução de saídas simuladas, não validação independente em campo.
- **Confirmação empírica:** comparações com publicações disponíveis são adaptadas. Sem
  inventários independentes compatíveis e dados de desfolha em campo, o TCC não declara
  validação empírica do módulo.

## Verificações e entrega

- O validador oficial do DOCX e um renderizador PDF não estão disponíveis neste ambiente;
  a conferência estrutural do DOCX não substitui esses procedimentos.
- Não há extensão de Google Drive carregada nesta sessão; portanto, não houve upload nem
  registro no Diário do TCC II. Essa limitação operacional não altera as conclusões do texto.
