-- 03_fatos.sql: tabelas de fato, com os tipos definidos e as regras de qualidade explícitas.

-- fato_voo: uma linha por etapa de voo (VRA), só linhas domésticas (Código Tipo Linha = 'N').
CREATE OR REPLACE TABLE fato_voo AS
WITH tipado AS (
    SELECT
        "ICAO Empresa Aérea"     AS empresa_icao,
        "Número Voo"             AS numero_voo,
        "Código Tipo Linha"      AS tipo_linha,
        "ICAO Aeródromo Origem"  AS origem_icao,
        "ICAO Aeródromo Destino" AS destino_icao,
        try_strptime("Partida Prevista", '%Y-%m-%d %H:%M:%S') AS partida_prevista,
        try_strptime("Partida Real",     '%Y-%m-%d %H:%M:%S') AS partida_real,
        try_strptime("Chegada Prevista", '%Y-%m-%d %H:%M:%S') AS chegada_prevista,
        try_strptime("Chegada Real",     '%Y-%m-%d %H:%M:%S') AS chegada_real,
        "Situação Voo"           AS situacao,
        "Código Justificativa"   AS justificativa
    FROM stg_vra
    WHERE "Código Tipo Linha" = 'N'
),
bruto AS (
    SELECT
        *,
        situacao = 'REALIZADO' AND partida_real IS NOT NULL AND chegada_real IS NOT NULL AS tem_horario_real,
        date_diff('minute', partida_prevista, partida_real)  AS atraso_partida_bruto,
        date_diff('minute', chegada_prevista, chegada_real)  AS atraso_chegada_bruto
    FROM tipado
),
corrigido AS (
    -- virada de dia: voo previsto para 23h50 que sai às 00h56 às vezes aparece com a data real do dia
    -- anterior, o que dá um "adiantamento" de cerca de -1.374 min. Menos de -12 h só pode ser isso: soma 24 h.
    SELECT
        *,
        atraso_partida_bruto < -720 OR atraso_chegada_bruto < -720                AS corrigido_virada_dia,
        atraso_partida_bruto + CASE WHEN atraso_partida_bruto < -720 THEN 1440 ELSE 0 END AS atraso_partida_corr,
        atraso_chegada_bruto + CASE WHEN atraso_chegada_bruto < -720 THEN 1440 ELSE 0 END AS atraso_chegada_corr
    FROM bruto
),
validado AS (
    -- horário real válido: voo realizado, com os dois horários reais e atrasos plausíveis depois da correção
    -- (partida até 2 h adiantada e chegada até 3 h adiantada; atraso de no máximo 24 h)
    SELECT
        *,
        tem_horario_real
            AND atraso_partida_corr BETWEEN -120 AND 1440
            AND atraso_chegada_corr BETWEEN -180 AND 1440
            AND chegada_real > partida_real                                         AS horario_real_valido
    FROM corrigido
)
SELECT
    empresa_icao, numero_voo, origem_icao, destino_icao,
    CAST(partida_prevista AS DATE)                                      AS data_id,
    hour(partida_prevista)                                              AS hora_prevista,
    partida_prevista, partida_real, chegada_prevista, chegada_real,
    situacao, justificativa, tem_horario_real, corrigido_virada_dia, horario_real_valido,
    CASE WHEN horario_real_valido THEN atraso_partida_corr END          AS atraso_partida_min,
    CASE WHEN horario_real_valido THEN atraso_chegada_corr END          AS atraso_chegada_min
FROM validado
WHERE partida_prevista IS NOT NULL;

-- fato_estatistica_mes: passageiros e oferta por empresa, mês e natureza (doméstica ou internacional).
CREATE OR REPLACE TABLE fato_estatistica_mes AS
SELECT
    EMPRESA_SIGLA                                                   AS empresa_icao,
    CAST(ANO AS INTEGER)                                            AS ano,
    CAST(MES AS INTEGER)                                            AS mes,
    NATUREZA                                                        AS natureza,
    SUM(CAST(PASSAGEIROS_PAGOS AS BIGINT))                          AS passageiros_pagos,
    SUM(CAST(ASSENTOS AS BIGINT))                                   AS assentos,
    SUM(CAST(DECOLAGENS AS BIGINT))                                 AS decolagens,
    SUM(CAST(replace(RPK, ',', '.') AS DOUBLE))                     AS rpk,
    SUM(CAST(replace(ASK, ',', '.') AS DOUBLE))                     AS ask
FROM stg_estatistica
WHERE GRUPO_DE_VOO = 'REGULAR'
GROUP BY ALL;

-- fato_reclamacao: uma linha por reclamação no consumidor.gov.br.
CREATE OR REPLACE TABLE fato_reclamacao AS
SELECT
    "Nome Fantasia"                                                 AS nome_fantasia,
    CAST("Data Abertura" AS DATE)                                   AS data_id,
    "UF"                                                            AS uf,
    "Grupo Problema"                                                AS grupo_problema,
    "Problema"                                                      AS problema,
    -- problema operacional: o motivo da reclamação é o próprio atraso, cancelamento ou interrupção do voo
    regexp_matches("Problema", 'Atraso de voo|Cancelamento de voo|interrupção de voo') AS problema_operacional,
    "Respondida" = 'S'                                              AS respondida,
    "Situação"                                                      AS situacao,
    "Avaliação Reclamação"                                          AS avaliacao,
    TRY_CAST("Nota do Consumidor" AS INTEGER)                       AS nota,
    TRY_CAST("Tempo Resposta (em dias)" AS INTEGER)                 AS tempo_resposta_dias
FROM stg_reclamacao;
