#!/usr/bin/python3

from oauth2client.service_account import ServiceAccountCredentials
import gspread
import requests
import json
import time
import datetime
import glob

# ************************************

keyfile   = 'keyfile.json' # .import your google api configuration file
sheetname = 'book'        # .name of the spreadsheet you created in your google drive account
limitbook = 15           # .Choose book size

if not 'database.json' in glob.glob('*'):

    make = {
      "database" : {"expiry" : None, "booklength" : 1}
    }

    file = open('database.json','w')
    file.write(str(make))
    file.close()

    print(
      ''
    )

# *********************************** 

reqjson = lambda URL, JSON : json.loads(requests.post(
    URL, json=JSON
).text)

def Latestexchanges(limit=15):

    API = 'https://apizigzag.wpmix.net/graphql'

    JSON = {
        "operationName":"latestExchangesQuery",
        "variables":{"limit": limit},
        "query":"query latestExchangesQuery($limit: Int) {\n  exchangeList(limit: $limit) {\n    data {\n      createdAt\n      fromAsset\n      fromType\n      fromAmount\n      toAsset\n      toType\n      toAmount\n      __typename\n    }\n    error {\n      code\n      message\n      __typename\n    }\n    __typename\n  }\n}\n"
    }

    try:
        return reqjson(API, JSON)['data']['exchangeList']
    except:
        return False

def GoogleSheet(sheet, value, index):
    try:
      sheet.insert_row(value, index)
    except:
      return False

def AddSheet(sheet, book, locktitle=None):

    start = 0

    if locktitle == True:

        title = []

        for key in book[0]['data'].keys():

            if '__typename' != key:

                text = key.lower().title()
                text = text.replace('__Typename','Typename')
                title.append(text)
    
        lock = True

        while lock == True:
            try:
                GoogleSheet(sheet, title, 1)
                lock = False
            except:
                GoogleSheet(sheet, title, 1)

        del(key) ; del(lock)

    value = []
    index = 1

    for count in range(0, len(book)):

        for key in book[0]['data'].keys():

            text = str(book[count]['data'][key]).lower()

            if 'exchangelistitemdata' != text:

                value.append(text)

        index += 1
        lock = True

        while lock == True:
          try:
            GoogleSheet(sheet, value, index)
            lock = False
          except:
            GoogleSheet(sheet, value, index)

        value = []

    return True

def DelSheet(Sheet, lenrow):

    lock  = True

    for x in range(1, lenrow):

        while lock == True:
            try:
                Sheet.delete_row(x)
                lock = False
            except:
                Sheet.delete_row(x)
        lock = True
              

# def DeleteSheet():
    
Scope = [
  'https://spreadsheets.google.com/feeds',
  'https://www.googleapis.com/auth/spreadsheets',
  'https://www.googleapis.com/auth/drive.file',
  'https://www.googleapis.com/auth/drive'
]

print('* Software started.\n* Importing keyfile: ' + str(keyfile))

Creds = ServiceAccountCredentials.from_json_keyfile_name(keyfile, Scope)

print('* Starting GoogleSpreadsheet')
print('* Authorizing Access')

Client = gspread.authorize(Creds)

print('* Opening spreadsheet')

while True:
    
    try:
      Sheet  = Client.open(sheetname).sheet1
    except:
      print("[!] This spreadsheet doesn't exist or doesn't list any data")

    data = eval(
      open('database.json','r').read()
    )

    if data['database']['expiry'] == None or datetime.datetime.today().day >= data['database']['expiry']:

        lock = True

        while lock == True:

            print("* Taking zigzag.io's ord book")
            Book = Latestexchanges(limit=limitbook)

            if Book != False:
                    
                print('* Deleting entire spreadsheet')
                DelSheet(Sheet, limitbook + 1, locktitle=True)

                print('* Entering new data into spreadsheet')
                AddSheet(Sheet, Book)

                print('* Spreadsheet was successfully exported to google spreadsheet')

                make = {"database" : {"expiry" : datetime.datetime.today().day + 1, "booklength" : data["database"]["booklength"] + 15}}

                file = open('database.json','w')
                file.write(str(make))
                file.close()

                lock = False

            else:
                print('\n[!] Zigzag.io api request failed retrying')
