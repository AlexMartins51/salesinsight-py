# ==============================================================================
# SALESINSIGHT PY - CÓDIGO COMPLETO (RF01 até RF11)
# ==============================================================================

import os
import re
import json
import random
from datetime import datetime, timedelta
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# Configuração visual global
sns.set_theme(style="whitegrid", palette="muted")
plt.rcParams["figure.figsize"] = (12, 6)

# --- RF01: Dataset ---
def gerar_dataset_vendas(n_registros=200, seed=42):
    random.seed(seed)
    np.random.seed(seed)
    produtos = ["Notebook", "Smartphone", "Tablet", "Monitor", "Teclado", "Mouse", "Headset"]
    categorias = {
        "Notebook": "Computadores", "Smartphone": "Celulares", "Tablet": "Celulares",
        "Monitor": "Computadores", "Teclado": "Perifericos", "Mouse": "Perifericos", "Headset": "Perifericos"
    }
    precos = {"Notebook": 3500, "Smartphone": 2200, "Tablet": 1800, "Monitor": 1200, "Teclado": 250, "Mouse": 120, "Headset": 350}
    regioes = ["Sudeste", "Sul", "Nordeste", "Centro-Oeste", "Norte"]
    data_inicio = datetime(2025, 1, 1)
    
    dados = []
    for i in range(n_registros):
        produto = random.choice(produtos)
        categoria = categorias[produto]
        quantidade = random.randint(1, 10)
        preco = round(precos[produto] * random.uniform(0.85, 1.15), 2)
        data_txt = (data_inicio + timedelta(days=random.randint(0, 364))).strftime("%Y-%m-%d")
        cliente = f"Cliente_{random.randint(1, 50):03d}"
        
        if random.random() < 0.05: quantidade = None
        if random.random() < 0.04: preco = None
        if random.random() < 0.06: produto = " " + produto + " "
        if random.random() < 0.03: data_txt = "DATA INVALIDA"
        if random.random() < 0.10: cliente = random.choice([cliente.upper().replace("_", "-"), cliente + "!!", " " + cliente])
            
        dados.append({
            "id_venda": i + 1, "data_venda": data_txt, "cliente": cliente,
            "produto": produto, "categoria": categoria, "regiao": random.choice(regioes),
            "quantidade": quantidade, "preco_unitario": preco
        })
    return pd.DataFrame(dados)

# --- RF02: Inspeção ---
def inspecionar_dados(df):
    print("\n=== INSPEÇÃO DOS DADOS ===")
    print(f"Shape: {df.shape}")
    print(f"Valores Nulos:\n{df.isnull().sum()}")

# --- RF03: Limpeza ---
def limpar_dados(df):
    df_limpo = df.copy()
    colunas_texto = df_limpo.select_dtypes(include=['object']).columns
    for col in colunas_texto:
        df_limpo[col] = df_limpo[col].astype(str).str.strip()
        
    df_limpo["data_venda"] = pd.to_datetime(df_limpo["data_venda"], errors="coerce")
    df_limpo = df_limpo.dropna(subset=["data_venda", "quantidade", "preco_unitario"])
    
    df_limpo["quantidade"] = df_limpo["quantidade"].astype(int)
    df_limpo["preco_unitario"] = df_limpo["preco_unitario"].astype(float)
    
    def padronizar_nome(nome):
        limpo = re.sub(r"[^A-Za-z0-9_]", "", str(nome).strip())
        numeros = re.findall(r"\d+", limpo)
        return f"Cliente_{int(numeros[0]):03d}" if numeros else "Cliente_000"

    df_limpo["cliente"] = df_limpo["cliente"].apply(padronizar_nome)
    return df_limpo, {"registros_finais": len(df_limpo)}

# --- RF04: Colunas Derivadas ---
def criar_colunas_derivadas(df):
    df_m = df.copy()
    df_m["receita_total"] = df_m["quantidade"] * df_m["preco_unitario"]
    df_m["mes"] = df_m["data_venda"].dt.month
    dici_meses = {1: "Janeiro", 2: "Fevereiro", 3: "Março", 4: "Abril", 5: "Maio", 6: "Junho", 
                  7: "Julho", 8: "Agosto", 9: "Setembro", 10: "Outubro", 11: "Novembro", 12: "Dezembro"}
    df_m["mes_nome"] = df_m["mes"].map(dici_meses)
    
    condicoes = [df_m["receita_total"] < 500, (df_m["receita_total"] >= 500) & (df_m["receita_total"] < 5000), df_m["receita_total"] >= 5000]
    df_m["faixa_receita_item"] = np.select(condicoes, ["Baixo Valor", "Medio Valor", "Alto Valor"], default="Nao Classificado")
    return df_m

