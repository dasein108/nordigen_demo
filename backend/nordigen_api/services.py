import asyncio
import logging
from datetime import datetime
from enum import Enum
from functools import lru_cache, partial
from typing import Dict, List, Literal, Optional, Union
from uuid import uuid4

from asgiref.sync import async_to_sync, sync_to_async
from django.core.exceptions import ObjectDoesNotExist
from django.forms.models import model_to_dict
from nordigen import NordigenClient
from nordigen.types import Institutions, RequisitionDto

from .config import (backend_url, institution_connected_url_path, loop,
                     nordigen_secret_id, nordigen_secret_key)
from .models import UserAccount, UserRequisition


class AccountDataType(Enum):
    DETAILS = "details"
    TRANSACTIONS = "transactions"
    BALANCES = "balances"


class NordigenServices(object):
    refresh_token = None
    token_data: Dict[str, str]

    def __init__(self):
        self.client: Optional[NordigenClient] = None

        self.init()

    def init(self):
        self.client = NordigenClient(
            secret_id=nordigen_secret_id, secret_key=nordigen_secret_key
        )
        self.token_data = self.client.generate_token()

    def _get_user_accounts(self, user_id: str) -> List[UserAccount]:
        return UserAccount.objects.filter(
            requisition=UserRequisition.objects.filter(
                user_id=user_id, status=UserRequisition.RequisitionStatus.SUCCESS
            ).get()
        ).all()

    def _wrap_account_data(
        self, account_id, data_type: AccountDataType, data: Union[dict, List]
    ):
        return {"id": account_id, **data, "type": data_type.value}

    @lru_cache
    def get_institutions(self, country: Optional[str]) -> List[Institutions]:
        institutions = self.client.institution.get_institutions(country)
        return institutions

    @lru_cache
    def get_institution(self, institution_id: str) -> Institutions:
        institution = self.client.institution.get_institution_by_id(institution_id)
        return institution

    def start_auth_institution(
        self, institution_id: str, user_id: str
    ) -> RequisitionDto:
        reference_id = str(uuid4())
        institution = self.get_institution(institution_id)
        redirect_uri = (
            f"{backend_url}api/{institution_connected_url_path}/{reference_id}"
        )

        data = self.client.initialize_session(
            institution_id=institution_id,
            redirect_uri=redirect_uri,
            reference_id=reference_id,
        )

        req = UserRequisition.objects.create(
            requisition_id=data.requisition_id,
            institution_id=institution_id,
            reference_id=reference_id,
            name=institution["name"],
            user_id=user_id,
        )
        req.save()

        return data

    def complete_auth_institution(self, reference_id: str, user_id: str) -> bool:
        try:
            item = UserRequisition.objects.filter(
                reference_id=reference_id, user_id=user_id
            ).get()
            item.status = UserRequisition.RequisitionStatus.SUCCESS
            item.connected_at = datetime.now()
            item.save()
            req = self.client.requisition.get_requisition_by_id(item.requisition_id)
            for a in req["accounts"]:
                user_account = UserAccount.objects.create(
                    requisition=item, account_id=a
                )
                user_account.save()

            return True
        except (ObjectDoesNotExist, Exception):
            return False

    @async_to_sync
    async def get_user_accounts(self, user_id: str):
        accounts = self._get_user_accounts(user_id)
        asyncio.set_event_loop(loop)
        data = await asyncio.gather(
            *[self.get_account_details(account.account_id) for account in accounts],
            *[self.get_account_balances(account.account_id) for account in accounts],
        )
        data_map = {(r["id"], r["type"]): r for r in data}
        result = []
        for account in accounts:
            account_id = account.account_id
            item = model_to_dict(account)
            item["name"] = account.requisition.name
            item["details"] = data_map.get(
                (account_id, AccountDataType.DETAILS.value), None
            )
            item["balances"] = data_map.get(
                (account_id, AccountDataType.BALANCES.value), None
            )
            result.append(item)

        return result

    @async_to_sync
    async def get_transactions(
        self,
        user_id: str,
        account_id: Optional[str] = None,
        date_from: Optional[str] = None,
        date_to: Optional[str] = None,
    ) -> List[dict]:
        accounts = self._get_user_accounts(user_id)

        account_ids = (
            [account_id]
            if account_id is not None
            else [account.account_id for account in accounts]
        )

        transactions_data = await asyncio.gather(
            *[
                self.get_account_transactions(acc_id, date_from, date_to)
                for acc_id in account_ids
            ]
        )

        account_institutions = {
            account.account_id: account.requisition.name for account in accounts
        }
        result = []
        for data in transactions_data:
            acc_id = data["id"]
            source = account_institutions[acc_id]
            for item in data["transactions"]["booked"]:
                item["source"] = source
                result.append(item)

        return sorted(result, key=lambda k: k["bookingDate"])

    @sync_to_async
    def get_account_metadata(self, account_id: str) -> dict:
        return self.client.account_api(id=account_id).get_metadata()

    @sync_to_async
    def get_account_details(self, account_id: str) -> dict:
        details = self.client.account_api(id=account_id).get_details()
        return self._wrap_account_data(
            account_id, AccountDataType.DETAILS, data=details["account"]
        )

    @sync_to_async
    def get_account_balances(self, account_id: str) -> dict:
        balances = self.client.account_api(id=account_id).get_balances()
        return self._wrap_account_data(
            account_id, AccountDataType.BALANCES, data=balances
        )

    @sync_to_async
    def get_account_transactions(
        self,
        account_id: str,
        date_from: Optional[str] = None,
        date_to: Optional[str] = None,
    ) -> dict:
        try:
            transactions = self.client.account_api(id=account_id).get_transactions(
                date_from, date_to
            )
            return self._wrap_account_data(
                account_id, AccountDataType.TRANSACTIONS, data=transactions
            )
        except Exception as e:
            logging.error(e)
            return self._wrap_account_data(
                account_id, AccountDataType.TRANSACTIONS, data={}
            )
