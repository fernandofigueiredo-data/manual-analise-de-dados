-- 02_dimensoes.sql: dimensões do modelo estrela.

-- dim_empresa: de-para entre o código ICAO (VRA e Dados Estatísticos) e o Nome Fantasia do
-- consumidor.gov.br. O arquivo de-para é versionado em sql/de_para_empresas.csv.
CREATE OR REPLACE TABLE dim_empresa AS
SELECT *
FROM read_csv('sql/de_para_empresas.csv', header = true, delim = ';', quote = '"');

-- dim_aerodromo: código ICAO, nome, UF e região, a partir das origens e destinos dos Dados Estatísticos.
CREATE OR REPLACE TABLE dim_aerodromo AS
WITH todos AS (
    SELECT AEROPORTO_DE_ORIGEM_SIGLA AS icao, AEROPORTO_DE_ORIGEM_NOME AS nome,
           AEROPORTO_DE_ORIGEM_UF AS uf, AEROPORTO_DE_ORIGEM_REGIAO AS regiao, AEROPORTO_DE_ORIGEM_PAIS AS pais
    FROM stg_estatistica
    UNION ALL
    SELECT AEROPORTO_DE_DESTINO_SIGLA, AEROPORTO_DE_DESTINO_NOME,
           AEROPORTO_DE_DESTINO_UF, AEROPORTO_DE_DESTINO_REGIAO, AEROPORTO_DE_DESTINO_PAIS
    FROM stg_estatistica
)
SELECT icao, any_value(nome) AS nome, any_value(uf) AS uf, any_value(regiao) AS regiao, any_value(pais) AS pais
FROM todos
WHERE icao IS NOT NULL
GROUP BY icao;

-- dim_data: um dia por linha, do início do VRA ao fim do período.
CREATE OR REPLACE TABLE dim_data AS
SELECT
    CAST(d AS DATE)                    AS data_id,
    year(d)                            AS ano,
    month(d)                           AS mes,
    CAST(date_trunc('month', d) AS DATE) AS ano_mes,
    isodow(d)                          AS dia_semana,          -- 1 = segunda … 7 = domingo
    isodow(d) IN (6, 7)                AS fim_de_semana
FROM generate_series(DATE '2023-01-01', DATE '2026-12-31', INTERVAL 1 DAY) AS t(d);
