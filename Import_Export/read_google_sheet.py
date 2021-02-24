import os.path
import pickle
import pandas as pd
from django.http import HttpResponse
from google.auth.transport.requests import Request
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

from product.models import Product, Category, Brand, Color

client_id = "408628163025-8hqm66v244fiea05bnli2v21m0bna8ve.apps.googleusercontent.com"
client_secret = "cWwUMFr1jTnGNIBNdMW0noZ8"

# If modifying these scopes, delete the file token.pickle.
SCOPES = ['https://www.googleapis.com/auth/spreadsheets.readonly']

# The ID and range of a sample spreadsheet.
SAMPLE_SPREADSHEET_ID = '1qbZy1JqtlvpVrYSaKU9-esipXox5RufzoOB1hR8UMOU'
SAMPLE_RANGE_NAME = 'A:Z'


def handle_url():
    """Shows basic usage of the Sheets API.
    Prints values from a sample spreadsheet.
    """
    creds = None
    # The file token.pickle stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
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
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)

    service = build('sheets', 'v4', credentials=creds)

    # Call the Sheets API
    sheet = service.spreadsheets()
    result = sheet.values().get(spreadsheetId=SAMPLE_SPREADSHEET_ID,
                                range=SAMPLE_RANGE_NAME).execute()

    values = result.get('values', [])

    if not values:
        msg = 'No data found from the Google sheet.'
        return msg

    else:
        df = pd.DataFrame(values)
        # selecting 0th row as columns
        df.columns = df.iloc[0]
        # selecting from the 1st row
        df = df.iloc[1:]
        # this will store the data of google sheet to the db
        for row in df.to_dict('records'):

            try:
                _, created = Product.objects.get_or_create(
                    product_name=row.get('product_name'),
                    description=row.get('description'),
                    category=Category.objects.filter(category__iexact=row.get('category')).first(),
                    brand=Brand.objects.filter(brand__iexact=row.get('brand')).first(),
                    color=Color.objects.filter(color__iexact=row.get('color')).first(),
                    price=row.get('price'),
                    size=row.get('size'),
                    type=row.get('type')
                )
            except Exception as e:
                print(e)
                break
            # Print columns A and E, which correspond to indices 0 and 4.
            # print('%s, %s' % (row[0], row[4]))
