# Projeto Final - Previsão de Aprovação de Empréstimo

Dado o perfil financeiro e pessoal de um solicitante, prever se um empréstimo será aprovado ou recusado.


**Tipo:** Classificação binária supervisionada  
**Target:** `loan_status` → 1 = Aprovado / 0 = Recusado  
**Métricas:** Accuracy, F1-Score, ROC AUC  

## Dataset
- **Fonte:** Kaggle — Loan Prediction Problem Dataset
- **Tamanho:** ~614 registros, 13 colunas

## Stack
Supabase → DuckDB → DVC/DagsHub → MLflow → Docker → Render → Streamlit