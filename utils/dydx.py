import pandas as pd
MARKET_TOKEN_MAP = {
    0: "ETH",
    1: "SAI",
    2: "USDC",
    3: "DAI",
}

MARKET_DECIMAL_MAP = {
    0: 18,
    1: 18,
    2: 6,
    3: 18,
}


def get_token(market):
    return MARKET_TOKEN_MAP[market]


def get_decimals(market):
    return MARKET_DECIMAL_MAP[market]


def get_value_usd(df, price, market_column='market', value_column='value'):
    df['date'] = pd.to_datetime(df['block_timestamp']).dt.date
    df['date'] = pd.to_datetime(df['date'], utc=True)
    df['token'] = df[market_column].apply(get_token)
    df['decimals'] = df[market_column].apply(get_decimals)
    df['value'] = df[value_column]/10**df['decimals']
    df = df.merge(price, on=['date', 'token'])
    df['value_usd'] = df['value']*df['close']
    return df


def remove_token(df, token, token_column='token'):
    return df[df[token_column] != token]
