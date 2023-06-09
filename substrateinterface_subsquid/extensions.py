#  Subsquid extension for Substrate Interface Library
#
#  Copyright 2018-2023 Stichting Polkascan (Polkascan Foundation).
#
#  Licensed under the Apache License, Version 2.0 (the "License");
#  you may not use this file except in compliance with the License.
#  You may obtain a copy of the License at
#
#  http://www.apache.org/licenses/LICENSE-2.0
#
#  Unless required by applicable law or agreed to in writing, software
#  distributed under the License is distributed on an "AS IS" BASIS,
#  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#  See the License for the specific language governing permissions and
#  limitations under the License.
#
from datetime import datetime

from substrateinterface.extensions import SearchExtension
from gql import gql, Client
from gql.transport.aiohttp import AIOHTTPTransport


class SubsquidExtension(SearchExtension):

    def __init__(self, url: str):
        self.url = url
        # Select your transport with a defined url endpoint
        transport = AIOHTTPTransport(url=url)

        # Create a GraphQL client using the defined transport
        self.client = Client(transport=transport, fetch_schema_from_transport=True)
        super().__init__()

    def filter_events(self, block_start: int = None, block_end: int = None, pallet_name: str = None,
                      event_name: str = None, account_id: str = None,
                      page_size: int = 10, page_number: int = 1) -> list:

        # Compose GraphQL query
        filters = []

        if block_start:
            filters.append(f"blockNumber_gte: {block_start}")

        if block_end:
            filters.append(f"blockNumber_lte: {block_end}")

        if pallet_name:
            filters.append(f'palletName_eq: "{pallet_name}"')

        if event_name:
            filters.append(f'eventName_eq: "{event_name}"')

        if account_id:
            filters.append('argsStr_containsAny: "0x' + self.substrate.ss58_decode(account_id) + '"')

        offset = page_size * (page_number - 1)

        query = gql(
            f"""
            query MyQuery {{
              events(orderBy: id_DESC, limit: {page_size}, where: {{{', '.join(filters)}}}, offset: {offset}) {{
                blockNumber
                indexInBlock
                extrinsic {{
                  indexInBlock
                }}
              }}
            }}
            """
        )
        result = self.client.execute(query)

        events = []
        current_block_number = None
        block_events = []

        for item in result['events']:

            if current_block_number != item['blockNumber']:
                # Retrieve actual events on-chain
                block_events = self.substrate.get_events(block_hash=self.substrate.get_block_hash(item['blockNumber']))
                current_block_number = item['blockNumber']

            events.append(block_events[item['indexInBlock']])
        return events

    def filter_extrinsics(self, block_start: int = None, block_end: int = None, ss58_address: str = None,
                          pallet_name: str = None, call_name: str = None, page_size: int = 10, page_number: int = 1) -> list:

        # Compose GraphQL query
        filters = []

        if block_start:
            filters.append(f"blockNumber_gte: {block_start}")

        if block_end:
            filters.append(f"blockNumber_lte: {block_end}")

        if pallet_name:
            if call_name:
                filters.append(f'mainCall: {{palletName_eq: "{pallet_name}", callName_eq: "{call_name}"}}')
            else:
                filters.append(f'mainCall: {{palletName_eq: "{pallet_name}"}}')

        if ss58_address:
            filters.append('signerPublicKey_eq: "0x' + self.substrate.ss58_decode(ss58_address) + '"')

        offset = page_size * (page_number - 1)

        query = gql(
            f"""
            query MyQuery {{
              extrinsics(limit: {page_size}, orderBy: id_DESC, where: {{{', '.join(filters)}}}, offset: {offset}) {{
                blockNumber
                indexInBlock
              }}
            }}
            """
        )

        result = self.client.execute(query)
        extrinsics = []
        for item in result['extrinsics']:
            # Retrieve actual extrinsics on-chain
            extrinsics.append(
                self.substrate.retrieve_extrinsic_by_identifier(f"{item['blockNumber']}-{item['indexInBlock']}")
            )
        return extrinsics

    def search_block_number(self, block_datetime: datetime, block_time: int = 6, **kwargs) -> int:
        """
        Search corresponding block number for provided `block_datetime`. the prediction tolerance is provided with
        `block_time`

        Parameters
        ----------
        block_datetime: datetime
        block_time: int
        kwargs

        Returns
        -------
        int
        """

        target_block_timestamp = block_datetime.strftime("%Y-%m-%dT%H:%M:%SZ")

        query = gql(
            f"""
            query {{
              blocks(where: {{timestamp_eq: "{target_block_timestamp}"}}) {{
                height
              }}
            }}
            """
        )

        result = self.client.execute(query)
        if len(result["blocks"]) > 0:
            return result["blocks"][0]["height"]
