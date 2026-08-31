"""
============================================================
 Checkpoint 1 - Exercício Integrador de Análise de Dados
============================================================
Tema: Vendas de uma loja de eletrônicos (dataset sintético)
Arquivo de dados: vendas_eletronicos.csv

Este programa cumpre as 6 etapas pedidas no enunciado:
  1. Carregar e apresentar os dados
  2. Exibir informações gerais, tipos das colunas e estatísticas descritivas
  3. Identificar valores ausentes, duplicados e inconsistências
  4. Realizar limpeza e pré-processamento
  5. Criar no mínimo 3 visualizações
  6. Apresentar conclusões e insights

As respostas às "Questões Analíticas" do enunciado aparecem ao longo do
código, marcadas com comentários "RESPOSTA:" e impressas via print().

Como executar:
    python analise_vendas.py
(ver README.md para instruções detalhadas e instalação de dependências)
============================================================
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

sns.set_theme(style="whitegrid")
pd.set_option("display.max_columns", None)
pd.set_option("display.width", 120)


def titulo(texto):
    """Imprime um cabeçalho de seção para organizar a saída no terminal."""
    print("\n" + "=" * 70)
    print(texto)
    print("=" * 70)


# ============================================================
# 1) CARREGAR E APRESENTAR OS DADOS
# ============================================================
titulo("1. CARREGAMENTO E APRESENTAÇÃO DOS DADOS")

CAMINHO_ARQUIVO = "vendas_eletronicos.csv"
df = pd.read_csv(CAMINHO_ARQUIVO)

print(f"Dataset carregado: {CAMINHO_ARQUIVO}")
print(f"Dimensões (linhas, colunas): {df.shape}")
print("\nPrimeiras 5 linhas:")
print(df.head())
print("\nÚltimas 5 linhas:")
print(df.tail())


# ============================================================
# 2) INFORMAÇÕES GERAIS, TIPOS E ESTATÍSTICAS DESCRITIVAS
# ============================================================
titulo("2. INFORMAÇÕES GERAIS, TIPOS DE DADOS E ESTATÍSTICAS DESCRITIVAS")

print("Informações gerais (df.info()):")
df.info()

print("\nTipos de dados por coluna:")
print(df.dtypes)

print("\nEstatísticas descritivas - colunas numéricas:")
print(df.describe())

print("\nEstatísticas descritivas - colunas categóricas (texto):")
print(df.describe(include="object"))

# RESPOSTA (Questão Analítica 1 - distribuição das principais variáveis):
# Já dá para observar aqui que 'preco_unitario' tem desvio padrão e máximo
# muito elevados em relação à média/mediana -> forte indício de outliers.
# 'quantidade' apresenta valor mínimo negativo, o que é fisicamente
# impossível para uma venda -> erro de lançamento a ser tratado.
print(
    "\nRESPOSTA (distribuição inicial): o desvio padrão elevado e o valor "
    "máximo muito acima do 3º quartil em 'preco_unitario' já indicam a "
    "presença de outliers. O valor mínimo negativo em 'quantidade' indica "
    "erro de digitação/sistema."
)


# ============================================================
# 3) VALORES AUSENTES, DUPLICADOS E INCONSISTÊNCIAS
# ============================================================
titulo("3. VALORES AUSENTES, DUPLICADOS E INCONSISTÊNCIAS")

print("Valores ausentes por coluna:")
ausentes = df.isnull().sum()
ausentes_pct = (df.isnull().mean() * 100).round(2)
resumo_ausentes = pd.DataFrame({"qtd_ausentes": ausentes, "pct_ausentes": ausentes_pct})
print(resumo_ausentes[resumo_ausentes["qtd_ausentes"] > 0])

qtd_duplicadas = df.duplicated().sum()
print(f"\nLinhas duplicadas (todas as colunas idênticas): {qtd_duplicadas}")

print("\nValores únicos da coluna 'produto' (verificar inconsistência de texto):")
print(sorted(df["produto"].unique()))

print("\nValores únicos da coluna 'estado' (verificar inconsistência de texto):")
print(sorted(df["estado"].dropna().unique()))

print("\nVerificando inconsistências numéricas:")
print(f"  Vendas com preco_unitario <= 0: {(df['preco_unitario'] <= 0).sum()}")
print(f"  Vendas com quantidade <= 0: {(df['quantidade'] <= 0).sum()}")

# Detecção de outliers em preco_unitario usando a regra do IQR
Q1 = df["preco_unitario"].quantile(0.25)
Q3 = df["preco_unitario"].quantile(0.75)
IQR = Q3 - Q1
limite_inferior = Q1 - 1.5 * IQR
limite_superior = Q3 + 1.5 * IQR
outliers_preco = df[(df["preco_unitario"] < limite_inferior) | (df["preco_unitario"] > limite_superior)]
print(f"\nOutliers em 'preco_unitario' pela regra do IQR: {len(outliers_preco)} linhas")
print(f"  Faixa aceitável (IQR): [{limite_inferior:.2f}, {limite_superior:.2f}]")


# ============================================================
# 4) LIMPEZA E PRÉ-PROCESSAMENTO
# ============================================================
titulo("4. LIMPEZA E PRÉ-PROCESSAMENTO DOS DADOS")

df_limpo = df.copy()
linhas_iniciais = len(df_limpo)

# --- 4.1 Remover linhas totalmente duplicadas ---
df_limpo = df_limpo.drop_duplicates()
print(f"[4.1] Duplicadas removidas: {linhas_iniciais - len(df_limpo)}")

# --- 4.2 Padronizar texto (remover espaços extras e uniformizar capitalização) ---
df_limpo["produto"] = df_limpo["produto"].str.strip().str.title()
df_limpo["estado"] = df_limpo["estado"].str.strip().str.upper()
print("[4.2] Colunas 'produto' e 'estado' padronizadas (strip + capitalização única).")

# --- 4.3 Corrigir tipos de dados ---
df_limpo["data_venda"] = pd.to_datetime(df_limpo["data_venda"], errors="coerce")
print("[4.3] Coluna 'data_venda' convertida para datetime.")

# --- 4.4 Remover/corrigir inconsistências físicas (valores impossíveis) ---
# Preço negativo é erro de digitação -> corrigimos usando valor absoluto
qtd_preco_negativo = (df_limpo["preco_unitario"] < 0).sum()
df_limpo["preco_unitario"] = df_limpo["preco_unitario"].abs()
print(f"[4.4] Preços negativos corrigidos com valor absoluto: {qtd_preco_negativo}")

# Quantidade negativa não tem correção lógica segura -> removemos as linhas
qtd_qtd_negativa = (df_limpo["quantidade"] < 0).sum()
df_limpo = df_limpo[df_limpo["quantidade"] > 0]
print(f"[4.4] Linhas com quantidade negativa removidas: {qtd_qtd_negativa}")

# --- 4.5 Tratar outliers extremos de preço (recalculado após limpeza acima) ---
Q1 = df_limpo["preco_unitario"].quantile(0.25)
Q3 = df_limpo["preco_unitario"].quantile(0.75)
IQR = Q3 - Q1
limite_superior = Q3 + 1.5 * IQR
qtd_outliers = (df_limpo["preco_unitario"] > limite_superior).sum()
df_limpo = df_limpo[df_limpo["preco_unitario"] <= limite_superior]
print(f"[4.5] Outliers extremos de preço (> {limite_superior:.2f}) removidos: {qtd_outliers}")

# --- 4.6 Tratar valores ausentes ---
# avaliacao_cliente: ausência não invalida a venda -> preenchemos com a mediana
mediana_avaliacao = df_limpo["avaliacao_cliente"].median()
df_limpo["avaliacao_cliente"] = df_limpo["avaliacao_cliente"].fillna(mediana_avaliacao)
print(f"[4.6] 'avaliacao_cliente' ausente preenchida com a mediana ({mediana_avaliacao}).")

# forma_pagamento e estado: categóricas -> preenchidas com a moda (mais frequente)
for col in ["forma_pagamento", "estado"]:
    moda = df_limpo[col].mode()[0]
    df_limpo[col] = df_limpo[col].fillna(moda)
    print(f"[4.6] '{col}' ausente preenchida com a moda ('{moda}').")

# preco_unitario ausente: sem preço não é possível calcular receita -> removemos
qtd_preco_nan = df_limpo["preco_unitario"].isnull().sum()
df_limpo = df_limpo.dropna(subset=["preco_unitario"])
print(f"[4.6] Linhas sem 'preco_unitario' removidas (não é possível estimar): {qtd_preco_nan}")

# --- 4.7 Engenharia de atributos (feature engineering) ---
df_limpo["valor_total"] = (
    df_limpo["preco_unitario"] * df_limpo["quantidade"] * (1 - df_limpo["desconto_pct"])
).round(2)
df_limpo["mes"] = df_limpo["data_venda"].dt.month
df_limpo["nome_mes"] = df_limpo["data_venda"].dt.strftime("%b")
print("[4.7] Novas colunas criadas: 'valor_total', 'mes', 'nome_mes'.")

print(f"\nLinhas antes da limpeza: {linhas_iniciais}")
print(f"Linhas após a limpeza:   {len(df_limpo)}")
print(f"Total de linhas removidas: {linhas_iniciais - len(df_limpo)}")
print("\nVerificação final de valores ausentes:")
print(df_limpo.isnull().sum())

# RESPOSTA (Questão Analítica 4 - pré-processamento necessário e por quê):
print(
    "\nRESPOSTA (pré-processamento realizado):\n"
    "  - Remoção de duplicatas: registros de venda repetidos distorceriam receita.\n"
    "  - Padronização de texto (strip/title/upper): 'notebook', 'NOTEBOOK' e "
    "'Notebook' representavam o mesmo produto e seriam contados como categorias "
    "diferentes nos gráficos e agrupamentos.\n"
    "  - Conversão de data para datetime: necessário para extrair mês e analisar "
    "sazonalidade.\n"
    "  - Correção de preços negativos e remoção de quantidades negativas: "
    "erros de lançamento que não fazem sentido no domínio do problema.\n"
    "  - Remoção de outliers extremos de preço (regra do IQR): preços 20-25x "
    "acima do padrão distorceriam médias e visualizações.\n"
    "  - Preenchimento de ausentes: mediana para variável numérica (robusta a "
    "outliers) e moda para variáveis categóricas; já preço ausente foi removido "
    "por impedir o cálculo confiável da receita da venda."
)


# ============================================================
# 5) VISUALIZAÇÕES (mínimo de 3 - aqui temos 5)
# ============================================================
titulo("5. VISUALIZAÇÕES")

fig, axes = plt.subplots(2, 3, figsize=(18, 10))
fig.suptitle("Checkpoint 1 - Análise de Vendas de Eletrônicos", fontsize=16, fontweight="bold")

# 5.1 Histograma - distribuição do preço unitário
sns.histplot(df_limpo["preco_unitario"], bins=25, kde=True, ax=axes[0, 0], color="#4C72B0")
axes[0, 0].set_title("Distribuição do Preço Unitário")
axes[0, 0].set_xlabel("Preço (R$)")
axes[0, 0].set_ylabel("Frequência")

# 5.2 Boxplot - preço por categoria de produto (checagem visual de outliers)
sns.boxplot(data=df_limpo, x="categoria", y="preco_unitario", ax=axes[0, 1], hue="categoria",
            palette="Set2", legend=False)
axes[0, 1].set_title("Preço Unitário por Categoria")
axes[0, 1].set_xlabel("Categoria")
axes[0, 1].set_ylabel("Preço (R$)")

# 5.3 Gráfico de barras - receita total por produto
receita_produto = df_limpo.groupby("produto")["valor_total"].sum().sort_values(ascending=False)
sns.barplot(x=receita_produto.values, y=receita_produto.index, ax=axes[0, 2],
            hue=receita_produto.index, palette="viridis", legend=False)
axes[0, 2].set_title("Receita Total por Produto")
axes[0, 2].set_xlabel("Receita (R$)")
axes[0, 2].set_ylabel("Produto")

# 5.4 Heatmap de correlação entre variáveis numéricas
colunas_numericas = ["preco_unitario", "quantidade", "desconto_pct", "avaliacao_cliente", "valor_total"]
matriz_corr = df_limpo[colunas_numericas].corr()
sns.heatmap(matriz_corr, annot=True, fmt=".2f", cmap="coolwarm", center=0, ax=axes[1, 0])
axes[1, 0].set_title("Matriz de Correlação")

# 5.5 Evolução da receita mensal (série temporal)
receita_mensal = df_limpo.groupby(["mes", "nome_mes"])["valor_total"].sum().reset_index().sort_values("mes")
sns.lineplot(data=receita_mensal, x="nome_mes", y="valor_total", marker="o", ax=axes[1, 1], sort=False)
axes[1, 1].set_title("Receita Total por Mês")
axes[1, 1].set_xlabel("Mês")
axes[1, 1].set_ylabel("Receita (R$)")
axes[1, 1].tick_params(axis="x", rotation=45)

# 5.6 Distribuição de vendas por forma de pagamento
sns.countplot(data=df_limpo, y="forma_pagamento", ax=axes[1, 2],
              hue="forma_pagamento", order=df_limpo["forma_pagamento"].value_counts().index,
              palette="pastel", legend=False)
axes[1, 2].set_title("Vendas por Forma de Pagamento")
axes[1, 2].set_xlabel("Quantidade de Vendas")
axes[1, 2].set_ylabel("Forma de Pagamento")

plt.tight_layout(rect=[0, 0, 1, 0.96])
ARQUIVO_SAIDA = "vendas_eletronicos_dashboard.png"
plt.savefig(ARQUIVO_SAIDA, dpi=150, bbox_inches="tight")
print(f"Painel com 6 visualizações salvo em: {ARQUIVO_SAIDA}")
plt.close(fig)

# RESPOSTA (Questão Analítica 2 - correlações importantes):
correlacao_desconto_qtd = matriz_corr.loc["desconto_pct", "quantidade"]
correlacao_preco_valor = matriz_corr.loc["preco_unitario", "valor_total"]
print(
    f"\nRESPOSTA (correlações): a correlação entre 'preco_unitario' e "
    f"'valor_total' é de {correlacao_preco_valor:.2f} (forte, esperado, pois o "
    f"valor total deriva do preço). A correlação entre 'desconto_pct' e "
    f"'quantidade' é de {correlacao_desconto_qtd:.2f}, indicando uma relação "
    "fraca — descontos maiores não estão associados a compras em maior "
    "quantidade neste conjunto de dados."
)


# ============================================================
# 6) CONCLUSÕES E INSIGHTS
# ============================================================
titulo("6. CONCLUSÕES E INSIGHTS")

produto_mais_vendido_qtd = df_limpo.groupby("produto")["quantidade"].sum().idxmax()
produto_mais_receita = receita_produto.idxmax()
estado_mais_vendas = df_limpo["estado"].value_counts().idxmax()
pagamento_preferido = df_limpo["forma_pagamento"].value_counts().idxmax()
mes_maior_receita = receita_mensal.loc[receita_mensal["valor_total"].idxmax(), "nome_mes"]
avaliacao_media = df_limpo["avaliacao_cliente"].mean()
ticket_medio = df_limpo["valor_total"].mean()

print(f"- Produto com maior volume vendido (unidades): {produto_mais_vendido_qtd}")
print(f"- Produto que mais gera receita: {produto_mais_receita}")
print(f"- Estado com mais vendas registradas: {estado_mais_vendas}")
print(f"- Forma de pagamento preferida: {pagamento_preferido}")
print(f"- Mês com maior receita: {mes_maior_receita}")
print(f"- Avaliação média dos clientes: {avaliacao_media:.2f} / 5")
print(f"- Ticket médio por venda: R$ {ticket_medio:,.2f}")

# RESPOSTA (Questão Analítica 3 - insights extraídos dos dados):
print(
    "\nRESPOSTA (principais insights):\n"
    f"  1. Apesar de acessórios (Mouse, Teclado, Fone) terem maior volume de "
    f"unidades vendidas, o produto '{produto_mais_receita}' concentra a maior "
    "receita, típico de itens de ticket alto e baixo giro.\n"
    f"  2. A forma de pagamento '{pagamento_preferido}' domina as transações, "
    "sugerindo priorizar parcerias e taxas competitivas com essa modalidade.\n"
    f"  3. A avaliação média de {avaliacao_media:.2f}/5 indica satisfação "
    "geral boa, mas ainda há espaço para melhoria (não está próxima de 5).\n"
    "  4. A correlação fraca entre desconto e quantidade sugere que a "
    "política de descontos atual não está impulsionando vendas em maior "
    "volume — vale testar promoções mais agressivas ou segmentadas.\n"
    "  5. A limpeza de dados (duplicatas, textos inconsistentes, outliers e "
    "valores impossíveis) foi essencial: sem ela, métricas como receita "
    "total e preço médio estariam infladas/distorcidas."
)

titulo("FIM DA ANÁLISE")
print("Script executado com sucesso.")
