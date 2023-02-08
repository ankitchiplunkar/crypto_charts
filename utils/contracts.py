new_contracts = """
select transaction_hash, deployer, contract, block_number, eth_balance/pow(10, 18) as balance from
(SELECT transaction_hash, from_address as deployer, to_address as contract, block_number  FROM `bigquery-public-data.crypto_ethereum.traces` 
WHERE DATE(block_timestamp) = "2022-12-28" 
AND trace_type = 'create'
and status = 1) as c
inner join `bigquery-public-data.crypto_ethereum.balances` as b
on c.contract = b.address
order by balance desc
LIMIT 10
"""