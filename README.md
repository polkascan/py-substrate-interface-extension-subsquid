# Python Substrate Interface: Subsquid Extension

[![Latest Version](https://img.shields.io/pypi/v/substrate-interface-subsquid.svg)](https://pypi.org/project/substrate-interface-subsquid/)
[![Supported Python versions](https://img.shields.io/pypi/pyversions/substrate-interface-subsquid.svg)](https://pypi.org/project/substrate-subsquid/)
[![License](https://img.shields.io/pypi/l/substrate-interface-subsquid.svg)](https://github.com/polkascan/py-substrate-interface-extension-subsquid/blob/master/LICENSE)


## Description
This extension enables [Substrate Interface](https://github.com/polkascan/py-substrate-interface) to use [Giant Squid indexes](https://docs.subsquid.io/giant-squid-api/statuses/) provided by [Subsquid](https://subsquid.io)   

## Installation
```bash
pip install substrate-interface-subsquid
```

## Initialization

```python
from substrateinterface import SubstrateInterface
from substrateinterface_subsquid.extensions import SubsquidExtension

substrate = SubstrateInterface(url="wss://rpc.polkadot.io")

substrate.register_extension(SubsquidExtension(url='https://squid.subsquid.io/gs-explorer-polkadot/graphql'))
```

## Usage

### Filter events

```python
events = substrate.extensions.filter_events(
    pallet_name="Balances", event_name="Transfer", account_id="12L9MSmxHY8YvtZKpA7Vpvac2pwf4wrT3gd2Tx78sCctoXSE", 
    page_size=25
)
```

### Filter extrinsics

```python
extrinsics = substrate.extensions.filter_extrinsics(
    ss58_address="12L9MSmxHY8YvtZKpA7Vpvac2pwf4wrT3gd2Tx78sCctoXSE",
    pallet_name="Balances", call_name="transfer_keep_alive", page_size=25
)
```

### Search block number

```python
block_datetime = datetime(2020, 7, 12, 0, 0, 0, tzinfo=timezone.utc)

block_number = substrate.extensions.search_block_number(block_datetime=block_datetime)
```

## License
https://github.com/polkascan/py-substrate-interface-extension-subsquid/blob/master/LICENSE
