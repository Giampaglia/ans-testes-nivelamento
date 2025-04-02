CREATE TABLE operadoras (
    id_operadora INT PRIMARY KEY,
    nome VARCHAR(255),
    cnpj VARCHAR(18),
    modalidade VARCHAR(100)
);

CREATE TABLE demonstracoes_contabeis (
    id SERIAL PRIMARY KEY,
    id_operadora INT,
    ano INT,
    trimestre INT,
    despesas_eventos DECIMAL(18,2),
    FOREIGN KEY (id_operadora) REFERENCES operadoras(id_operadora)
);