# --- RF05: Métricas ---
def calcular_metricas(df):
    metricas = {}
    metricas["por_mes"] = df.groupby(["mes", "mes_nome"]).agg(receita_total=("receita_total", "sum"), quantidade=("quantidade", "sum"), n_vendas=("id_venda", "count")).reset_index().sort_values(by="mes")
    metricas["top_produtos"] = df.groupby("produto").agg(receita_total=("receita_total", "sum")).sort_values(by="receita_total", ascending=False).head(5).reset_index()
    metricas["por_regiao"] = df.groupby("regiao").agg(receita_total=("receita_total", "sum")).reset_index()
    return metricas

# --- RF06: Segmentação ---
def segmentar_clientes(df):
    df_cli = df.groupby("cliente").agg(total_gasto=("receita_total", "sum")).reset_index()
    df_cli["segmento"] = df_cli["total_gasto"].apply(lambda g: "Bronze" if g < 5000 else ("Prata" if g <= 15000 else "Ouro"))
    return df_cli.sort_values(by="total_gasto", ascending=False)

# --- RF07: NumPy ---
def calcular_estatisticas_numpy(df):
    receitas = df["receita_total"].to_numpy()
    return {
        "media": np.mean(receitas), "mediana": np.median(receitas),
        "desvio_padrao": np.std(receitas), "soma_total": np.sum(receitas),
        "minimo": np.min(receitas), "maximo": np.max(receitas)
    }

# --- RF08: Visualizações ---
def gerar_visualizacoes(metricas, df_limpo):
    os.makedirs("outputs/graficos", exist_ok=True)
    fig, ax = plt.subplots(figsize=(10, 5))
    ax.plot(metricas["por_mes"]["mes_nome"], metricas["por_mes"]["receita_total"], marker="o", color="navy")
    plt.savefig("outputs/graficos/receita_por_mes.png", dpi=150)
    plt.close()

# --- RF09: Função de Ordem Superior & Classe ---
def processar_coluna(df, coluna, funcao, nome_saida):
    df_temp = df.copy()
    df_temp[nome_saida] = df_temp[coluna].apply(funcao)
    return df_temp

class AnalisadorDeVendas:
    def __init__(self, caminho_arquivo):
        self.caminho_arquivo = caminho_arquivo
        self.df_bruto = None
        self.df_limpo = None
        self.metricas = {}
        self.clientes = None
        self.estatisticas_numpy = {}

    def carregar(self):
        self.df_bruto = pd.read_csv(self.caminho_arquivo)

    def limpar(self):
        self.df_limpo, _ = limpar_dados(self.df_bruto)

    def transformar(self):
        self.df_limpo = criar_colunas_derivadas(self.df_limpo)

    def analisar(self):
        self.metricas = calcular_metricas(self.df_limpo)
        self.clientes = segmentar_clientes(self.df_limpo)
        self.estatisticas_numpy = calcular_estatisticas_numpy(self.df_limpo)

    def visualizar(self):
        gerar_visualizacoes(self.metricas, self.df_limpo)

    def resumo(self):
        print("\n=== RESUMO EXECUTIVO ===")
        print(f"Total Faturamento: R$ {self.estatisticas_numpy['soma_total']:,.2f}")

# --- RF10: Exportação ---
def exportar_resultados(metricas, clientes, estatisticas):
    os.makedirs("outputs", exist_ok=True)
    metricas["por_mes"].to_csv("outputs/metricas_por_mes.csv", index=False, encoding="utf-8-sig")
    clientes.to_csv("outputs/segmentacao_clientes.csv", index=False, encoding="utf-8-sig")
    
    estatisticas_serializaveis = {k: v.item() if hasattr(v, "item") else v for k, v in estatisticas.items()}
    caminho_json = "outputs/estatisticas_gerais.json"
    
    with open(caminho_json, "w", encoding="utf-8") as f:
        json.dump(estatisticas_serializaveis, f, indent=4, ensure_ascii=False)
        
    with open(caminho_json, "r", encoding="utf-8") as f:
        conferencia = json.load(f)
    print("\n✅ [RF10] Arquivos CSV e JSON salvos e conferidos com sucesso.")

# --- RF11: Ponto de Entrada (Main) ---
def main():
    print("=" * 60)
    print(" SALESINSIGHT PY - Análise e Visualização de Dados de Vendas")
    print("=" * 60)
    
    caminho_dataset = "vendas.csv"
    if not os.path.exists(caminho_dataset):
        gerar_dataset_vendas().to_csv(caminho_dataset, index=False)

    analisador = AnalisadorDeVendas(caminho_dataset)
    analisador.carregar()
    inspecionar_dados(analisador.df_bruto)
    analisador.limpar()
    analisador.transformar()
    analisador.analisar()
    analisador.visualizar()
    analisador.resumo()
    exportar_resultados(analisador.metricas, analisador.clientes, analisador.estatisticas_numpy)
    
    print("\n🚀 [RF11] PROJETO EXECUTADO COM SUCESSO DE RF01 A RF11!")

if __name__ == "__main__":
    main()
