-- 04_marts.sql: tabela analítica companhia × mês, que junta as três fontes.
-- A ligação entre voos e reclamações só existe neste nível: o consumidor.gov.br não traz o número do voo.

CREATE OR REPLACE TABLE mart_empresa_mes AS
WITH voos AS (
    SELECT
        e.empresa, d.ano_mes,
        count(*) FILTER (WHERE f.situacao IN ('REALIZADO', 'CANCELADO'))   AS voos_previstos,
        count(*) FILTER (WHERE f.situacao = 'CANCELADO')                   AS voos_cancelados,
        count(*) FILTER (WHERE f.horario_real_valido)                      AS voos_com_horario,
        count(*) FILTER (WHERE f.atraso_partida_min > 15)                  AS voos_atraso15_partida,
        count(*) FILTER (WHERE f.atraso_chegada_min > 15)                  AS voos_atraso15_chegada,
        count(*) FILTER (WHERE f.atraso_partida_min > 240)                 AS voos_atraso240_partida
    FROM fato_voo AS f
    JOIN dim_empresa AS e USING (empresa_icao)
    JOIN dim_data    AS d USING (data_id)
    GROUP BY ALL
),
passageiros AS (
    SELECT
        e.empresa, make_date(s.ano, s.mes, 1)                             AS ano_mes,
        sum(s.passageiros_pagos)                                          AS passageiros_pagos,
        sum(s.passageiros_pagos) FILTER (WHERE s.natureza = 'DOMÉSTICA')  AS passageiros_domesticos,
        sum(s.rpk) FILTER (WHERE s.natureza = 'DOMÉSTICA')                AS rpk_domestico,
        sum(s.ask) FILTER (WHERE s.natureza = 'DOMÉSTICA')                AS ask_domestico
    FROM fato_estatistica_mes AS s
    JOIN dim_empresa AS e USING (empresa_icao)
    GROUP BY ALL
),
reclamacoes AS (
    SELECT
        e.empresa, d.ano_mes,
        count(*)                                                          AS reclamacoes,
        count(*) FILTER (WHERE r.problema_operacional)                    AS reclamacoes_operacionais,
        count(*) FILTER (WHERE r.grupo_problema = 'Cobrança / Contestação') AS reclamacoes_cobranca,
        count(*) FILTER (WHERE r.respondida)                              AS respondidas,
        count(*) FILTER (WHERE r.avaliacao IN ('Resolvida', 'Não Resolvida')) AS avaliadas,
        count(*) FILTER (WHERE r.avaliacao = 'Resolvida')                 AS resolvidas,
        count(*) FILTER (WHERE r.avaliacao = 'Não Resolvida')             AS nao_resolvidas,
        count(*) FILTER (WHERE r.avaliacao = 'Não Resolvida' AND r.problema_operacional) AS nao_resolvidas_operacionais,
        avg(r.tempo_resposta_dias)                                        AS tempo_resposta_medio_dias
    FROM fato_reclamacao AS r
    JOIN dim_empresa AS e ON r.nome_fantasia = e.nome_fantasia_consumidor
    JOIN dim_data    AS d USING (data_id)
    GROUP BY ALL
)
SELECT
    v.*,
    p.passageiros_pagos, p.passageiros_domesticos, p.rpk_domestico, p.ask_domestico,
    r.* EXCLUDE (empresa, ano_mes),
    100.0 * v.voos_cancelados / v.voos_previstos                          AS pct_cancelados,
    100.0 * v.voos_atraso15_chegada / v.voos_com_horario                  AS pct_atraso15_chegada,
    100.0 * v.voos_atraso15_partida / v.voos_com_horario                  AS pct_atraso15_partida,
    100.0 * p.rpk_domestico / p.ask_domestico                             AS ocupacao_pct,
    1e5 * r.reclamacoes / p.passageiros_pagos                             AS reclamacoes_100k,
    1e5 * r.reclamacoes_operacionais / p.passageiros_pagos                AS reclamacoes_operacionais_100k,
    1e5 * r.reclamacoes_cobranca / p.passageiros_pagos                    AS reclamacoes_cobranca_100k
FROM voos AS v
LEFT JOIN passageiros AS p USING (empresa, ano_mes)
LEFT JOIN reclamacoes AS r USING (empresa, ano_mes)
ORDER BY v.empresa, v.ano_mes;
