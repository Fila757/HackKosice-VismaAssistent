from __future__ import print_function
import datetime
import pickle
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request

import sys
sys.path.append('google_calendar/list_events')
from list_events import list_events


# If modifying these scopes, delete the file token.pickle.
SCOPES = ['https://www.googleapis.com/auth/calendar']


def mv_event(event, calendarId):
    """
    Moving an event to a google calendar
    """
    creds = None
    # The file token.pickle stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists(os.path.join(calendarId, 'token.pickle')):
        with open(os.path.join(calendarId, 'token.pickle'), 'rb') as token:
            creds = pickle.load(token)
            # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
            # Save the credentials for the next run
        with open(os.path.join(calendarId, 'token.pickle'), 'wb') as token:
            pickle.dump(creds, token)

    service = build('calendar', 'v3', credentials=creds)
    event = service.events().move(calendarId='primary', eventId='f7aa99kjvr2uhu786ucjffu1v8_20200905T160000Z')
    print(event)
    #print ('Event created: %s' % (event.get('htmlLink')))



if __name__ == '__main__':

    events = list_events('primary')
    mv_event(events[0], 'primary')
