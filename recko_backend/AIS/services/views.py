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
        'xeroAccounts':EmptySerializer,
        'xeroUsers':EmptySerializer
    }

    queryset=''

    @action(methods=['GET'], detail=False, permission_classes=[
        IsAuthenticated,
    ])
    def transactions(self, request):
        #returns data from our database
        queryset=Accounts.objects.values('accountId','accountName','amount','date','accountType','providerName')
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
