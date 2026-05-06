import os
import pickle
import pandas as pd
import mlflow
import mlflow.sklearn
from dotenv import load_dotenv

from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.impute import SimpleImputer
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier
from sklearn.metrics import accuracy_score, f1_score, roc_auc_score

def build_preprocessor():
    numeric_features = [
        "ApplicantIncome", "CoapplicantIncome", "LoanAmount",
        "Loan_Amount_Term", "Credit_History",
        "total_income", "income_to_loan_ratio"
    ]
    categorical_features = [
        "Gender", "Married", "Dependents",
        "Education", "Self_Employed", "Property_Area"
    ]

    numeric_transformer = Pipeline(steps=[
        ("imputer", SimpleImputer(strategy="median")),
        ("scaler", StandardScaler())
    ])

    categorical_transformer = Pipeline(steps=[
        ("imputer", SimpleImputer(strategy="most_frequent")),
        ("onehot", OneHotEncoder(handle_unknown="ignore"))
    ])

    return ColumnTransformer(transformers=[
        ("num", numeric_transformer, numeric_features),
        ("cat", categorical_transformer, categorical_features)
    ])

def evaluate(model, X_test, y_test):
    y_pred = model.predict(X_test)
    y_proba = model.predict_proba(X_test)[:, 1]
    return {
        "accuracy": round(accuracy_score(y_test, y_pred), 4),
        "f1_score": round(f1_score(y_test, y_pred), 4),
        "roc_auc": round(roc_auc_score(y_test, y_proba), 4)
    }

def main():
    load_dotenv()

    # Configurar MLflow → DagsHub
    dagshub_user = os.getenv("DAGSHUB_USER")
    dagshub_repo = os.getenv("DAGSHUB_REPO")
    mlflow.set_tracking_uri(
        f"https://dagshub.com/{dagshub_user}/{dagshub_repo}.mlflow"
    )
    mlflow.set_experiment("emprestimo")

    # Carregar dados
    df = pd.read_parquet("data/processed/loan_processed.parquet")
    X = df.drop(columns=["loan_status"])
    y = df["loan_status"]

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y
    )

    preprocessor = build_preprocessor()

    # 3 modelos para comparar
    models = {
        "LogisticRegression": LogisticRegression(max_iter=1000, random_state=42),
        "RandomForest": RandomForestClassifier(n_estimators=100, random_state=42),
        "GradientBoosting": GradientBoostingClassifier(n_estimators=100, random_state=42)
    }

    best_model = None
    best_auc = 0
    best_model_name = ""

    for model_name, classifier in models.items():
        with mlflow.start_run(run_name=model_name):

            pipeline = Pipeline(steps=[
                ("preprocessor", preprocessor),
                ("classifier", classifier)
            ])

            pipeline.fit(X_train, y_train)
            metrics = evaluate(pipeline, X_test, y_test)

            # Logar no MLflow
            mlflow.log_param("model", model_name)
            mlflow.log_param("test_size", 0.2)
            mlflow.log_metric("accuracy", metrics["accuracy"])
            mlflow.log_metric("f1_score", metrics["f1_score"])
            mlflow.log_metric("roc_auc", metrics["roc_auc"])
            mlflow.sklearn.log_model(pipeline, artifact_path="model")

            print(f"📊 {model_name}: {metrics}")

            if metrics["roc_auc"] > best_auc:
                best_auc = metrics["roc_auc"]
                best_model = pipeline
                best_model_name = model_name

    print(f"\n Melhor modelo: {best_model_name} — ROC AUC: {best_auc}")

    # Salvar melhor modelo localmente
    os.makedirs("models", exist_ok=True)
    with open("models/best_model.pkl", "wb") as f:
        pickle.dump(best_model, f)
    print(" Modelo salvo em models/best_model.pkl")

if __name__ == "__main__":
    main()