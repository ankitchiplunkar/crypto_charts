import pandas as pd


def unwrap_decoded_events(decoded_logs, event_name):
    decoded_events = []
    df = decoded_logs[decoded_logs['name'] == event_name]
    for i, row in df.iterrows():
        temp_dict = {
            'log_index': row['log_index'],
            'transaction_hash': row['transaction_hash'],
            'transaction_index': row['transaction_index'],
            'block_timestamp': row['block_timestamp'],
            'block_number': row['block_number'],
        }
        for name, value in row['decoded'].items():
            if 'update' in name.lower():
                temp_dict.update({name: parse_updates(value)})
            else:
                temp_dict.update({name: value})
        decoded_events.append(temp_dict)
    return pd.DataFrame(decoded_events)


def parse_updates(updates):
    result = 0
    for update in updates:
        result += parse_update(update)
    return result


def parse_update(update):
    if update[0] is True:
        return update[1]
    elif update[0] is False:
        return -1*update[1]
