import requests
import pandas as pd


def get_data(token, to_timestamp):
    """ Query the API for 2000 days historical price data starting from "date". """
    url = f"https://min-api.cryptocompare.com/data/histoday?fsym={token}&tsym=USD&limit=2000&toTs={to_timestamp}"
    r = requests.get(url)
    ipdata = r.json()
    return ipdata


def get_token_price(token, from_date, to_date):
    """ Get historical price data between two dates. """
    from_timestamp = pd.to_datetime(from_date).timestamp()
    to_timestamp = pd.to_datetime(to_date).timestamp()
    date = to_timestamp
    holder = []
    # While the earliest date returned is later than the earliest date requested, keep on querying the API
    # and adding the results to a list.
    while date > from_timestamp:
        data = get_data(token, date)
        holder.append(pd.DataFrame(data['Data']))
        date = data['TimeFrom']
    # Join together all of the API queries in the list.
    df = pd.concat(holder, axis=0)
    # Remove data points from before from_date
    df = df[df['time'] > from_timestamp]
    # Convert to timestamp to readable date format
    df['time'] = pd.to_datetime(df['time'], unit='s', utc=True)
    # Make the DataFrame index the time
    df.set_index('time', inplace=True)
    # And sort it so its in time order
    df.sort_index(ascending=False, inplace=True)
    return df


def get_prices(token_list, from_date, to_date):
    temp_prices = []
    for token in token_list:
        token_price = get_token_price(token, from_date, to_date)
        token_price['token'] = token
        token_price = token_price.reset_index().rename(
            columns={'time': 'date'})
        temp_prices.append(token_price)
    return pd.concat(temp_prices)
