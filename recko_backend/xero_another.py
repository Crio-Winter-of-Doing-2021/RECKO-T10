import os
from functools import wraps
from django.urls import reverse
from django.shortcuts import redirect
from xero_python.api_client import ApiClient, serialize
from xero_python.api_client.configuration import Configuration
from xero_python.api_client.oauth2 import OAuth2Token
from requests_oauthlib import OAuth2Session
from authlib.integrations.django_client import OAuth, token_update
from django.core.cache import cache
from django.http import HttpResponse
from django.dispatch import receiver

oauth = OAuth()
xero = oauth.register(
    name="xero",
    version="2",
    client_id="client_id",
    client_secret="client_secret",
    endpoint_url="https://api.xero.com/",
    authorization_url="https://login.xero.com/identity/connect/authorize",
    access_token_url="https://identity.xero.com/connect/token",
    refresh_token_url="https://identity.xero.com/connect/token",
    scope="offline_access accounting.transactions")

api_client = ApiClient(
    Configuration(
        debug=True,
        oauth2_token=OAuth2Token(
            client_id=app.config["CLIENT_ID"], client_secret=app.config["CLIENT_SECRET"]
        ),
    ),
    pool_threads=1,
)

redirect_uri = request.build_absolute_uri('authorise/')

