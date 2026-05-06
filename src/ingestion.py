import os
import pandas as pd
from supabase import create_client
from dotenv import load_dotenv

def main():
    load_dotenv()

    url = os.getenv("SUPABASE_URL")
    key = os.getenv("SUPABASE_KEY")
    supabase = create_client(url, key)

    print(" Conectando ao Supabase...")
    response = supabase.table("loan_applications").select("*").execute()

    df = pd.DataFrame(response.data)
    print(f" {df.shape[0]} registros carregados com {df.shape[1]} colunas.")

    # Remover coluna de ID
    if "loan_id" in df.columns:
        df.drop(columns=["loan_id"], inplace=True)

    os.makedirs("data/raw", exist_ok=True)
    df.to_parquet("data/raw/loan_applications.parquet", index=False)
    print("Salvo em data/raw/loan_applications.parquet")

if __name__ == "__main__":
    main()