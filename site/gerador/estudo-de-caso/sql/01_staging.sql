-- 01_staging.sql: leitura dos CSVs da ANAC, sem transformar o conteúdo.
-- Executado a partir de gerador/estudo-de-caso/ (os caminhos são relativos a essa pasta).
--
-- Os três arquivos têm o mesmo formato: UTF-8 com BOM, uma primeira linha "Atualizado em: AAAA-MM-DD"
-- (pulada com skip=1), separador ";", aspas duplas e o texto "null" no lugar de valor ausente.
-- Tudo é lido como texto (all_varchar): os tipos são definidos nas tabelas de fato, onde cada
-- conversão fica visível.

CREATE OR REPLACE VIEW stg_vra AS
SELECT *
FROM read_csv('dados/vra/VRA_*.csv',
              skip = 1, header = true, delim = ';', quote = '"',
              nullstr = 'null', all_varchar = true, filename = true);

CREATE OR REPLACE VIEW stg_estatistica AS
SELECT *
FROM read_csv('dados/estatisticas/Dados_Estatisticos.csv',
              skip = 1, header = true, delim = ';', quote = '"',
              nullstr = ['null', ''], all_varchar = true)
WHERE CAST(ANO AS INTEGER) >= 2023;           -- o arquivo vai de 2000 até hoje

CREATE OR REPLACE VIEW stg_reclamacao AS
SELECT *
FROM read_csv('dados/reclamacoes/dadosconsumidor*.csv',
              skip = 1, header = true, delim = ';', quote = '"',
              nullstr = 'null', all_varchar = true, union_by_name = true);
