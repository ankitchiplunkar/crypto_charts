import os
import json
from web3._utils.abi import (
    abi_to_signature,
    filter_by_type,
    get_abi_input_types,
    get_abi_input_names,
    get_indexed_event_inputs,
    exclude_indexed_event_inputs,
)
from eth_utils import (
    event_abi_to_log_topic,
    to_hex,
    to_bytes,
)
from hexbytes import HexBytes
from eth_abi import (
    decode_abi,
    decode_single
)
import itertools


def get_abi(file_path):
    with open(file_path) as json_file:
        return json.load(json_file)


def get_event_list_by_protocol(protocol):
    events = {}
    for contract_name in os.listdir(f'../abi/{protocol}'):
        file_path = f'../abi/{protocol}/{contract_name}'
        abi = get_abi(file_path)['abi']
        events_abi = filter_by_type('event', abi)
        for event_abi in events_abi:
            events.update({
                to_hex(event_abi_to_log_topic(event_abi)): {
                    'name': event_abi['name'],
                    'inputs': event_abi['inputs'],
                    'anonymous': event_abi['anonymous'],
                    'signature': abi_to_signature(event_abi),
                    'abi': event_abi}
            })
    return events


def get_event_name(log_data, events):
    if len(log_data['topics']) > 0:
        return events[log_data['topics'][0]]['name']
    else:
        return events[log_data['data'][:32]]['name']


def get_event_abi(log_data, events):
    if len(log_data['topics']) > 0:
        return events[log_data['topics'][0]]['abi']
    else:
        return events[log_data['data'][:32]]['abi']


def decode_log(log_data, events):
    topic_inputs = get_indexed_event_inputs(log_data['abi'])
    topic_types = get_abi_input_types({'inputs': topic_inputs})
    topic_names = get_abi_input_names({'inputs': topic_inputs})
    topic_data = [HexBytes(topic) for topic in log_data['topics'][1:]]
    decoded_topics = [
        decode_single(topic_type, topic_data)
        for topic_type, topic_data
        in zip(topic_types, topic_data)
    ]
    data_inputs = exclude_indexed_event_inputs(log_data['abi'])
    data_types = get_abi_input_types({'inputs': data_inputs})
    data_names = get_abi_input_names({'inputs': data_inputs})
    decoded_data = decode_abi(data_types, HexBytes(log_data['data']))
    return dict(itertools.chain(
        zip(topic_names, decoded_topics),
        zip(data_names, decoded_data),
    ))
