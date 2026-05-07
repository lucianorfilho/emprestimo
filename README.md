# Projeto Final - Previsão de Aprovação de Empréstimo

## Problema (Justificativa)
Bancos e instituições financeiras recebem diariamente diversas solicitações de empréstimo. Avaliar manualmente cada pedido é caro e demorado.
O objetivo deste projeto é construir um modelo de classificação binária que, dado o perfil do solicitante, preveja se o empréstimo será aprovado ou recusado, auxiliando o processo de triagem.

**Tipo de problema:** Classificação binária supervisionada
**Variável‑alvo:** loan_status (1 = Aprovado, 0 = Recusado)
**Métricas:** Accuracy, F1-Score, ROC AUC  
**Objetivo de negócio:** priorizar análises para clientes mais propensos a aprovação, reduzindo tempo e custo operacional.

## Dataset
- **Fonte:** Kaggle — Loan Prediction Problem Dataset
- **Link:** https://www.kaggle.com/datasets/altruistdelhite04/loan-prediction-problem-dataset
- **Tamanho:** ~614 registros, 13 colunas

## Stack
Supabase → DuckDB → DVC/DagsHub → MLflow → Docker → Render → Streamlit

```mermaid
graph LR
    subgraph Ingênção e Armazenamento
        A[Dataset Kaggle] --> B[(Supabase)]
    end

    subgraph Processamento e Versionamento
        B --> C{DuckDB}
        C --> D[Parquet em data/processed]
        D --> E[DVC + DagsHub]
    end

    subgraph Modelagem e Registro
        E --> F[Treinamento + MLflow]
        F --> G[Modelo Serializado]
    end

    subgraph Deploy e Interface
        G --> H[Docker]
        H --> I[Render]
        I --> J[Streamlit App]
    end

    style A fill:#f9f,stroke:#333,stroke-width:2px
    style J fill:#00ff00,stroke:#333,stroke-width:2px
    style B fill:#3ecf8e,stroke:#333
```


### 📁 Estrutura do Projeto

```text
projeto-final/
├── data/               # Dados versionados via DVC
│   ├── raw/
│   └── processed/
├── notebooks/          # EDA exploratória
├── src/
│   ├── ingestion.py    # Ingestão Supabase -> Parquet
│   ├── preprocessing.py # Feature engineering com DuckDB
│   ├── train.py        # Treinamento + MLflow
│   └── predict.py      # Função de inferência
├── app/
│   └── streamlit_app.py # Interface Streamlit
├── models/             # Modelo final (.pkl)
├── Dockerfile
├── requirements.txt
├── dvc.yaml
├── .env                # Credenciais (não versionado)
├── .gitignore
└── README.md
