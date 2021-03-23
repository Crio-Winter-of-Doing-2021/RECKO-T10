from intuitlib.client import AuthClient
from intuitlib.enums import Scopes


client_id="AB1CT9l9mtRkuGnS9w9hASGJtnHTL0JhDggPIPM3gJy2W6gQAy"
client_secret="GG6jhkVesyPyowXBYg9UVlGO1eJF3CUvEhXxfCiS"
redirect_uri="http://localhost:8000/"  #"https://developer.intuit.com/v2/OAuth2Playground/RedirectUrl"
environment="sandbox"
scopes = [
    Scopes.ACCOUNTING,
]

auth_client = AuthClient( client_id, client_secret, redirect_uri, environment )

url = auth_client.get_authorization_url(scopes)
print(url)





#########################################################################################################




client_id="AB1CT9l9mtRkuGnS9w9hASGJtnHTL0JhDggPIPM3gJy2W6gQAy"
client_secret="GG6jhkVesyPyowXBYg9UVlGO1eJF3CUvEhXxfCiS"
redirect_uri="http://localhost:8000/callback"  #"https://developer.intuit.com/v2/OAuth2Playground/RedirectUrl"
environment="sandbox"
scopes = [
    Scopes.ACCOUNTING,
]
auth_client = AuthClient( client_id, client_secret, redirect_uri, environment )


def hello(request):
    url = auth_client.get_authorization_url(scopes)
    return redirect(url)

def callback(request):
    auth_code = request.GET.get('code', None)
    realm_id = request.GET.get('realmId', None)
    print("Auth code"," ",auth_code)
    print("Relam id"," ",realm_id)
    auth_client.get_bearer_token(auth_code, realm_id=realm_id)
    access_token=auth_client.access_token
    refresh_token=auth_client.refresh_token
    print(refresh_token)


    base_url = 'https://sandbox-quickbooks.api.intuit.com'
    url = '{0}/v3/company/{1}/journalentry?minorversion=57'.format(base_url,realm_id)
    auth_header = 'Bearer {0}'.format(access_token)
    headers = {
    'Authorization': auth_header,
    'Accept': 'application/json',
    'Content-Type': 'application/json'
    }
    body={
        "Line": [
    {
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
    }, 
    {
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
    }
  ]
    }
    

    #payload="{\n  \"Line\": [\n    {\n      \"Id\": \"0\",\n      \"Description\": \"nov portion of rider insurance\",\n      \"Amount\": 100.0,\n      \"DetailType\": \"JournalEntryLineDetail\",\n      \"JournalEntryLineDetail\": {\n        \"PostingType\": \"Debit\",\n         \"AccountRef\": {\n                \"value\": \"39\",\n                \"name\": \"Opening Bal Equity\"\n              }\n      }\n    },\n    {\n      \"Description\": \"nov portion of rider insurance\",\n      \"Amount\": 100.0,\n      \"DetailType\": \"JournalEntryLineDetail\",\n      \"JournalEntryLineDetail\": {\n        \"PostingType\": \"Credit\",\n              \"AccountRef\": {\n                \"value\": \"44\",\n                \"name\": \"Notes Payable\"\n              }\n\n      }\n    }\n  ]\n}"
    response = requests.post(url, headers=headers,data=json.dumps(body))
    return HttpResponse(response)

###########################################################################################################################

"""
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

   

    response = requests.get(url, headers=headers, data=payload)#json.dumps(body))
    
    return HttpResponse(response.text.encode('utf8'))
    """

    #####################################################################################################################

    #payload = "{\n  \"Line\": [\n    {\n      \"Id\": \"0\",\n      \"Description\": \"nov portion of rider insurance\",\n      \"Amount\": 100.0,\n      \"DetailType\": \"JournalEntryLineDetail\",\n      \"JournalEntryLineDetail\": {\n        \"PostingType\": \"Debit\",\n         \"AccountRef\": {\n                \"value\": \"39\",\n                \"name\": \"Opening Bal Equity\"\n              }\n      }\n    },\n    {\n      \"Description\": \"nov portion of rider insurance\",\n      \"Amount\": 100.0,\n      \"DetailType\": \"JournalEntryLineDetail\",\n      \"JournalEntryLineDetail\": {\n        \"PostingType\": \"Credit\",\n              \"AccountRef\": {\n                \"value\": \"44\",\n                \"name\": \"Notes Payable\"\n              }\n\n      }\n    }\n  ]\n}"


    #json.dumps(body))
    #HttpResponse(response.text.encode('utf8'))