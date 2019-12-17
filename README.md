# WHAT IS THE PROJECT?

The application consists of searching for zigzag exchanges and adding it to a spreadsheet, making this loop once a day.

# CONFIGURING THE ENVIRONMENT
#
#
##### 1 - One step :  program installation is packages
#
#
```bash
sudo su && apt-get update
apt-get upgrade && apt-get install python3
apt-get install python3-pip && apt-get install git
git clone https://github.com/bitnod-dev/zigzagtosheet
cd zigzagtosheet && pip3 -r requirements.txt
```

##### 2 - First step:  Getting your credentials
#
#
![Screenshot](https://s3.amazonaws.com/com.twilio.prod.twilio-docs/original_images/google-developer-console.gif)

###### .1 Go to the Google APIs Console.
###### .2 Create a new project.
###### .3 Click Enable API. Search for and enable the Google Drive API.
###### .4 Create credentials for a Web Server to access Application Data.
###### .5 Name the service account and grant it a Project Role of Editor.
###### .6 Download the JSON file.
###### .7 Copy the JSON file to your code directory and rename it to keyfile.json
#
#
##### 3 - Two step: Sharing spreadsheet with app
#
![Screenshot](https://s3.amazonaws.com/com.twilio.prod.twilio-docs/original_images/share-google-spreadshet.gif)
#

###### .1 Ceate or import a spreadsheet named "book".
#
###### .2 Find the  client_email inside keyfile.json. Back in your spreadsheet, click the Share button in the top right, and paste the client email into the People field to give it edit rights. Hit Send.
#
###### .2 If you skip this step, you’ll get a gspread.exceptions.SpreadsheetNotFound error when you try to access the spreadsheet from Python.

#

## Starting the application
#
```bash
python3 app.py
```

#
![Screenshot](http://i.imgur.com/IQJhO0n.png)

## Seeing the google spreadsheet
#
![Screenshot](http://i.imgur.com/6zp4DI0.png)

#
## Custom settings
#
![Screenshot](https://i.imgur.com/tydG4a7.png)

* You can change some settings in the code such as the size of the book to be taken, the name of the spreadsheet, the name of the keyfile, the settings are from line 11 to 17.

###### I freelance just call me on twitter DM [@devkakashi](https://twitter.com/devkakashi)
#
[Image Credits](https://www.twilio.com/blog/2017/02/an-easy-way-to-read-and-write-to-a-google-spreadsheet-in-python.html)
