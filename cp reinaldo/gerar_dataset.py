"""
Gera o dataset "vendas_eletronicos.csv" usado no Checkpoint 1.

Este script cria uma base sintética (mas realista) de vendas de uma loja
de eletrônicos, incluindo de forma PROPOSITAL:
- valores ausentes (NaN)
- linhas duplicadas
- inconsistências de texto (maiúsculas/minúsculas, espaços)
- outliers (preços absurdos, quantidades negativas)

O objetivo é ter uma base "suja" para praticar limpeza e pré-processamento
no script principal (analise_vendas.py).
"""

import numpy as np
import pandas as pd

np.random.seed(42)

N = 600  # número de vendas "válidas" antes de inserir sujeiras

produtos_precos = {
    "Notebook": 3500.0,
    "Smartphone": 2200.0,
    "Tablet": 1400.0,
    "Monitor": 900.0,
    "Fone de Ouvido": 250.0,
    "Teclado": 180.0,
    "Mouse": 90.0,
}
produtos = list(produtos_precos.keys())

categorias = {
    "Notebook": "Informática",
    "Smartphone": "Telefonia",
    "Tablet": "Telefonia",
    "Monitor": "Informática",
    "Fone de Ouvido": "Acessórios",
    "Teclado": "Acessórios",
    "Mouse": "Acessórios",
}

estados = ["SP", "RJ", "MG", "RS", "PR", "BA", "SC", "PE", "CE", "DF"]
pagamentos = ["Cartão de Crédito", "Cartão de Débito", "Pix", "Boleto"]

datas = pd.date_range("2024-01-01", "2024-12-31", freq="D")

linhas = []
for i in range(N):
    produto = np.random.choice(produtos)
    preco_base = produtos_precos[produto]
    preco = round(np.random.normal(preco_base, preco_base * 0.12), 2)
    quantidade = np.random.choice([1, 1, 1, 2, 2, 3], p=[0.4, 0.2, 0.15, 0.15, 0.05, 0.05])
    desconto = np.random.choice([0, 0, 0.05, 0.10, 0.15, 0.20], p=[0.5, 0.15, 0.15, 0.1, 0.05, 0.05])
    avaliacao = np.random.choice([1, 2, 3, 4, 5], p=[0.03, 0.07, 0.20, 0.40, 0.30])
    data_venda = np.random.choice(datas)
    estado = np.random.choice(estados)
    pagamento = np.random.choice(pagamentos, p=[0.4, 0.25, 0.3, 0.05])

    linhas.append({
        "id_venda": 1000 + i,
        "data_venda": pd.Timestamp(data_venda).strftime("%Y-%m-%d"),
        "produto": produto,
        "categoria": categorias[produto],
        "preco_unitario": preco,
        "quantidade": quantidade,
        "desconto_pct": desconto,
        "forma_pagamento": pagamento,
        "estado": estado,
        "avaliacao_cliente": avaliacao,
    })

df = pd.DataFrame(linhas)

# ---------------------------------------------------------------
# Inserindo "sujeiras" propositais para o exercício de limpeza
# ---------------------------------------------------------------

# 1) Valores ausentes em algumas colunas
for col, frac in [("preco_unitario", 0.03), ("avaliacao_cliente", 0.05),
                   ("estado", 0.02), ("forma_pagamento", 0.02)]:
    idx = df.sample(frac=frac, random_state=1).index
    df.loc[idx, col] = np.nan

# 2) Inconsistências de texto (maiúsculas/minúsculas e espaços extras)
idx_txt = df.sample(frac=0.08, random_state=2).index
df.loc[idx_txt, "produto"] = df.loc[idx_txt, "produto"].str.upper()
idx_txt2 = df.sample(frac=0.05, random_state=3).index
df.loc[idx_txt2, "produto"] = " " + df.loc[idx_txt2, "produto"].str.lower() + " "
idx_txt3 = df.sample(frac=0.05, random_state=4).index
df.loc[idx_txt3, "estado"] = df.loc[idx_txt3, "estado"].str.lower()

# 3) Outliers / valores impossíveis
idx_out1 = df.sample(n=4, random_state=5).index
df.loc[idx_out1, "preco_unitario"] = df.loc[idx_out1, "preco_unitario"] * 25  # preço absurdamente alto
idx_out2 = df.sample(n=3, random_state=6).index
df.loc[idx_out2, "preco_unitario"] = -df.loc[idx_out2, "preco_unitario"]  # preço negativo (erro de digitação)
idx_out3 = df.sample(n=3, random_state=7).index
df.loc[idx_out3, "quantidade"] = -1  # quantidade negativa (erro de sistema)

# 4) Linhas duplicadas (mesma venda repetida no sistema)
duplicadas = df.sample(n=15, random_state=8)
df = pd.concat([df, duplicadas], ignore_index=True)

# Embaralha as linhas para não deixar as sujeiras "visíveis" no final do arquivo
df = df.sample(frac=1, random_state=9).reset_index(drop=True)

df.to_csv("vendas_eletronicos.csv", index=False, encoding="utf-8-sig")
print(f"Dataset gerado com {len(df)} linhas -> vendas_eletronicos.csv")
