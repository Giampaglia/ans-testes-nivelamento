-- tutorial/README.md
-- Passo a passo para rodar o programa

# Como Rodar o Programa

## 1️⃣ Criar o banco de dados
Abra seu terminal ou cliente SQL e execute:

### MySQL
```sql
CREATE DATABASE ans_dados;
USE ans_dados;
```

### PostgreSQL
```sql
CREATE DATABASE ans_dados;
\c ans_dados
```

## 2️⃣ Criar as tabelas
Execute o script para criar as tabelas:

### MySQL
```bash
mysql -u seu_usuario -p ans_dados < scripts/01_criar_tabelas.sql
```

### PostgreSQL
```bash
psql -U seu_usuario -d ans_dados -f scripts/01_criar_tabelas.sql
```

## 3️⃣ Importar os dados
Coloque os arquivos CSV na pasta `dados/`, depois rode:

### MySQL
```bash
mysql -u seu_usuario -p ans_dados < scripts/02_importar_dados.sql
```

### PostgreSQL
```bash
psql -U seu_usuario -d ans_dados -f scripts/02_importar_dados.sql
```

## 4️⃣ Rodar a análise
Agora, execute o script para ver as 10 operadoras com maiores despesas:

### MySQL
```bash
mysql -u seu_usuario -p ans_dados < scripts/03_analise_despesas.sql
```

### PostgreSQL
```bash
psql -U seu_usuario -d ans_dados -f scripts/03_analise_despesas.sql
```

## 5️⃣ Verificar manualmente
Para conferir os dados carregados:
```sql
SELECT * FROM operadoras LIMIT 10;
SELECT * FROM demonstracoes_contabeis LIMIT 10;
```