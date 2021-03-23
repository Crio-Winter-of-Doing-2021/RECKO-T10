import json
import requests
import webbrowser
import base64

from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseBadRequest, HttpResponseServerError, HttpResponseRedirect
import datetime
from intuitlib.client import AuthClient
from intuitlib.enums import Scopes
import requests
import json
# Create your views here.
from django.core.cache import cache

from xero import Xero
from xero.auth import OAuth2Credentials
from xero.constants import XeroScopes




client_id = '53CA5E526A9C41AB91C216CC29C0A535'
client_secret = 'vh7Kar4K4FvGrbugjfzzEPCUvLD2t2b-p9SmLIR5cng30FgH'
redirect_url = 'http://localhost:8000/xero_callback'

scope = 'offline_access accounting.journals.read'
b64_id_secret = base64.b64encode(
    bytes(client_id + ':' + client_secret, 'utf-8')).decode('utf-8')

client_id1 = "AB1CT9l9mtRkuGnS9w9hASGJtnHTL0JhDggPIPM3gJy2W6gQAy"
client_secret1 = "GG6jhkVesyPyowXBYg9UVlGO1eJF3CUvEhXxfCiS"
redirect_uri1 = "http://localhost:8000/callback"
environment = "sandbox"
scopes = [
    Scopes.ACCOUNTING,
]
auth_client = AuthClient(client_id1, client_secret1, redirect_uri1,
                         environment)


def hello(request):
    url = auth_client.get_authorization_url(scopes)
    return redirect(url)


def callback(request):
    auth_code = request.GET.get('code', None)
    realm_id = request.GET.get('realmId', None)
    print("Auth code", " ", auth_code)
    print("Relam id", " ", realm_id)
    auth_client.get_bearer_token(auth_code, realm_id=realm_id)
    access_token = auth_client.access_token
    refresh_token = auth_client.refresh_token
    print(refresh_token)
    
    """
    minoversion = 57
    auth_header = 'Bearer {0}'.format(access_token)
    base_url = 'https://sandbox-quickbooks.api.intuit.com'

    url = "https://{0}/v3/company/{1}/journalentry/8?minorversion=57".format(
        base_url, realm_id)

    payload = "{\n  \"Line\": [\n    {\n      \"Id\": \"0\",\n      \"Description\": \"nov portion of rider insurance\",\n      \"Amount\": 100.0,\n      \"DetailType\": \"JournalEntryLineDetail\",\n      \"JournalEntryLineDetail\": {\n        \"PostingType\": \"Debit\",\n         \"AccountRef\": {\n                \"value\": \"39\",\n                \"name\": \"Opening Bal Equity\"\n              }\n      }\n    },\n    {\n      \"Description\": \"nov portion of rider insurance\",\n      \"Amount\": 100.0,\n      \"DetailType\": \"JournalEntryLineDetail\",\n      \"JournalEntryLineDetail\": {\n        \"PostingType\": \"Credit\",\n              \"AccountRef\": {\n                \"value\": \"44\",\n                \"name\": \"Notes Payable\"\n              }\n\n      }\n    }\n  ]\n}"
    headers = {
        'Authorization': auth_header,
        'Accept': 'application/json',
        'Content-Type': 'application/text'
    }
    """
    base_url = 'https://sandbox-quickbooks.api.intuit.com'

    url = '{0}/v3/company/{1}//journalentry/1?minorversion=57'.format(
        base_url, realm_id)
    auth_header = 'Bearer {0}'.format(access_token)
    headers = {
        'Authorization': auth_header,
        'Accept': 'application/json',
        'Content-Type': 'application/json'
    }
    payload = "{\n  \"Line\": [\n    {\n      \"Id\": \"0\",\n      \"Description\": \"nov portion of rider insurance\",\n      \"Amount\": 100.0,\n      \"DetailType\": \"JournalEntryLineDetail\",\n      \"JournalEntryLineDetail\": {\n        \"PostingType\": \"Debit\",\n         \"AccountRef\": {\n                \"value\": \"39\",\n                \"name\": \"Opening Bal Equity\"\n              }\n      }\n    },\n    {\n      \"Description\": \"nov portion of rider insurance\",\n      \"Amount\": 100.0,\n      \"DetailType\": \"JournalEntryLineDetail\",\n      \"JournalEntryLineDetail\": {\n        \"PostingType\": \"Credit\",\n              \"AccountRef\": {\n                \"value\": \"44\",\n                \"name\": \"Notes Payable\"\n              }\n\n      }\n    }\n  ]\n}"

    """
    response = requests.request("GET", url, headers=headers, data=payload)

    print(response.text.encode('utf8'))
    
    body = {
        "Line": [{
            "JournalEntryLineDetail": {
                "PostingType": "Debit",
                "AccountRef": {
                    "name": "Opening Bal Equity",
                    "value": "39"
                }
            },
            "DetailType": "JournalEntryLineDetail",
            "Amount": 100.0,
            "Id": "0",
            "Description": "nov portion of rider insurance"
        }, {
            "JournalEntryLineDetail": {
                "PostingType": "Credit",
                "AccountRef": {
                    "name": "Notes Payable",
                    "value": "44"
                }
            },
            "DetailType": "JournalEntryLineDetail",
            "Amount": 100.0,
            "Description": "nov portion of rider insurance"
        }]
    }
    """

    response = requests.get(url, headers=headers, data=payload)#json.dumps(body))
    
    return HttpResponse(response.text.encode('utf8'))


def xero(request):
    auth_url = ('''https://login.xero.com/identity/connect/authorize?''' +
                '''response_type=code''' + '''&client_id=''' + client_id +
                '''&redirect_uri=''' + redirect_url + '''&scope=''' + scope +
                '''&state=123''')
    return redirect(auth_url)


def xero_callback(request):
    auth_code = request.GET.get('code', None)
    print(auth_code)
    exchange_code_url = 'https://identity.xero.com/connect/token'
    response = requests.post(
        exchange_code_url,
        headers={'Authorization': 'Basic ' + b64_id_secret},
        data={
            'grant_type': 'authorization_code',
            'code': auth_code,
            'redirect_uri': redirect_url
        })
    json_response = response.json()
    print(json_response)

    refresh_token = json_response['refresh_token']
    access_token = json_response['access_token']
    print(refresh_token)

    connections_url = 'https://api.xero.com/connections'
    response = requests.get(connections_url,
                            headers={
                                'Authorization': 'Bearer ' + access_token,
                                'Content-Type': 'application/json'
                            })
    json_response = response.json()
    print(json_response)

    for tenants in json_response:
        json_dict = tenants

    tid = json_dict['tenantId']
    print("\n ACCESS TOKEN ", " ", access_token)
    print("\n Tenant id", " ", tid)

    url = 'https://api.xero.com/api.xro/2.0/Journals'
    response = requests.get(url,
                            headers={
                                'Authorization': 'Bearer ' + access_token,
                                'Xero-Tenant-Id': tid,
                                'Accept': 'application/json'
                            })
    print(response.json())
    return HttpResponse(response.text.encode('utf8'))



"""
def get_Description(self, obj):
        if hasattr(obj, 'Description'):
            return "No Description"
        else:
            return obj.Description

    def get_TaxType(self, obj):
        if hasattr(obj, 'TaxType'):
            return "No Tax Type"
        else:
            return obj.TaxType

    def get_TaxName(self, obj):
        if hasattr(obj, 'TaxName'):
            return "No Tax Name"
        else:
            return obj.TaxType

            """