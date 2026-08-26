"""
SalesInsight PY - Analise e Visualizacao de Dados de Vendas
Autor: Alex Martins
"""

import pandas as pd
import numpy as np
import random
import re
import os
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime, timedelta


def gerar_dataset_vendas(n_registros=200, seed=42):
    """Gera um dataset sintético de vendas com dados sujos."""
    random.seed(seed)
    np.random.seed(seed)
    produtos = [
        "Notebook", "Smartphone", "Tablet", "Monitor",
        "Teclado", "Mouse", "Headset"
    ]
    categorias = {
        "Notebook": "Computadores", "Smartphone": "Celulares",
        "Tablet": "Celulares", "Monitor": "Computadores",
        "Teclado": "Perifericos", "Mouse": "Perifericos",
        "Headset": "Perifericos"
    }
    precos = {
        "Notebook": 3500, "Smartphone": 2200, "Tablet": 1800,
        "Monitor": 1200, "Teclado": 250, "Mouse": 120, "Headset": 350
    }
    regioes = ["Sudeste", "Sul", "Nordeste", "Centro-Oeste", "Norte"]
    data_inicio = datetime(2025, 1, 1)
    dados = []
    for i in range(n_registros):
        produto = random.choice(produtos)
        categoria = categorias[produto]
        quantidade = random.randint(1, 10)
        preco = round(precos[produto] * random.uniform(0.85, 1.15), 2)
        data = data_inicio + timedelta(days=random.randint(0, 364))
        data_txt = data.strftime("%Y-%m-%d")
        cliente = f"Cliente_{random.randint(1, 50):03d}"

        if random.random() < 0.05:
            quantidade = None
        if random.random() < 0.04:
            preco = None
        if random.random() < 0.06:
            produto = " " + produto + " "
        if random.random() < 0.03:
            data_txt = "DATA INVALIDA"
        if random.random() < 0.10:
            cliente = random.choice([
                cliente.upper().replace("_", "-"),
                cliente + "!!",
                " " + cliente,
                cliente.replace("Cliente_", "cliente#"),
            ])

        dados.append({
            "id_venda": i + 1,
            "data_venda": data_txt,
            "cliente": cliente,
            "produto": produto,
            "categoria": categoria,
            "regiao": random.choice(regioes),
            "quantidade": quantidade,
            "preco_unitario": preco
        })
    return pd.DataFrame(dados)


def inspecionar_dados(df):
    """Exibe as informacoes estruturais do DataFrame."""
    print("\n=== INSPECAO INICIAL DO DATASET ===")
    print(f"Shape: {df.shape}")
    print(f"\nColunas: {list(df.columns)}")
    print(f"\nTipos de dados:\n{df.dtypes}")
    print(f"\nValores nulos por coluna:\n{df.isnull().sum()}")
    print(f"\nPrimeiros registros:\n{df.head()}")
    return df


def limpar_dados(df):
    """
    Limpa e trata o DataFrame de vendas.
    Retorna: (df_limpo, relatorio), onde relatorio e um dicionario
    com as contagens de registros iniciais, removidos e finais.
    """
    df = df.copy()
    total_inicial = len(df)

    # 1. Remover espacos extras nas colunas de texto
    colunas_texto = ["cliente", "produto", "categoria", "regiao"]
    for col in colunas_texto:
        df[col] = df[col].str.strip()

    # 2. Converter data_venda e remover datas invalidas
    df["data_venda"] = pd.to_datetime(df["data_venda"], errors="coerce")
    antes_datas = len(df)
    df = df.dropna(subset=["data_venda"])
    removidos_datas = antes_datas - len(df)

    # 3. Remover nulos nas colunas criticas
    antes_nulos = len(df)
    df = df.dropna(subset=["quantidade", "preco_unitario"])
    removidos_nulos = antes_nulos - len(df)

    # 4. Ajustar os tipos numericos
    df["quantidade"] = df["quantidade"].astype(int)
    df["preco_unitario"] = df["preco_unitario"].astype(float)

    # 5. Padronizar o nome do cliente usando regex
    df["cliente"] = df["cliente"].apply(
        lambda s: re.sub(r"[^A-Za-z0-9_]", "", str(s).strip())
    )

    # 6. Validar o padrao Cliente_NNN e sinalizar fora do padrao
    padrao_cliente = re.compile(r"^Cliente_\d{3}$", flags=re.IGNORECASE)
    df["cliente_fora_padrao"] = ~df["cliente"].str.match(padrao_cliente)

    # 7. Montar e imprimir o relatorio de limpeza
    total_final = len(df)
    relatorio = {
        "registros_iniciais": total_inicial,
        "removidos_datas_invalidas": removidos_datas,
        "removidos_nulos_criticos": removidos_nulos,
        "registros_finais": total_final,
        "clientes_fora_do_padrao": int(df["cliente_fora_padrao"].sum())
    }

    print("\n=== RELATORIO DE LIMPEZA ===")
    for chave, valor in relatorio.items():
        print(f"{chave}: {valor}")

    return df, relatorio


