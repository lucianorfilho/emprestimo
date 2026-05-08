import streamlit as st
import sys, os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from src.predict import load_model, predict

st.set_page_config(page_title="Aprovação de Empréstimo")
st.title("Previsão de Aprovação de Empréstimo")
st.markdown("Preencha os dados do solicitante para verificar se o empréstimo seria aprovado.")

@st.cache_resource
def get_model():
    return load_model()

model = get_model()

# Formulário dividido em 2 colunas
col1, col2 = st.columns(2)

with col1:
    gender = st.selectbox("Gênero", ["Male", "Female"])
    married = st.selectbox("É Casado?", ["Yes", "No"])
    dependents = st.selectbox("Nº de Dependentes", ["0", "1", "2", "3+"])
    education = st.selectbox("Possui Ensino Superior?", ["Graduate", "Not Graduate"])
    self_employed = st.selectbox("Autônomo?", ["No", "Yes"])
    property_area = st.selectbox("Área do Imóvel onde Reside", ["Urban", "Semiurban", "Rural"])

with col2:
    applicant_income = st.number_input("Renda do Solicitante (R$)", min_value=0, value=5000, step=500)
    coapplicant_income = st.number_input("Renda do Co-Solicitante (R$)", min_value=0, value=0, step=500)
    loan_amount = st.number_input("Valor do Empréstimo (em milhares)", min_value=1, value=100, step=5)
    loan_amount_term = st.number_input("Prazo (meses)", min_value=12, max_value=480, value=360, step=12)
    credit_history = st.selectbox("Histórico de Crédito OK?", [1, 0],
                                   format_func=lambda x: "Sim" if x == 1 else "Não")

# Features derivadas
total_income = applicant_income + coapplicant_income
income_to_loan_ratio = round(total_income / loan_amount, 2) if loan_amount > 0 else 0

st.info(f"Renda Total: R$ {total_income:,.2f} |  Razão Renda/Empréstimo: {income_to_loan_ratio}")

# Previsão
if st.button(" Verificar Aprovação", use_container_width=True):
    features = {
    "Gender": gender,
    "Married": married,
    "Dependents": dependents,
    "Education": education,
    "Self_Employed": self_employed,
    "ApplicantIncome": applicant_income,
    "CoapplicantIncome": coapplicant_income,
    "LoanAmount": loan_amount,
    "Loan_Amount_Term": loan_amount_term,
    "Credit_History": credit_history,
    "Property_Area": property_area,
    "total_income": total_income,
    "income_to_loan_ratio": income_to_loan_ratio
    }

    result = predict(model, features)

    if result["approved"]:
        st.success(f"**{result['label']}** — Probabilidade: {result['probability']*100:.1f}%")
    else:
        st.error(f"**{result['label']}** — Probabilidade de aprovação: {result['probability']*100:.1f}%")

    st.progress(result["probability"])