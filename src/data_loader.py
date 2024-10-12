from typing import Any, Dict, List

import pandas as pd


def load_transactions_from_csv(file_path: str) -> List[Dict[str, Any]]:
    """Загружает данные о финансовых транзакциях из CSV-файла."""
    try:
        df = pd.read_csv(file_path)
        transactions = df.to_dict(orient="records")
        return transactions
    except FileNotFoundError:
        return []
    except pd.errors.EmptyDataError:
        return []
    except pd.errors.ParserError:
        return []


def load_transactions_from_excel(file_path: str) -> List[Dict[str, Any]]:
    """Загружает данные о финансовых транзакциях из Excel-файла."""
    try:
        df = pd.read_excel(file_path)
        transactions = df.to_dict(orient="records")
        return transactions
    except FileNotFoundError:
        return []
    except ValueError:
        return []
