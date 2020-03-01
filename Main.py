import sys
import os
import requests

import urllib.request
import shutil
import time

from ZeroLogger.ZeroLogger import *

# FileID = str("1s0iNX7UppwYNK3XrPQePu4J2jRURRw1H") #https://drive.google.com/file/d/1s0iNX7UppwYNK3XrPQePu4J2jRURRw1H/view?usp=sharing
FileID = str("1qp0IYzh2Xlpp0eOTJTsulcsd0hnoQvLd") # testfile

def initDownload():
    # get google downloader.
    # https://github.com/oOHiyoriOo/SRMultiplayer/raw/master/HostedFile/gget.exe

    info("cheking dirs...")    
    if not os.path.isdir('temp'):
        os.system('mkdir %cd%\\temp')
    
    done_task("all dirs should be there...")


    # Download the file from `url` and save it locally under `file_name`:
    url = "https://github.com/oOHiyoriOo/SRMultiplayer/raw/master/HostedFile/UnRAR.exe"
    file_name = "./temp/unrar.exe"

    with urllib.request.urlopen(url) as response, open(file_name, 'wb') as out_file:
        shutil.copyfileobj(response, out_file)



    done_task("Init Done!!")
    
    time.sleep(1)
    os.system("cls")


def clearUp():
    warn("Cleaning tools dir!")
    os.system("RMDIR /Q/S %cd%\\tools")
    done_task("Deleted tools.")

def MainDownload():
    warn("Downloading SlimeRancher...")
    GDriveGet(FileID,'./temp/SlimeRancher.rar')
    warn("Downloading Multiplay...")

    url = "https://github.com/oOHiyoriOo/SRMultiplayer/raw/master/HostedFile/Multiplayer.zip"
    file_name = "./temp/Multiplayer.zip"

    with urllib.request.urlopen(url) as response, open(file_name, 'wb') as out_file:
        shutil.copyfileobj(response, out_file)


def UnPack():
    os.system("%cd%/temp/unrar.exe x %cd%/temp/SlimeRancher.rar")


##################################################################################################
##################################################################################################
##################################################################################################

#taken from this StackOverflow answer: https://stackoverflow.com/a/39225039
 
def GDriveGet(id, destination):
    URL = "https://docs.google.com/uc?export=download"

    session = requests.Session()

    response = session.get(URL, params = { 'id' : id }, stream = True)
    token = get_confirm_token(response)

    if token:
        params = { 'id' : id, 'confirm' : token }
        response = session.get(URL, params = params, stream = True)

    save_response_content(response, destination)    

def get_confirm_token(response):
    for key, value in response.cookies.items():
        if key.startswith('download_warning'):
            return value

    return None

def save_response_content(response, destination):
    CHUNK_SIZE = 32768

    with open(destination, "wb") as f:
        for chunk in response.iter_content(CHUNK_SIZE):
            if chunk: # filter out keep-alive new chunks
                f.write(chunk)


##################################################################################################
##################################################################################################
##################################################################################################

initDownload()

MainDownload()

UnPack()