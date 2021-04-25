#Line API for Sending a notification
import time
import requests
import Scaping_Data as Var
def Lineconfig(command):
    url = 'https://notify-api.line.me/api/notify'
    token = '7CbTkpjA3BNxQPJF064lVKdrTU2fIwiA63Xv1T9wKwn'  ## EDIT
    header = {'content-type': 'application/x-www-form-urlencoded', 'Authorization': 'Bearer ' + token}
    return requests.post(url, headers=header, data=command)

def sendtext(message):
    # send plain text to line
    command = {'message': message}
    return Lineconfig(command)

def sendimage(url):
    command = {'message':" ",'imageThumbnail':url,'imageFullsize':url}
    return Lineconfig(command)