def criar_colunas_derivadas(df):
    """
    Cria colunas derivadas a partir do DataFrame limpo:
    receita_total, mes, mes_nome, trimestre, ano, faixa_receita_item.
    """
    df = df.copy()

    # 1. Receita total = quantidade x preco unitario
    df["receita_total"] = df["quantidade"] * df["preco_unitario"]

    # 2. Extrair mes, trimestre e ano da data
    df["mes"] = df["data_venda"].dt.month
    df["trimestre"] = "Q" + df["data_venda"].dt.quarter.astype(str)
    df["ano"] = df["data_venda"].dt.year

    # 3. Nome do mes em portugues, via dicionario
    nomes_meses = {
        1: "Janeiro", 2: "Fevereiro", 3: "Marco", 4: "Abril",
        5: "Maio", 6: "Junho", 7: "Julho", 8: "Agosto",
        9: "Setembro", 10: "Outubro", 11: "Novembro", 12: "Dezembro"
    }
    df["mes_nome"] = df["mes"].map(nomes_meses)

    # 4. Classificar a receita da linha em faixas, de forma vetorizada
    condicoes = [
        df["receita_total"] < 500,
        (df["receita_total"] >= 500) & (df["receita_total"] < 5000),
        df["receita_total"] >= 5000,
    ]
    faixas = ["Baixo Valor", "Medio Valor", "Alto Valor"]
    df["faixa_receita_item"] = np.select(
        condicoes, faixas, default="Nao Classificado"
    )

    return df


def calcular_metricas(df):
    """
    Calcula as metricas agregadas do dataset.
    Retorna um dicionario no formato {nome_da_metrica: DataFrame}.
    Chaves: por_mes, top_produtos, por_categoria, por_regiao.
    """
    metricas = {}

    # 1. Receita total, quantidade vendida e numero de vendas por mes
    por_mes = df.groupby("mes").agg(
        receita_total=("receita_total", "sum"),
        quantidade=("quantidade", "sum"),
        n_vendas=("id_venda", "count")
    ).reset_index()
    metricas["por_mes"] = por_mes

    # 2. Receita total por produto (Top 5, em ordem decrescente)
    top_produtos = df.groupby("produto").agg(
        receita_total=("receita_total", "sum")
    ).reset_index()
    top_produtos = top_produtos.sort_values(
        "receita_total", ascending=False
    ).head(5)
    metricas["top_produtos"] = top_produtos

    # 3. Receita total por categoria
    por_categoria = df.groupby("categoria").agg(
        receita_total=("receita_total", "sum")
    ).reset_index()
    por_categoria = por_categoria.sort_values(
        "receita_total", ascending=False
    )
    metricas["por_categoria"] = por_categoria

    # 4. Receita total e ticket medio por regiao
    por_regiao = df.groupby("regiao").agg(
        receita_total=("receita_total", "sum"),
        ticket_medio=("receita_total", "mean")
    ).reset_index()
    por_regiao = por_regiao.sort_values("receita_total", ascending=False)
    metricas["por_regiao"] = por_regiao

    return metricas


