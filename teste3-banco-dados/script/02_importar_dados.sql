LOAD DATA INFILE 'dados/operadoras_ativas.csv'
INTO TABLE operadoras
FIELDS TERMINATED BY ';'
ENCLOSED BY '"'
LINES TERMINATED BY '\n'
IGNORE 1 LINES
(id_operadora, nome, cnpj, modalidade);

LOAD DATA INFILE 'dados/demonstracoes_contabeis/dados.csv'
INTO TABLE demonstracoes_contabeis
FIELDS TERMINATED BY ';'
ENCLOSED BY '"'
LINES TERMINATED BY '\n'
IGNORE 1 LINES
(id_operadora, ano, trimestre, despesas_eventos);