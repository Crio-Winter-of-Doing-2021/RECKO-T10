import json
import requests
import webbrowser
import base64


#Created One app in my XERO account, which have the following details to connect

client_id = 'E9B0D8958E2F423A820BFC800474C7B4'
client_secret = 'ti9Fr0jegG7DYMn2wIifjacyr5bBrIhZdAAaTKonN2ACgti_'
redirect_url = 'https://developer.xero.com/'
scope = 'offline_access accounting.transactions'
b64_id_secret = base64.b64encode(bytes(client_id + ':' + client_secret, 'utf-8')).decode('utf-8')



# Run this only first time to get authenticate, it will return access token and refresh token

def XeroFirstAuth():
    # 1. Send a user to authorize your app
    auth_url = ('''https://login.xero.com/identity/connect/authorize?''' +
                '''response_type=code''' +
                '''&client_id=''' + client_id +
                '''&redirect_uri=''' + redirect_url +
                '''&scope=''' + scope +
                '''&state=123''')
    webbrowser.open_new(auth_url)
    
    # 2. Users are redirected back to you with a code
    auth_res_url = input('What is the response URL? ')
    start_number = auth_res_url.find('code=') + len('code=')
    end_number = auth_res_url.find('&scope')
    auth_code = auth_res_url[start_number:end_number]
    print(auth_code)
    print('\n')
    
    # 3. Exchange the code
    exchange_code_url = 'https://identity.xero.com/connect/token'
    response = requests.post(exchange_code_url, 
                            headers = {
                                'Authorization': 'Basic ' + b64_id_secret
                            },
                            data = {
                                'grant_type': 'authorization_code',
                                'code': auth_code,
                                'redirect_uri': redirect_url
                            })
    json_response = response.json()
    print(json_response)
    print('\n')
    # 4. Receive your tokens
    refresh_token = json_response['refresh_token']
    access_token = json_response['access_token']
     # 4. Receive your tokens
    return [json_response['access_token'], json_response['refresh_token']]



XeroFirstAuth()




# 5. Check the full set of tenants you've been authorized to access
def XeroTenants(access_token):
    connections_url = 'https://api.xero.com/connections'
    response = requests.get(connections_url,
                           headers = {
                               'Authorization': 'Bearer ' + access_token,
                               'Content-Type': 'application/json'
                           })
    json_response = response.json()
    print(json_response)
    
    for tenants in json_response:
        json_dict = tenants
    return json_dict['tenantId']





# 6.1 Refreshing access tokens, since acess token expires in 12 minutes we will use our refresh token to generate new access token and new refresh token, as refresh token never expires. 

#Before this create a file 'refresh_token.txt'  in location C:/folder to store our refresh token latest value everytime we will create new access token

def XeroRefreshToken(refresh_token):
    token_refresh_url = 'https://identity.xero.com/connect/token'
    response = requests.post(token_refresh_url,
                            headers = {
                                'Authorization' : 'Basic ' + b64_id_secret,
                                'Content-Type': 'application/x-www-form-urlencoded'
                            },
                            data = {
                                'grant_type' : 'refresh_token',
                                'refresh_token' : refresh_token
                            })
    json_response = response.json()
    print(json_response)
    
    new_refresh_token = json_response['refresh_token']
    rt_file = open('C:/folder/refresh_token.txt', 'w')
    rt_file.write(new_refresh_token)
    rt_file.close()
    
    return [json_response['access_token'], json_response['refresh_token']]



# Enter refresh token recived while authentication 
XeroRefreshToken('<REFRESH_TOKEN>')





# 6.2 Call the API
def XeroRequests():
    old_refresh_token = open('C:/folder/refresh_token.txt', 'r').read()
    new_tokens = XeroRefreshToken(old_refresh_token)
    xero_tenant_id = XeroTenants(new_tokens[0])
    get_url = 'https://api.xero.com/api.xro/2.0/Invoices'
    response = requests.get(get_url,
                           headers = {
                               'Authorization': 'Bearer ' + new_tokens[0],
                               'Xero-tenant-id': xero_tenant_id,
                               'Accept': 'application/json'
                           })
    json_response = response.json()
    print(json_response)
    
    xero_output = open('C:/folder/xero_output.txt', 'w')
    xero_output.write(response.text)
    xero_output.close()