def segmentar_clientes(df):
    """
    Agrupa por cliente, soma a receita e classifica em
    Bronze / Prata / Ouro.
    Retorna um DataFrame com: cliente, total_gasto, segmento.
    """
    clientes = df.groupby("cliente").agg(
        total_gasto=("receita_total", "sum")
    ).reset_index()

    # Classificar em Bronze / Prata / Ouro usando lambda + apply
    clientes["segmento"] = clientes["total_gasto"].apply(
        lambda gasto: "Ouro" if gasto > 15000
        else ("Prata" if gasto >= 5000 else "Bronze")
    )

    return clientes


def calcular_estatisticas_numpy(df):
    """
    Aplica operacoes NumPy sobre a coluna receita_total.
    Retorna um dicionario com os valores agregados calculados.
    """
    receitas = df["receita_total"].to_numpy()

    media = np.mean(receitas)
    mediana = np.median(receitas)
    desvio_padrao = np.std(receitas)
    soma = np.sum(receitas)

    receitas_escalonadas = (receitas - receitas.min()) / (receitas.max() - receitas.min())

    vendas_acima_da_media = receitas[receitas > media]
    qtd_acima_da_media = len(vendas_acima_da_media)

    return {
        "media": media,
        "mediana": mediana,
        "desvio_padrao": desvio_padrao,
        "soma": soma,
        "qtd_vendas_acima_da_media": qtd_acima_da_media,
        "receitas_escalonadas_amostra": receitas_escalonadas[:5]
    }


def configurar_visual():
    """Configura o tema visual global dos graficos (paleta em tons de azul)."""
    paleta_azul = sns.light_palette("#1f77b4", n_colors=8, reverse=False)
    sns.set_theme(style="whitegrid", palette=paleta_azul)
    plt.rcParams["figure.figsize"] = (10, 6)
    plt.rcParams["axes.titlesize"] = 14
    os.makedirs("outputs/graficos", exist_ok=True)


def grafico_receita_por_mes(por_mes):
    """Gera o grafico de linha da receita total por mes."""
    fig, ax = plt.subplots()
    ax.plot(
        por_mes["mes"], por_mes["receita_total"],
        marker="o", linewidth=2, color="#1f77b4"
    )
    ax.set_title("Receita Total por Mes")
    ax.set_xlabel("Mes")
    ax.set_ylabel("Receita Total (R$)")
    plt.tight_layout()
    plt.savefig("outputs/graficos/receita_por_mes.png", dpi=150)
    plt.close()
    print("Grafico salvo: outputs/graficos/receita_por_mes.png")


def grafico_top_produtos(top_produtos):
    """Gera o grafico de barras dos top 5 produtos por receita."""
    fig, ax = plt.subplots()
    sns.barplot(
        data=top_produtos, y="produto", x="receita_total",
        hue="produto", legend=False, palette="Blues_d", ax=ax
    )
    ax.set_title("Top 5 Produtos por Receita")
    ax.set_xlabel("Receita Total (R$)")
    ax.set_ylabel("Produto")
    plt.tight_layout()
    plt.savefig("outputs/graficos/top_produtos.png", dpi=150)
    plt.close()
    print("Grafico salvo: outputs/graficos/top_produtos.png")


def grafico_quantidade_vs_receita(df):
    """Gera o grafico de dispersao: quantidade x receita_total, por categoria."""
    fig, ax = plt.subplots()
    sns.scatterplot(
        data=df, x="quantidade", y="receita_total",
        hue="categoria", palette="Blues_d", ax=ax
    )
    ax.set_title("Quantidade x Receita Total (por Categoria)")
    ax.set_xlabel("Quantidade Vendida")
    ax.set_ylabel("Receita Total (R$)")
    ax.legend(title="Categoria")
    plt.tight_layout()
    plt.savefig("outputs/graficos/quantidade_vs_receita.png", dpi=150)
    plt.close()
    print("Grafico salvo: outputs/graficos/quantidade_vs_receita.png")


