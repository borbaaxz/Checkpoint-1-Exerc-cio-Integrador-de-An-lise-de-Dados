# Checkpoint 1 – Exercício Integrador de Análise de Dados

Análise exploratória de um conjunto de dados sintético de **vendas de uma loja de eletrônicos**, aplicando Python, NumPy, Pandas, Matplotlib, Seaborn e técnicas de pré-processamento.

## Arquivos entregues

| Arquivo | Descrição |
|---|---|
| `analise_vendas.py` | Script principal: carga, exploração, limpeza, visualizações e conclusões. **Este é o arquivo a ser executado.** |
| `vendas_eletronicos.csv` | Conjunto de dados utilizado (615 registros, gerado sinteticamente com valores ausentes, duplicados e inconsistências propositais para a atividade de limpeza). |
| `gerar_dataset.py` | Script opcional que gerou o `vendas_eletronicos.csv`. Não precisa ser executado — incluído apenas para mostrar como o dataset foi criado. Se rodado novamente, gera uma nova versão do CSV. |
| `vendas_eletronicos_dashboard.png` | Imagem gerada automaticamente ao rodar `analise_vendas.py`, com os 6 gráficos da análise. |

## Sobre o dataset

Base sintética representando vendas de uma loja de eletrônicos ao longo do ano de 2024, contendo:

- `id_venda`, `data_venda`, `produto`, `categoria`, `preco_unitario`, `quantidade`, `desconto_pct`, `forma_pagamento`, `estado`, `avaliacao_cliente`.

Foram inseridos propositalmente: valores ausentes, linhas duplicadas, inconsistências de texto (ex.: `"NOTEBOOK"`, `" notebook "`, `"Notebook"`) e outliers/erros de digitação (preços negativos, preços muito acima do padrão, quantidades negativas), para permitir a prática real de limpeza de dados pedida no enunciado.

## Como executar

### 1. Pré-requisitos
- Python 3.9 ou superior
- Bibliotecas: `pandas`, `numpy`, `matplotlib`, `seaborn`

### 2. Instalar as dependências
```bash
pip install pandas numpy matplotlib seaborn
```

### 3. Rodar o programa
Coloque `analise_vendas.py` e `vendas_eletronicos.csv` na mesma pasta e execute:
```bash
python analise_vendas.py
```

### 4. Saída esperada
- Todo o passo a passo da análise (carregamento, `info()`, `describe()`, valores ausentes/duplicados, limpeza, respostas às questões analíticas e conclusões) é impresso no terminal.
- Um arquivo de imagem `vendas_eletronicos_dashboard.png`, com 6 visualizações, é salvo na mesma pasta.

## Estrutura da análise (`analise_vendas.py`)

1. **Carregamento e apresentação dos dados** — leitura do CSV, dimensões, `head()`/`tail()`.
2. **Informações gerais e estatísticas** — `info()`, `dtypes`, `describe()` numérico e categórico.
3. **Identificação de problemas** — valores ausentes, linhas duplicadas, inconsistências de texto e outliers (regra do IQR).
4. **Limpeza e pré-processamento** — remoção de duplicatas, padronização de texto, conversão de tipos, correção/remoção de valores impossíveis, tratamento de outliers, preenchimento de ausentes (mediana/moda) e criação de novas colunas (`valor_total`, `mes`).
5. **Visualizações** (6 gráficos): histograma de preços, boxplot por categoria, receita total por produto, matriz de correlação (heatmap), receita mensal (série temporal) e vendas por forma de pagamento.
6. **Conclusões e insights** — principais indicadores de negócio extraídos da base já limpa.

As **Questões Analíticas** do enunciado são respondidas diretamente no código, via comentários `RESPOSTA:` e comandos `print()`, nas seções 2 (distribuição), 5 (correlações) e 6 (insights e pré-processamento).

## Autor
Atividade desenvolvida para o Checkpoint 1 da disciplina de Análise de Dados.
