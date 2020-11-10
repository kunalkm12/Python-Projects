from __future__ import print_function
from apiclient import discovery
from oauth2client import client
from oauth2client import tools
from oauth2client.file import Storage
import logging
import telegram
from telegram.error import NetworkError, Unauthorized
from time import sleep
import httplib2
import os
from tkinter import *

update_id = None
SCOPES = 'https://www.googleapis.com/auth/spreadsheets.readonly'
CLIENT_SECRET_FILE = 'client_secret.json'
APPLICATION_NAME = 'Google Sheets API Python Quickstart'

global spreadsheetId
global service

try:
    import argparse
    flags = argparse.ArgumentParser(parents=[tools.argparser]).parse_args()
except ImportError:
    flags = None


def get_credentials():
    home_dir = os.path.expanduser('~')
    credential_dir = os.path.join(home_dir, '.credentials')
    if not os.path.exists(credential_dir):
        os.makedirs(credential_dir)
    credential_path = os.path.join(
        credential_dir, 'sheets.googleapis.com-python-quickstart.json')

    store = Storage(credential_path)
    credentials = store.get()
    if not credentials or credentials.invalid:
        flow = client.flow_from_clientsecrets(CLIENT_SECRET_FILE, SCOPES)
        flow.user_agent = APPLICATION_NAME
        if flags:
            credentials = tools.run_flow(flow, store, flags)
        else:
            credentials = tools.run(flow, store)
        print('Storing credentials to ' + credential_path)
    return credentials


def start(bot, update):
    """Send a message when the command /start is issued."""
    update.message.reply_text('Hi!')
    update.message.reply_text('Enter data followed by spaces')
    update.message.reply_text('For example 2010 CS Vineet Subject')


def help(bot, update):
    """Send a message when the command /help is issued."""
    update.message.reply_text('Please contact system administrators for help!')


def chooseStream(message):
    print("message: ", message)
    if message == "CS" or message == "cs":
        spreadsheetId = '1AIWf2upwG2-ot8Bda9_yzgpzsKaU8P4Fa1HprHL8oh4'
        print("spreadsheetID for CS: ", spreadsheetId)
        return 1, spreadsheetId
    else:
        spreadsheetId = '1AIWf2upwG2-ot8Bda9_yzgpzsKaU8P4Fa1HprHL8oh4'
        print("spreadsheetID for NOT CS", spreadsheetId)
        return 1, spreadsheetId


def chooseSheet(message, spreadsheetId):
    if message == 'Sub1':
        rangeName = 'Sheet1!A2:E'  # chooses which sheet and which columns 
        print("rangeName for sub1: ", rangeName)
        return 1, rangeName
    elif message == 'Sub2':
        rangeName = 'Sheet2!A2:E'
        print("rangeName2 for sub2: ", rangeName)
        return 1, rangeName
    else:
        return 0, 0


def authentication(rangeName, spreadsheetId, s2):
    if s2 == 1:
        credentials = get_credentials()
        http = credentials.authorize(httplib2.Http())
        discoveryUrl = (
            'https://sheets.googleapis.com/$discovery/rest?''version=v4')
        service = discovery.build(
            'sheets', 'v4', http=http, discoveryServiceUrl=discoveryUrl,
            cache_discovery=False)
        result = service.spreadsheets().values().get(
            spreadsheetId=spreadsheetId, range=rangeName).execute()
        values = result.get('values', [])
        return 1, values
    else:
        return 0, 0


def checkinsheet(bot, update, values, incomingmessage):
    flag = 1
    print("Func Called")
    for row in values:
        if incomingmessage == row[0]:
            update.message.reply_text(
                'Name: ' + row[0] + ' Gender: ' +
                row[1] + ' Class Level: ' + row[2])
            flag = 0
            break
        else:
            flag = 1
    if flag == 1:
        flag = 0
        update.message.reply_text("Name not found")
    print("Func Ended")

# Function to check the value for PythonGUI


def checkinsheetGUI(values, name):
    flag = 1
    global replyLabel
    print("Func Called")
    for row in values:
        if name == row[0]:
            replyLabel = (
                'Name: ' + row[0] + '\n Gender: ' +
                row[1] + '\n Class Level: ' + row[2])
            flag = 0
            break
        else:
            flag = 1
    if flag == 1:
        flag = 0
        replyLabel = ("Name not found")
    print("Func Ended")


