import asyncio
from typing import Any, Dict, List, TypedDict, Union

from asgiref.sync import async_to_sync
from django.http import (HttpRequest, HttpResponse, HttpResponseRedirect,
                         JsonResponse)
from django.shortcuts import redirect, render

from .config import hardcoded_user_id, frontend_url
from .services import NordigenServices

# Create your views here.


class Results(TypedDict):
    results: Union[Dict[str, Any], List]


service = NordigenServices()


def connect_bank(request, institution_id: str):
    user_id = hardcoded_user_id  # TODO: request.user.id
    auth_data = service.start_auth_institution(institution_id, user_id)
    response = HttpResponseRedirect(auth_data.link)
    return response


def process_bank(request, reference_id: str):
    # TODO: Can be obtained from request.GET['ref']
    user_id = hardcoded_user_id  # TODO: request.user.id

    service.complete_auth_institution(reference_id, user_id)
    response = HttpResponseRedirect(frontend_url)
    # response.set_cookie('', '', 5, secure=True, httponly=True)

    return response


def user_accounts(request):
    user_id = hardcoded_user_id  # TODO: request.user.id
    data = service.get_user_accounts(user_id)
    return JsonResponse(Results(results=data))


def latest_transactions(request):
    user_id = hardcoded_user_id  # TODO: request.user.id
    data = service.get_transactions(user_id)
    return JsonResponse(Results(results=data))


def transactions(request, account_id: str):
    user_id = hardcoded_user_id  # TODO: request.user.id
    data = service.get_transactions(user_id, account_id)
    return JsonResponse(Results(results=data))


def institutions(request):
    data = service.get_institutions("LV")
    return JsonResponse(Results(results=data))
