from fastapi import FastAPI, Query, HTTPException
import pandas as pd
from fastapi.middleware.cors import CORSMiddleware
import logging

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
    df = pd.read_csv("Relatorio_cadop.csv", delimiter=";", encoding='utf-8', dtype={"Registro_ANS": str})
    df.columns = df.columns.str.strip()  # Remove espaços extras nos nomes das colunas
    print("CSV carregado com sucesso!")
except Exception as e:
    print(f"Erro ao carregar CSV: {e}")
    df = pd.DataFrame()

print(df.columns.tolist())  # Verifica os nomes reais das colunas


@app.get("/operadoras/")
def buscar_operadoras(
    termo: str = Query(..., description="Registro ANS ou Razão Social da operadora"),
    limite: int = Query(10, description="Número máximo de resultados")
):
    """
    Busca operadoras pelo Registro ANS ou Razão Social
    """
    if df.empty:
        raise HTTPException(status_code=500, detail="Base de dados não disponível")

    try:
        resultados = df[
            (df["Registro_ANS"].astype(str) == termo) |  # Busca por Registro ANS
            (df["Razao_Social"].str.contains(termo, case=False, na=False))  # Busca por Razão Social
        ].head(limite)

        if resultados.empty:
            raise HTTPException(status_code=404, detail="Nenhuma operadora encontrada")

        #Substitui NaN por strings vazias para evitar erro JSON
        resultados = resultados.fillna("")

        return resultados.to_dict(orient="records")
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Erro na busca: {str(e)}")
    
    


logging.basicConfig(level=logging.INFO)

@app.get("/operadora/{registro_ans}")
def detalhes_operadora(registro_ans: str):
    """
    Obtém detalhes de uma operadora pelo registro ANS, retornando apenas os campos desejados.
    """
    if df.empty:
        raise HTTPException(status_code=500, detail="Base de dados não disponível")

    if "Registro_ANS" not in df.columns:
        raise HTTPException(status_code=500, detail="Coluna 'Registro_ANS' não encontrada no CSV")

    # Filtra o DataFrame para encontrar a operadora pelo Registro ANS
    operadora = df[df["Registro_ANS"].astype(str) == str(registro_ans)]
    
    if operadora.empty:
        raise HTTPException(status_code=404, detail="Operadora não encontrada")

    # Definir colunas desejadas (apenas as que existem no DataFrame)
    campos_desejados = [col for col in [
        "Representante",
        "Cargo_Representante",
        "Regiao_de_Comercializacao",
        "Data_Registro_ANS",
        "CNPJ",
        "Razao_Social",
        "Nome_Fantasia",
    ] if col in df.columns]

    # Converte a série para dicionário e substitui NaN por None
    resultado = operadora[campos_desejados].iloc[0].to_dict()
    resultado = {chave: (None if pd.isna(valor) else valor) for chave, valor in resultado.items()}
    
    df_resultado = df_resultado[[col for col in campos_desejados if col in df_resultado.columns]]

    resultado = df_resultado.to_dict(orient="records")
    print("Resposta da API:", resultado)  # Debug para ver o que está sendo enviado
    


    return resultado
    

