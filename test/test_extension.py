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

import unittest
from datetime import datetime, timezone
from os import environ

from substrateinterface import SubstrateInterface
from substrateinterface_subsquid.extensions import SubsquidExtension

POLKADOT_NODE_URL = environ.get('SUBSTRATE_NODE_URL_POLKADOT') or 'wss://rpc.polkadot.io'
SUBSQUID_GIANTSQUID_URL = environ.get('SUBSQUID_GIANTSQUID_URL') or 'https://squid.subsquid.io/gs-explorer-polkadot/graphql'


class TestExtension(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.substrate = SubstrateInterface(url=POLKADOT_NODE_URL)
        cls.substrate.register_extension(SubsquidExtension(url=SUBSQUID_GIANTSQUID_URL))

    def test_filter_events(self):

        events = self.substrate.extensions.filter_events(
            pallet_name="Balances", event_name="Transfer",
            account_id="12L9MSmxHY8YvtZKpA7Vpvac2pwf4wrT3gd2Tx78sCctoXSE",
            page_size=5
        )

        self.assertGreater(len(events), 0)

    def test_filter_extrinsics(self):

        extrinsics = self.substrate.extensions.filter_extrinsics(
            ss58_address="12L9MSmxHY8YvtZKpA7Vpvac2pwf4wrT3gd2Tx78sCctoXSE",
            pallet_name="Balances", call_name="transfer_keep_alive", page_size=5
        )

        self.assertGreater(len(extrinsics), 0)

    def test_search_block_number(self):
        block_datetime = datetime(2020, 7, 12, 0, 0, 0, tzinfo=timezone.utc)

        block_number = self.substrate.extensions.search_block_number(block_datetime=block_datetime)

        self.assertGreaterEqual(block_number, 665270)
        self.assertLessEqual(block_number, 665280)


if __name__ == '__main__':
    unittest.main()
