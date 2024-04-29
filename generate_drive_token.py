import pickle
import os
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request

def load_credentials():
    """Loads the Google Drive credentials from the file.

    Returns:
        google.oauth2.credentials.Credentials: The Google Drive credentials or None if not found.
    """
    credentials = None
    token_file = "token.pickle"

    if os.path.exists(token_file):
        with open(token_file, 'rb') as f:
            credentials = pickle.load(f)

    return credentials

def refresh_and_save_credentials():
    """Refreshes the Google Drive credentials if necessary and saves them to the file.
    """
    credentials = None
    oauth_scope = ["https://www.googleapis.com/auth/drive"]

    if load_credentials() is None:
        flow = InstalledAppFlow.from_client_secrets_file(
            'credentials.json', oauth_scope)
        try:
            credentials = flow.run_local_server(port=0, open_browser=False)
        except Exception as e:
            print(f"Error running local server: {e}")

    if (
        credentials is not None
        and not credentials.valid
        and credentials.expired
        and credentials.refresh_token
    ):
        try:
            credentials.refresh(Request())
        except Exception as e:
            print(f"Error refreshing credentials: {e}")

    if credentials is not None:
        try:
            with open("token.pickle", 'wb') as token:
                pickle.dump(credentials, token)
        except Exception as e:
            print(f"Error saving credentials: {e}")

if __name__ == "__main__":
    refresh_and_save_credentials()
