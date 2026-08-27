# 📊 SalesInsight PY - Análise e Visualização de Dados de Vendas

O **SalesInsight PY** é um pipeline completo em Python para processamento, limpeza, análise estatística e visualização de dados de vendas. O projeto gera relatórios em tabelas, gráficos de desempenho e arquivos estruturados para suporte à tomada de decisão.

---

## 🛠️ Tecnologias e Bibliotecas Utilizadas

* **Python 3.x** - Linguagem base da aplicação
* **Pandas** - Manipulação, tratamento e agregação de dados
* **NumPy** - Análise e cálculos estatísticos de alto desempenho
* **Matplotlib & Seaborn** - Geração de gráficos e visualização de dados
* **JSON & OS** - Exportação e manipulação de arquivos e diretórios

---

## ⚙️ Funcionalidades e Requisitos Funcionais (RF01 - RF11)

* **RF01 (Dataset):** Geração e carregamento do dataset simulado de vendas.
* **RF02 (Inspeção):** Identificação da estrutura do dataframe, tipos de dados e valores nulos.
* **RF03 (Limpeza):** Padronização de nomes de clientes, conversão de datas e tratamento de dados ausentes/inválidos.
* **RF04 (Colunas Derivadas):** Cálculo da receita total por item, extração de mês/nome e categorização do ticket de venda.
* **RF05 (Métricas):** Agregação de faturamento mensal, curva de top produtos e vendas por região.
* **RF06 (Segmentação):** Categorização de clientes em tiers de valor (Bronze, Prata e Ouro).
* **RF07 (NumPy):** Análise estatística da receita (média, mediana, desvio padrão, mínimo, máximo e total).
* **RF08 (Visualizações):** Criação de gráficos em PNG (linhas, barras, dispersão e painel dashboard).
* **RF09 (Orientação a Objetos):** Encapsulamento de todo o pipeline através da classe `AnalisadorDeVendas`.
* **RF10 (Exportação):** Salvamento automático dos relatórios finais formatados em CSV e estatísticas em JSON.
* **RF11 (Ponto de Entrada):** Execução orquestrada e automatizada de todo o fluxo via função `main()`.

---

## 📁 Estrutura do Repositório

```text
insights-de-vendas-py/
│
├── salesinsight.py         # Script principal contendo do RF01 ao RF11
├── vendas.csv              # Base de dados de vendas simulada
├── README.md               # Documentação do projeto
└── saídas/                 # Pasta de arquivos exportados
    ├── metricas_por_mes.csv
    ├── segmentacao_clientes.csv
    ├── estatisticas_gerais.json
    └── graficos/
        ├── receita_por_mes.png
        ├── top_produtos.png
        ├── quantidade_vs_receita.png
        └── painel_resumo.png
