"""
SalesInsight PY - Analise e Visualizacao de Dados de Vendas
Autor: Alex Martins
"""

import pandas as pd
import numpy as np
import random
import re
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


if __name__ == "__main__":
    df_bruto = gerar_dataset_vendas()
    df_bruto.to_csv("vendas.csv", index=False)
    print(f"Dataset gerado com {len(df_bruto)} registros.")

    df_bruto = inspecionar_dados(df_bruto)

    df_limpo, relatorio_limpeza = limpar_dados(df_bruto)
    print("\nPrimeiros registros do dataset limpo:")
    print(df_limpo.head())
