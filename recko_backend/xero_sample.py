from xero.auth import OAuth2Credentials
from xero.constants import XeroScopes

from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseBadRequest, HttpResponseServerError
import datetime
from intuitlib.client import AuthClient
from intuitlib.enums import Scopes
import requests 
import json
# Create your views here.


from xero.auth import OAuth2Credentials
from xero.constants import XeroScopes

my_scope = [XeroScopes.ACCOUNTING_TRANSACTIONS,XeroScopes.PAYROLL_EMPLOYEES]

client_id='53CA5E526A9C41AB91C216CC29C0A535'
client_secret='zgYxUtvRbW9t8_K2KO_RawCmyHh270il2QgI3n2ZtXV-W81r'
callback_uri='https://developer.xero.com/'

mycache={}

credentials = OAuth2Credentials(client_id, client_secret,scope=my_scope, callback_uri=callback_uri)

authorisation_url = credentials.generate_url()
print("Auth url"," ",authorisation_url)

mycache['xero_creds'] = credentials.state
credentials = OAuth2Credentials(**mycache['xero_creds'])
credentials.verify(request_uri)

cred_state = credentials.state
new_creds = OAuth2Credentials(**cred_state)

token = credentials.token
print("Token"," ",token)


new_creds = OAuth2Credentials(client_id, client_secret, token=token)

credentials.set_default_tenant()
xero = Xero(credentials)
xero.contacts.all()




####################################################################################################

my_scope = [XeroScopes.OFFLINE_ACCESS,XeroScopes.ACCOUNTING_JOURNALS_READ]


client_id1='53CA5E526A9C41AB91C216CC29C0A535'
client_secret1='vh7Kar4K4FvGrbugjfzzEPCUvLD2t2b-p9SmLIR5cng30FgH'
callback_uri1='http://localhost:8000/xero_callback'




def xero(request):
  credentials = OAuth2Credentials(client_id1, client_secret1,scope=my_scope, callback_uri=callback_uri1)
  authorization_url = credentials.generate_url()
  cache.set('xero_creds', credentials.state)
  return redirect(authorization_url)

def xero_callback(request):
  cred = cache.get('xero_creds')
  credentials = OAuth2Credentials(**cred)
  print(credentials.state)
  auth_secret = request.get_raw_uri()
  print("callback url"," ",auth_secret)
  credentials.verify(auth_secret)
  credentials.set_default_tenant()
  cache.set('xero_creds', credentials.state)
  return HttpResponse("BBB")

  #credentials.verify(request_uri)

  """
  cred_state = credentials.state
  new_creds = OAuth2Credentials(**cred_state)

  token = credentials.token
  print("Token"," ",token)


  new_creds = OAuth2Credentials(client_id, client_secret, token=token)

  credentials.set_default_tenant()
  xero = Xero(credentials)
  xero.contacts.all()
  """

############################### XERO API SERIALIZATION  #################################################
def xeroDataEntry(response):
    Accounts.objects.all().delete()
    for obj in response['Journals']:
        list1 = []
        print("Date: ",obj['JournalDate'])
        for journalLine in obj['JournalLines']:
            if hasattr(journalLine, 'Description'):
                s1 = XNestedSerializer2(data=journalLine)
                if s1.is_valid():
                    #print("2\n",s1.data,'\n')
                    list1.append(s1.data)
                else:
                    print(s1.errors)
            else:
                s1 = XNestedSerializer3(data=journalLine)
                if s1.is_valid():
                    print("Account Id: ",s1.data.get('AccountCode'),"\n")
                    print("Account Name: ",s1.data.get('AccountName'),"\n")
                    print("Amount: ",s1.data.get('GrossAmount'),"\n")
                    net=s1.data.get('NetAmount')
                    if net < 0:
                        print("Type: Credit")
                    else:
                        print("Type: Debit")
                    list1.append(s1.data)
                    #print("3 ",s1.data,'\n')
                else:
                    print(s1.errors)

        
        s2 = XNestedSerializer1(
            data={
                "JournalID": obj['JournalID'],
                "JournalDate": obj['JournalDate'],
                "JournalNumber": obj['JournalNumber'],
                "CreatedDateUTC": obj['CreatedDateUTC'],    
                "JournalLines": obj['JournalLines']
            })
        if s2.is_valid():
            print(s2.data, '\n')