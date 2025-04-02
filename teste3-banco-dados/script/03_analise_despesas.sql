SELECT o.nome, SUM(dc.despesas_eventos) AS total_despesas
FROM demonstracoes_contabeis dc
JOIN operadoras o ON dc.id_operadora = o.id_operadora
WHERE dc.ano = YEAR(CURDATE()) AND dc.trimestre = (SELECT MAX(trimestre) FROM demonstracoes_contabeis WHERE ano = YEAR(CURDATE()))
GROUP BY o.nome
ORDER BY total_despesas DESC
LIMIT 10;

SELECT o.nome, SUM(dc.despesas_eventos) AS total_despesas
FROM demonstracoes_contabeis dc
JOIN operadoras o ON dc.id_operadora = o.id_operadora
WHERE dc.ano = YEAR(CURDATE()) - 1
GROUP BY o.nome
ORDER BY total_despesas DESC
LIMIT 10;