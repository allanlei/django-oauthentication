import urllib2, urllib
import simplejson as json

client_id = None
client_secret = None
redirect_uri = 'http://localhost:8000/accounts/login/authenticate/oauth2/'



def get_authorization_url():
    return '{authorization_endpoint}?client_id={client_id}&redirect_uri={redirect_uri}&scope={scopes}&response_type={response_type}&access_type={access_type}&approval_prompt={approval_prompt}&state={state}'.format(
        authorization_endpoint='https://accounts.google.com/o/oauth2/auth',
        client_id=client_id,
        redirect_uri=redirect_uri,
        scopes=' '.join([
            'https://www.googleapis.com/auth/userinfo.profile', 
            'https://www.googleapis.com/auth/userinfo.email',
        ]),
        response_type='code',
        state='nonce=abc123',       #Store a nonce or next=/ param or domain
        access_type='online', #'offline',
        approval_prompt='auto', #'force',     #Set to "force" to ensure a refresh_token in response
    )

def get_access_token(auth_code):
    try:
        request = urllib2.Request(
          url='https://accounts.google.com/o/oauth2/token',
          data=urllib.urlencode({
              'code': auth_code,
              'client_id': client_id,
              'client_secret': client_secret,
              'redirect_uri': redirect_uri,
              'grant_type': 'authorization_code',
            }))
        
        request_open = urllib2.urlopen(request)
        response = request_open.read()
        request_open.close()
        tokens = json.loads(response)
        return tokens.get('access_token', None), tokens.get('refresh_token', None), tokens.get('expires', 0)
    except urllib2.HTTPError, err:
        
        return None, None, None

def refresh_access_token(refresh_token):
    request = urllib2.Request(
        url='https://accounts.google.com/o/oauth2/token',
        data=urllib.urlencode({
            'client_id': client_id,
            'client_secret': client_secret,
            'refresh_token': refresh_token,
            'grant_type': 'refresh_token',
        }),
    )
    request_open = urllib2.urlopen(request)
    response = request_open.read()
    request_open.close()
    tokens = json.loads(response)
    access_token = tokens['access_token']
    return access_token

#Catch Http 401
#    Try to refresh or get a new token
def get_user_profile(access_token):
    request = urllib2.Request(
        url='https://www.googleapis.com/oauth2/v1/userinfo',
        headers={
            'Authorization': 'Bearer {access_token}'.format(access_token=access_token),
        }
    )
    request_open = urllib2.urlopen(request)
    response = request_open.read()
    request_open.close()
    return json.loads(response)
    

#url = get_authorization_url()
#print url
#auth_code = raw_input('Enter authorization code (parameter of URL): ')
#access_token, refresh_token, expires = get_access_token(auth_code)
#print 'Access Token', access_token
#print 'Refreshable:', refresh_token is not None
#if access_token:
#    data = get_user_profile(access_token, auth_code)
#    for key, val in data.items():
#        print key, val


