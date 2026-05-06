import duckdb
import os

def main():
    os.makedirs("data/processed", exist_ok=True)
    con = duckdb.connect()

    # Carregar dados brutos
    con.execute("""
        CREATE TABLE loan_raw AS
        SELECT * FROM read_parquet('data/raw/loan_applications.parquet');
    """)

    print(" Amostra bruta:")
    print(con.execute("SELECT * FROM loan_raw LIMIT 3").df())

    # Transformações via SQL
    con.execute("""
        CREATE TABLE loan_processed AS
        SELECT
            Gender,
            Married,
            Dependents,
            Education,
            Self_Employed,
            ApplicantIncome,
            CoapplicantIncome,
            CAST(LoanAmount AS DOUBLE) AS LoanAmount, -- Converte para número aqui
            Loan_Amount_Term,
            Credit_History,
            Property_Area,

            -- Features derivadas
            (ApplicantIncome + CoapplicantIncome) AS total_income,
            ROUND(
                (ApplicantIncome + CoapplicantIncome) / 
                NULLIF(CAST(LoanAmount AS DOUBLE), 0), 2 -- Garante que a divisão seja entre números
            ) AS income_to_loan_ratio,

            -- Target binário
            CASE WHEN Loan_Status = 'Y' THEN 1 ELSE 0 END AS loan_status

        FROM loan_raw
        WHERE
            Gender IS NOT NULL
            AND Married IS NOT NULL
            -- Filtra valores que não podem ser convertidos ou são nulos
            AND TRY_CAST(LoanAmount AS DOUBLE) IS NOT NULL 
            AND Credit_History IS NOT NULL
            AND Loan_Status IS NOT NULL;
    """)

    print(" Amostra processada:")
    print(con.execute("SELECT * FROM loan_processed LIMIT 3").df())

    # Salvar como Parquet
    con.execute("""
        COPY loan_processed
        TO 'data/processed/loan_processed.parquet'
        (FORMAT 'parquet');
    """)

    print(" Salvo em data/processed/loan_processed.parquet")

if __name__ == "__main__":
    main()