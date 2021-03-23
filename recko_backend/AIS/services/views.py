################################################################################
from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseBadRequest, HttpResponseServerError, HttpResponseRedirect
from django.core import serializers
from django.contrib.auth import get_user_model, logout
from django.core.exceptions import ImproperlyConfigured
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response

from .serializers import EmptySerializer,DataSerializer, XeroSerializer, XNestedSerializer1, QuickBooksSerializer,QuickBooksSerializer1, XNestedSerializer3,QNestedSerializer1,QNestedSerializer2,QNestedSerializer3,QNestedSerializer4

from django.core.cache import cache
from django.shortcuts import render, redirect
from django.urls import reverse
from django.http import HttpResponse, HttpResponseBadRequest, HttpResponseServerError, HttpResponseRedirect

from intuitlib.client import AuthClient
from intuitlib.enums import Scopes
from xero import Xero
from xero.auth import OAuth2Credentials
from xero.constants import XeroScopes

import requests
import json
import datetime
import base64
import schedule
import time

from .quickbooks_helper import constructUrl,quickbooksDataEntry
from .xero_helper import constructXeroUrl, XeroRefreshToken, XeroTenants,xeroDataEntry

from .models import Accounts



# Create your views here.
from django.contrib.auth import get_user_model,logout
from django.core.exceptions import ImproperlyConfigured
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny,IsAuthenticated
from rest_framework.response import Response

from . import serializers
from users.utils import get_and_authenticate_user,create_user_account
from users.models import CustomUser
from datetime import date


User = get_user_model()

############################     QUICKBOOKS CREDENTIALS     ############################

client_id1 = "AB1CT9l9mtRkuGnS9w9hASGJtnHTL0JhDggPIPM3gJy2W6gQAy"
client_secret1 = "GG6jhkVesyPyowXBYg9UVlGO1eJF3CUvEhXxfCiS"
redirect_uri1 = "http://localhost:8000/callback"
environment = "sandbox"
scopes = [
    Scopes.ACCOUNTING,
]
auth_client = AuthClient(client_id1, client_secret1, redirect_uri1,
                         environment)
#########################################################################################

############################      XERO CREDENTIALS    ###################################

client_id = '53CA5E526A9C41AB91C216CC29C0A535'
client_secret = 'vh7Kar4K4FvGrbugjfzzEPCUvLD2t2b-p9SmLIR5cng30FgH'
redirect_url = 'http://localhost:8000/xero_callback'

scope = 'offline_access accounting.journals.read'
b64_id_secret = base64.b64encode(
    bytes(client_id + ':' + client_secret, 'utf-8')).decode('utf-8')

#########################################################################################

#################################### QUICKBOOKS API CALL #########################################
def quickbook(request):
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
    fetchUrl = reverse('qbo')
    return redirect(fetchUrl)#HttpResponse("QuickBooks Authentication Done!!")


def fetchQboData(request):
    #map quickbooks data to serializer and store in database/update existing data in database
    #if auth_client.access_token is None:
    if auth_client.refresh_token is None:
        getNewTokenUrl = reverse('quickbook')
        return HttpResponseRedirect(getNewTokenUrl)
    else:
        auth_client.refresh()

    #call construct url function in quickbooks_helper.py
    response = constructUrl(auth_client.access_token, auth_client.realm_id)
    r1=response.json()

    rt_file = open('quickbooks_response.json', 'w')
    rt_file.write(response.text)
    rt_file.close()

                

    serializer=QuickBooksSerializer(data=r1)
    if serializer.is_valid():
        quickbooksDataEntry(r1)
        return HttpResponse(response.text)
    else:
        print(serializer.errors)
        return HttpResponse(serializer.errors)
    
####################################################  XERO API CALL ################################################

def xero(request):
    auth_url = ('''https://login.xero.com/identity/connect/authorize?''' +
                '''response_type=code''' + '''&client_id=''' + client_id +
                '''&redirect_uri=''' + redirect_url + '''&scope=''' + scope +
                '''&state=123''')  ##can be put in xero_helper.py
    return redirect(auth_url)