def botmain():
    """Run the bot."""
    global update_id

    # print(values)
    # Telegram Bot Authorization Token
    bot = telegram.Bot('590901876:AAGjIUbFY73LFfjlTCqlv73KCCJNcxGe5_g')

    # get the first pending update_id, this is so we can skip over it in case
    # we get an "Unauthorized" exception.
    try:
        update_id = bot.get_updates()[0].update_id
    except IndexError:
        update_id = None

    logging.basicConfig(
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    while True:
        try:
            echo(bot)
        except NetworkError:
            sleep(1)
        except Unauthorized:
            # The user has removed or blocked the bot.
            update_id += 1


def echo(bot):
    global update_id
    success1 = 0
    success2 = 0
    success3 = 0
    # Request updates after the last update_id
    for update in bot.get_updates(offset=update_id, timeout=100):
        print(update.message.text)
        update_id = update.update_id + 1
        # update.message.reply_text(values[0])
        incomingmessage = str(update.message.text)
        if incomingmessage == "/start":
            start(bot, update)
        elif incomingmessage == "help":
            help(bot, update)
        else:
            try:
                year, stream, name, subject = incomingmessage.split(" ")
            except ValueError:
                update.message.reply_text('Sorry, input not in proper format.')
                update.message.reply_text('Please try again.')
            else:
                print("Year: ", year)
                print("Stream: ", stream)
                print("Name: ", name)
                print("Subject: ", subject)
                success1, id = chooseStream(stream)
                if success1 == 0:
                    update.message.reply_text('Stream not found..')
                else:
                    print("Success1", success1)
                    success2, rangeName = chooseSheet(subject, id)
                    if success2 == 0:
                        update.message.reply_text('Subject not found..')
                    else:
                        success3, values = authentication(
                            rangeName, id, success2)
                        if success3 == 1:
                            checkinsheet(bot, update, values, name)
                        else:
                            update.message.reply_text(
                                'Some Other Issue. Try Again.')


def wingui():
    interface = Tk()
    interface.title('Attendance Management')

    def check():
        if sap.get() == '' or namefield.get() == '' or subvar.get() == '' or yearvar.get() == '' or streamvar.get() == '':
            print('Enter the details correctly.')
        else:
            year = yearvar.get()
            stream = streamvar.get()
            name = namefield.get()
            subject = subvar.get()
            print("Year: ", year)
            print("Stream: ", stream)
            print("Name: ", name)
            print("Subject: ", subject)
            success1, id = chooseStream(stream)
            print("Success1", success1)
            success2, rangeName = chooseSheet(subject, id)
            success3, values = authentication(rangeName, id, success2)
            if success1 == 1 and success2 == 1 and success3 == 1:
                checkinsheetGUI(values, name)
                l6.config(text=replyLabel)

    l1 = Label(interface, text='Enter the SAP ID of the student : ')
    sap = Entry(interface)

    l2 = Label(interface, text='Select the year of study : ')
    yearvar = StringVar(interface)
    yearvar.set('-Select-')
    year = OptionMenu(interface, yearvar, '2010', '2010', '2010')

    l3 = Label(interface, text='Select the stream : ')
    streamvar = StringVar(interface)
    streamvar.set('-Select-')
    stream = OptionMenu(interface, streamvar, 'CS', 'cs')

    l4 = Label(interface, text='Enter Name of the student : ')
    namefield = Entry(interface)

    l5 = Label(interface, text='Enter the subject : ')
    subvar = StringVar(interface)
    subvar.set('-Select-')
    sub = OptionMenu(interface, subvar, 'Sub1', 'Sub2')

    l6 = Label(interface, text='')

    submit = Button(interface, text='Submit', command=check)

    l1.grid(row=0, column=0)
    sap.grid(row=0, column=1)

    l2.grid(row=1, column=0)
    year.grid(row=1, column=1)

    l3.grid(row=2, column=0)
    stream.grid(row=2, column=1)

    l4.grid(row=3, column=0)
    namefield.grid(row=3, column=1)

    l5.grid(row=4, column=0)
    sub.grid(row=4, column=1)

    submit.grid(row=5, columnspan=2)
    l6.grid(row=6, columnspan=2)

    interface.mainloop()


def main():
    interface = Tk()
    interface.title('Welcome to Attendance Managment System')
    L1 = Label(interface, text='Please select the interface : ')
    winBtn = Button(interface, text='PythonGUI', command=wingui)
    botBtn = Button(interface, text='BotGUI', command=botmain)
    L1.pack()
    winBtn.pack(pady=5)
    botBtn.pack(pady=5)
    interface.mainloop()


if __name__ == '__main__':
    main()
