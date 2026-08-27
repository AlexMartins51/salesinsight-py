# 📊 SalesInsight PY - Análise e Visualização de Dados de Vendas

O **SalesInsight PY** é um pipeline completo em Python para processamento, limpeza, análise estatística e visualização de dados de vendas. O projeto gera relatórios em tabelas, gráficos de desempenho e arquivos estruturados para suporte à tomada de decisão.

Desenvolvido como Mini-Projeto Avaliativo do Módulo 01 (Semana 08) do curso Carreira Tech (SCTEC), simulando o papel de um Analista de Dados Júnior em uma empresa de varejo fictícia.

---

## 🛠️ Tecnologias e Bibliotecas Utilizadas

* **Python 3.x** - Linguagem base da aplicação
* **Pandas** - Manipulação, tratamento e agregação de dados
* **NumPy** - Análise e cálculos estatísticos de alto desempenho
* **Matplotlib & Seaborn** - Geração de gráficos e visualização de dados
* **re (Expressões Regulares)** - Padronização e limpeza de textos
* **datetime** - Geração e extração de componentes de data (mês, trimestre, ano)
* **JSON & OS** - Exportação e manipulação de arquivos e diretórios
* **Git & GitHub** - Versionamento com GitFlow simplificado (branches `main`, `develop`, `feat/pipeline-dados`, `docs/readme`)

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

## ▶️ Como Executar

### Google Colab (recomendado)

1. Faça upload do arquivo `salesinsight.py` para o ambiente do Colab.
2. Execute em uma célula:
   ```python
   !python salesinsight.py
   ```

### Localmente (VS Code ou terminal)

1. Instale o Python 3.10+.
2. Instale as dependências:
   ```
   pip install pandas numpy matplotlib seaborn
   ```
3. Execute:
   ```
   python salesinsight.py
   ```

Ao rodar, o script gera automaticamente o dataset `vendas.csv` (caso não exista), processa todo o fluxo de análise e salva os resultados na pasta `outputs/`.

---

## 📁 Estrutura do Repositório

```text
salesinsight-py/
│
├── salesinsight.py         # Script principal contendo do RF01 ao RF11
├── vendas.csv              # Base de dados de vendas simulada
├── README.md               # Documentação do projeto
└── outputs/                # Pasta de arquivos exportados
    ├── metricas_por_mes.csv
    ├── segmentacao_clientes.csv
    ├── estatisticas_gerais.json
    └── graficos/
        ├── receita_por_mes.png
        ├── top_produtos.png
        ├── quantidade_vs_receita.png
        └── painel_resumo.png
```

---

## 💡 Decisões Técnicas

**Limpeza sem "correção agressiva" de nomes de cliente:** nomes fora do padrão `Cliente_NNN` (ex.: `cliente#016`) são limpos de caracteres especiais, mas não são forçados a corresponder a um cliente já existente — apenas recebem a sinalização `cliente_fora_padrao = True`. Isso evita fundir identidades por engano, mas como efeito colateral, esses registros aparecem como um "cliente" separado na segmentação.

**`np.std` vs `.std()` do Pandas:** o desvio padrão calculado com `np.std()` usa `ddof=0` por padrão, enquanto `pandas.Series.std()` usa `ddof=1` — os valores podem divergir ligeiramente, o que é esperado.

---

## 🎥 Vídeo de Demonstração

[inserir o link do Google Drive ou do YouTube aqui]

---

Projeto desenvolvido por Alex Martins para o curso Carreira Tech (SCTEC) — Desenvolvimento de IA para Análise Preditiva, Módulo 01, Semana 08.