def xero_callback(request):
    auth_code = request.GET.get('code', None)
    print(auth_code)

    ################################################################################
    exchange_code_url = 'https://identity.xero.com/connect/token'
    response = requests.post(
        exchange_code_url,
        headers={'Authorization': 'Basic ' + b64_id_secret},
        data={
            'grant_type': 'authorization_code',
            'code': auth_code,
            'redirect_uri': redirect_url
        })
    ###################################################################################
    json_response = response.json()
    print(json_response)

    refresh_token = json_response['refresh_token']

    rt_file = open('refresh_token.txt', 'w')
    rt_file.write(refresh_token)
    rt_file.close()

    access_token = json_response['access_token']
    print(refresh_token)

    rt_file = open('access_token.txt', 'w')
    rt_file.write(access_token)
    rt_file.close()
    return HttpResponse("Xero Authentication Done!!!")


def fetchXeroData(request):
    old_refresh_token = open('refresh_token.txt', 'r').read()
    new_tokens = XeroRefreshToken(old_refresh_token)
    xero_tenant_id = XeroTenants(new_tokens[0])

    response = constructXeroUrl(new_tokens[0], xero_tenant_id)
    r = response.json() 

    serializer=XeroSerializer(data=r)
    if serializer.is_valid():
        xeroDataEntry(r)
        return HttpResponse(response.text)
    else:
        return HttpResponse(serializer.errors)


class TransactionViewSet(viewsets.GenericViewSet):
    permission_classes = [
        AllowAny,
    ]
    serializer_class = EmptySerializer
    serializer_classes = {
        'transactions': EmptySerializer,
        'filterByDate': EmptySerializer,
        'filterByType': EmptySerializer,
        'filterByAccName': EmptySerializer,
    }

    queryset=''

    @action(methods=['GET'], detail=False, permission_classes=[
        IsAuthenticated,
    ])
    def transactions(self, request):
        #returns data from our database
        queryset=Accounts.objects.all()
        serializer=DataSerializer(queryset,many=True)
        return Response(serializer.data,status=status.HTTP_200_OK)

    @action(methods=['POST'], detail=False, permission_classes=[
        IsAuthenticated,
    ])
    def filterByDate(self, request):
        
        startDate=request.data['startDate']
        endDate=request.data['endDate']
        if startDate > endDate:
            return Response({"message":"Start date cannot be before end date"},status.HTTP_400_BAD_REQUEST)
        
        if endDate is None or len(endDate) ==0:
            endDate=datetime.now()

        if startDate is None or len(endDate) ==0:
            return Response({"message":"Please specify a start date"},status.HTTP_400_BAD_REQUEST)

        queryset=Accounts.objects.filter(date__range=[startDate,endDate])
        serializer=DataSerializer(queryset,many=True)
        
        if len(serializer.data)==0:
            return Response({"message":"No transaction records found"},status=status.HTTP_404_NOT_FOUND)
        return Response(serializer.data,status.HTTP_200_OK)
        

    @action(methods=['POST'], detail=False, permission_classes=[
        AllowAny,
    ])
    def filterByType(self, request):
        
        accType=request.data['type']
        

        if accType is None or len(accType) ==0:
            return Response({"message":"Invalid transaction type"},status.HTTP_400_BAD_REQUEST)

        queryset=Accounts.objects.filter(accountType=accType)
        serializer=DataSerializer(queryset,many=True)
        
        return Response(serializer.data,status.HTTP_200_OK)
        

    @action(methods=['POST'], detail=False, permission_classes=[
        AllowAny,
    ])
    def filterByAccName(self, request):
        accname=request.data['accountName']

        if accname is None or len(accname) == 0:
            return Response({"message":"Account Name cannot be blank"},status.HTTP_400_BAD_REQUEST)

        queryset=Accounts.objects.filter(accountName=accname)
        serializer=DataSerializer(queryset,many=True)
        
        if len(serializer.data)==0:
            return Response({"message":"No matching account name found"},status=status.HTTP_404_NOT_FOUND)
        return Response(serializer.data,status.HTTP_200_OK)
        

    def get_serializer_class(self):
        if not isinstance(self.serializer_classes, dict):
            raise ImproperlyConfigured(
                "serializer_classes should be a dict mapping.")

        if self.action in self.serializer_classes.keys():
            return self.serializer_classes[self.action]
        return super().get_serializer_class()
