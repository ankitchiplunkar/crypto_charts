from datetime import datetime, timedelta
from .constants import (
    BIGQUERY_PUBLIC,
    ETHEREUM_DATASET
)

YESTERDAY = datetime.strftime(datetime.now() - timedelta(1), '%Y-%m-%d')


def query_contract_logs(address: str, limit: int = 10, date=YESTERDAY) -> str:
    query = f"SELECT * FROM {BIGQUERY_PUBLIC}.{ETHEREUM_DATASET}.logs WHERE address='{address.lower()}'"
    query_with_date_filter = filter_date(query, date)
    return add_limit(query_with_date_filter, limit)


def add_limit(query: str, limit: int) -> str:
    if limit is None:
        return query
    else:
        return f"{query} LIMIT {limit}"


def filter_date(query: str, date: str) -> str:
    if date is None:
        return query
    else:
        return f"{query} AND DATE(block_timestamp) = '{date}'"
