from fastapi import FastAPI, Query, HTTPException
import pandas as pd
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# Configuração do CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://127.0.0.1:5500"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Carrega o arquivo CSV
try:
    df = pd.read_csv("Relatorio_cadop.csv", delimiter=";", encoding='utf-8')
    print("CSV carregado com sucesso!")
except Exception as e:
    print(f"Erro ao carregar CSV: {e}")
    df = pd.DataFrame()

@app.get("/operadoras/")
def buscar_operadoras(
    nome: str = Query(..., min_length=2, description="Termo para busca no nome da operadora"),
    limite: int = Query(10, description="Número máximo de resultados")
):
    """
    Busca operadoras por nome
    """
    if df.empty:
        raise HTTPException(status_code=500, detail="Base de dados não disponível")
    
    try:
        resultados = df[
            df["Nome_Fantasia"].str.contains(nome, case=False, na=False)
        ].head(limite)
        
        return resultados.to_dict(orient="records")
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Erro na busca: {str(e)}")

import logging

logging.basicConfig(level=logging.INFO)

@app.get("/operadora/{registro_ans}")
def detalhes_operadora(registro_ans: str):
    """
    Obtém detalhes de uma operadora pelo registro ANS, retornando apenas os campos desejados.
    """
    if df.empty:
        raise HTTPException(status_code=500, detail="Base de dados não disponível")
    
    operadora = df[df["Registro ANS"] == registro_ans]
    
    if operadora.empty:
        raise HTTPException(status_code=404, detail="Operadora não encontrada")

    # Definição dos campos desejados
    campos_desejados = [
        "Representante",
        "Cargo_Representante",
        "Regiao_de_Comercializacao",
        "Data_Registro_ANS",
        "CNPJ",
        "Razao_Social",
        "Nome_Fantasia",
    ]
    
    # Retorna apenas os campos especificados
    return operadora[campos_desejados].iloc[0].to_dict()
