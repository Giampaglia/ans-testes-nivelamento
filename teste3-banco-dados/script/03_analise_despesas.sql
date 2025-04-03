-- Últimos 3 meses
SELECT o.razao_social, SUM(dc.vl_saldo_final - dc.vl_saldo_inicial) AS total_despesas
FROM demonstracoes_contabeis dc
JOIN operadoras o ON dc.id_operadora = o.id_operadora
WHERE dc.data >= DATE_SUB(CURDATE(), INTERVAL 3 MONTH)
AND dc.cd_conta_contabil = 'EVENTOS/SINISTROS'
GROUP BY o.razao_social
ORDER BY total_despesas DESC
LIMIT 10;

-- Último ano
SELECT o.razao_social, SUM(dc.vl_saldo_final - dc.vl_saldo_inicial) AS total_despesas
FROM demonstracoes_contabeis dc
JOIN operadoras o ON dc.id_operadora = o.id_operadora
WHERE YEAR(dc.data) = YEAR(CURDATE()) - 1
AND dc.cd_conta_contabil = 'EVENTOS/SINISTROS'
GROUP BY o.razao_social
ORDER BY total_despesas DESC
LIMIT 10;
