from datetime import datetime, timedelta
from .constants import (
    BIGQUERY_PUBLIC,
    ETHEREUM_DATASET
)

START_DATE = datetime.strftime(datetime.now() - timedelta(1), '%Y-%m-%d')
END_DATE = datetime.strftime(datetime.now(), '%Y-%m-%d')


def query_contract_logs(address: str, limit: int = 10, start_date: str = START_DATE, end_date: str = END_DATE) -> str:
    query = f"SELECT * FROM {BIGQUERY_PUBLIC}.{ETHEREUM_DATASET}.logs WHERE address='{address.lower()}'"
    query_with_date_filter = filter_date(
        query, start_date=start_date, end_date=end_date)
    return add_limit(query_with_date_filter, limit)


def add_limit(query: str, limit: int) -> str:
    if limit is None:
        return query
    else:
        return f"{query} LIMIT {limit}"


def filter_date(query: str, start_date: str, end_date: str) -> str:
    start_part = ""
    end_part = ""
    if start_date is not None:
        start_part = f" AND DATE(block_timestamp) >= '{start_date}'"
    if end_date is not None:
        end_part = f" AND DATE(block_timestamp) <= '{end_date}'"
    return f"{query}{start_part}{end_part}"
