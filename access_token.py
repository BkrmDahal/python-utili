"""Makes access token for google API"""
import os

import oauth2client
from oauth2client import client, tools

SCOPES = 'https://www.googleapis.com/auth/gmail.send' 
CLIENT_SECRET_FILE = "M:\\everjobs\\key\\mail\\client_secret_2.json" 
APPLICATION_NAME = 'gmail'

def make_access_token(credential_path, 
                      token_name,
                      client_secret_file,
                      application_name,
                      scopes):
    """Make access token, this step is only required firsttime
    Params:
    -----------
    credential_path: str, path to save token
    token_name: str, name for token
    client_secret_file: str, path to client json from developer console
    application_name: str, project name in google developer console
    scopes:str, scope of your access token

    Output
    -----------
    save access token to credential_path
    """
    try:
        if not os.path.exists(credential_path):
            os.makedirs(credential_path)
    except:
        raise ValueError("Credential_path most be valid path")

    credential_path = credential_path + token_name + '.json'
    flow = client.flow_from_clientsecrets(client_secret_file, scopes)
    flow.user_agent = application_name
    store = oauth2client.file.Storage(credential_path)
    credentials = tools.run_flow(flow, store)
    print('Storing credentials to ' + credential_path)

def _main():
    make_access_token('M:/', "test", CLIENT_SECRET_FILE, APPLICATION_NAME, SCOPES)

if __name__ == "__main__":
    _main()