def grafico_painel_resumo(df, por_mes, top_produtos, por_regiao):
    """Gera um painel 2x2 combinando as principais visualizacoes."""
    fig, axes = plt.subplots(2, 2, figsize=(14, 9))

    axes[0, 0].plot(
        por_mes["mes"], por_mes["receita_total"],
        marker="o", linewidth=2, color="#1f77b4"
    )
    axes[0, 0].set_title("Receita por Mes")
    axes[0, 0].set_xlabel("Mes")
    axes[0, 0].set_ylabel("Receita Total (R$)")

    sns.barplot(
        data=top_produtos, y="produto", x="receita_total",
        hue="produto", legend=False, palette="Blues_d", ax=axes[0, 1]
    )
    axes[0, 1].set_title("Top 5 Produtos")
    axes[0, 1].set_xlabel("Receita Total (R$)")
    axes[0, 1].set_ylabel("Produto")

    sns.scatterplot(
        data=df, x="quantidade", y="receita_total",
        hue="categoria", palette="Blues_d", ax=axes[1, 0]
    )
    axes[1, 0].set_title("Quantidade x Receita")
    axes[1, 0].set_xlabel("Quantidade Vendida")
    axes[1, 0].set_ylabel("Receita Total (R$)")

    sns.barplot(
        data=por_regiao, y="regiao", x="receita_total",
        hue="regiao", legend=False, palette="Blues_d", ax=axes[1, 1]
    )
    axes[1, 1].set_title("Receita por Regiao")
    axes[1, 1].set_xlabel("Receita Total (R$)")
    axes[1, 1].set_ylabel("Regiao")

    fig.suptitle("SalesInsight PY - Painel Resumo", fontsize=16)
    plt.tight_layout()
    plt.savefig("outputs/graficos/painel_resumo.png", dpi=150)
    plt.close()
    print("Grafico salvo: outputs/graficos/painel_resumo.png")


if __name__ == "__main__":
    df_bruto = gerar_dataset_vendas()
    df_bruto.to_csv("vendas.csv", index=False)
    print(f"Dataset gerado com {len(df_bruto)} registros.")

    df_bruto = inspecionar_dados(df_bruto)

    df_limpo, relatorio_limpeza = limpar_dados(df_bruto)
    print("\nPrimeiros registros do dataset limpo:")
    print(df_limpo.head())

    df_transformado = criar_colunas_derivadas(df_limpo)
    print("\nPrimeiros registros com colunas derivadas:")
    print(df_transformado.head())

    metricas = calcular_metricas(df_transformado)
    print("\n=== POR MES ===")
    print(metricas["por_mes"])
    print("\n=== TOP 5 PRODUTOS ===")
    print(metricas["top_produtos"])
    print("\n=== POR CATEGORIA ===")
    print(metricas["por_categoria"])
    print("\n=== POR REGIAO ===")
    print(metricas["por_regiao"])

    clientes_segmentados = segmentar_clientes(df_transformado)
    print("\n=== TOP 10 CLIENTES POR GASTO TOTAL ===")
    print(clientes_segmentados.sort_values("total_gasto", ascending=False).head(10))
    print("\n=== DISTRIBUICAO POR SEGMENTO ===")
    print(clientes_segmentados["segmento"].value_counts())

    estatisticas_numpy = calcular_estatisticas_numpy(df_transformado)
    print("\n=== ESTATISTICAS NUMPY (receita_total) ===")
    for chave, valor in estatisticas_numpy.items():
        print(f"{chave}: {valor}")

    configurar_visual()
    grafico_receita_por_mes(metricas["por_mes"])
    grafico_top_produtos(metricas["top_produtos"])
    grafico_quantidade_vs_receita(df_transformado)
    grafico_painel_resumo(
        df_transformado,
        metricas["por_mes"],
        metricas["top_produtos"],
        metricas["por_regiao"]
    )
