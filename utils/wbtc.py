import pandas as pd
from .events import unwrap_decoded_events

MINTER_ADDRESS = '0x0000000000000000000000000000000000000000'


def build_token_supply(df, decimals):
    mints = unwrap_decoded_events(df, 'Mint')
    mints['value'] = mints['amount']
    burns = unwrap_decoded_events(df, 'Burn')
    burns['value'] = -1*burns['value']
    change = pd.concat([mints[['block_timestamp', 'value']],
                        burns[['block_timestamp', 'value']]])
    change['block_timestamp'] = pd.to_datetime(change['block_timestamp'])
    total_supply = change.sort_values(
        by=['block_timestamp']).set_index('block_timestamp').cumsum()
    total_supply = total_supply['value']/10**decimals
    return total_supply


def build_balance_diff(transfer, decimals):
    senders = transfer[['from', 'value', 'block_timestamp', 'block_number']]
    senders['address'] = senders['from']
    senders['value'] = -1*senders['value']
    senders = senders.drop(columns=['from'])
    receivers = transfer[['to', 'value', 'block_timestamp', 'block_number']]
    receivers['address'] = receivers['to']
    receivers = receivers.drop(columns=['to'])
    balancediff = pd.concat([senders, receivers])
    balancediff['value'] = balancediff['value']/10**decimals
    balancediff = balancediff.groupby(
        ['block_timestamp', 'block_number', 'address']).sum().reset_index()
    return balancediff[balancediff['address'] != MINTER_ADDRESS]


def get_balance(balance_diff, date):
    bd = balance_diff[balance_diff['block_timestamp'] < date]
    balance = bd.groupby('address')['value'].sum().reset_index()
    balance['date'] = date
    return balance[balance['value'] > 0]


def get_value_usd(df, price, decimals, value_column='value'):
    df['date'] = pd.to_datetime(df['block_timestamp']).dt.date
    df['date'] = pd.to_datetime(df['date'], utc=True)
    df = df.merge(price, on=['date'])
    df['value_usd'] = df['value']*df['close']/10**decimals
    return df
