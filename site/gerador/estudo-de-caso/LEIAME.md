# Estudo de caso: atraso, cancelamento e reclamações na aviação brasileira

**Fonte: ANAC (dados abertos).** Voo Regular Ativo (VRA), Dados Estatísticos do Transporte Aéreo e reclamações do consumidor.gov.br, em https://sistemas.anac.gov.br/dadosabertos/. Uso livre com crédito à fonte (Decreto 8.777/2016, art. 2º, III).

Página no site: https://manual-analise-de-dados.vercel.app/estudo-de-caso/aviacao-comercial/

| Arquivo ou pasta | Conteúdo | Versionado |
|---|---|---|
| `Estudo_de_Caso_Aviacao_ANAC.ipynb` | o notebook, já executado, com as saídas | sim |
| `baixar_dados.py` | download reproduzível do período (`--inicio AAAA-MM --fim AAAA-MM`) | sim |
| `manifesto_download.json` | URL, tamanho e SHA-256 de cada arquivo baixado | sim |
| `sql/` | modelo estrela em DuckDB: leitura, dimensões, fatos e tabela analítica, mais o de-para das companhias | sim |
| `agregados/` | tabelas pequenas geradas pelo notebook e usadas no site e no README | sim |
| `dados/` | CSVs brutos da ANAC (~1 GB) e o banco `anac.duckdb` | **não** (`.gitignore`) |

## Reproduzir

A partir de `site/`, com o ambiente do gerador criado (ver `site/README.md`):

```bash
gerador/.venv/bin/python gerador/estudo-de-caso/baixar_dados.py --inicio 2023-01 --fim 2026-08
npm run gerar:caso
```

O primeiro comando baixa o que falta; o segundo executa o notebook (cerca de 2 minutos), grava as saídas nele e atualiza as páginas do site. O notebook também chama o download, então o segundo comando sozinho já basta.

## Agregados

Todos com o crédito "Fonte: ANAC (dados abertos)" e a mesma licença dos dados de origem.

| Arquivo | Grão |
|---|---|
| `empresa_mes.csv` | companhia × mês (jan/2023 a ago/2026): voos, cancelamentos, atrasos, passageiros, reclamações e taxas |
| `kpis_empresa.csv` | companhia: KPIs de pontualidade, cancelamento e ocupação do período |
| `conversao_empresa.csv` | companhia: voos com problema, reclamações operacionais e não resolvidas, com IC 95 % |
| `regressao_coeficientes.csv` | coeficientes dos modelos M1, M2 e M3, com IC 95 % |
| `ml_metricas_teste.csv` | ROC-AUC, PR-AUC e Brier do modelo e das linhas de base no teste (jan–ago/2026) |
| `resumo.json` | os números citados nos achados, no site e no README |
