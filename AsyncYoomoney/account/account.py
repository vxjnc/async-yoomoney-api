import aiohttp
import json
from typing import TYPE_CHECKING, List

from AsyncYoomoney.account.balance_details import BalanceDetails
from AsyncYoomoney.account.card import Card
from AsyncYoomoney.exceptions import InvalidToken

class Account:

    @classmethod
    async def create(cls,
                 base_url: str = None,
                 token: str = None,
                 method: str = None,
                 session: aiohttp.ClientSession = None
                 ):
        self = cls()
        self.__private_method = method

        self.__private_base_url = base_url
        self.__private_token = token

        self.session = session

        data = await self._request()

        if len(data) != 0:
            self.account = data['account']
            self.balance = data['balance']
            self.currency = data['currency']
            self.account_status = data['account_status']
            self.account_type = data['account_type']

            self.balance_details = BalanceDetails()
            if 'balance_details' in data:
                if 'available' in data['balance_details']:
                    self.balance_details.available = float(data['balance_details']['available'])
                if 'blocked' in data['balance_details']:
                    self.balance_details.blocked = float(data['balance_details']['blocked'])
                if 'debt' in data['balance_details']:
                    self.balance_details.debt = float(data['balance_details']['debt'])
                if 'deposition_pending' in data['balance_details']:
                    self.balance_details.deposition_pending = float(data['balance_details']['deposition_pending'])
                if 'total' in data['balance_details']:
                    self.balance_details.total = float(data['balance_details']['total'])
                if 'hold' in data['balance_details']:
                    self.balance_details.hold = float(data['balance_details']['hold'])

            self.cards_linked = []
            if 'cards_linked' in data:
                for card_linked in data['cards_linked']:
                    card = Card(pan_fragment=card_linked['pan_fragment'], type=card_linked['type'])
                    self.cards_linked.append(card)
        else:
            raise InvalidToken()

        return self

    async def _request(self) -> aiohttp.ClientResponse:

        access_token = str(self.__private_token)
        url = self.__private_base_url + self.__private_method

        headers = {
            'Authorization': 'Bearer ' + str(access_token),
            'Content-Type': 'application/x-www-form-urlencoded'
        }

        if self.session:
            async with self.session.post(url, headers=headers) as response:
                return await response.json()
            
        async with aiohttp.ClientSession() as session:
            async with session.post(url, headers=headers) as response:
                return await response.json()