# get admin rights
import ctypes, sys
##

import subprocess
import os, winshell

import requests

import urllib.request
import shutil
import time

from ZeroLogger.ZeroLogger import *
from win32com.client import Dispatch

FileID = str("1s0iNX7UppwYNK3XrPQePu4J2jRURRw1H") #https://drive.google.com/file/d/1s0iNX7UppwYNK3XrPQePu4J2jRURRw1H/view?usp=sharing

def initDownload():
    # get google downloader.
    # https://github.com/oOHiyoriOo/SRMultiplayer/raw/master/HostedFile/gget.exe

    info("checking dirs...")    
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
    warn("Downloading SlimeRancher... (This may take a while...)")
    GDriveGet(FileID,'./temp/SlimeRancher.rar')
    warn("Downloading Multiplayer...")

    url = "https://github.com/oOHiyoriOo/SRMultiplayer/raw/master/HostedFile/Multiplayer.rar"
    file_name = "./temp/Multiplayer.rar"

    with urllib.request.urlopen(url) as response, open(file_name, 'wb') as out_file:
        shutil.copyfileobj(response, out_file)


def UnPack():
    info("Unpacking Files... to C:\\Program Files")

    os.system('%cd%/temp/unrar.exe x %cd%/temp/SlimeRancher.rar "C:\\Program Files"')
    os.system("%cd%/temp/unrar.exe x %cd%/temp/Multiplayer.rar")
    os.system("cls")
    done_task("Extracted files.")
    

def installMultiplayer():
    warn("Installing Multiplayer files!")
    os.system('xcopy "%cd%\\Multiplayer\\*.*" "C:\\Program Files\\Slime.Rancher.v1.4.1c\\" /S /K /D /H /Y')
    done_task("Done.")

    info("Calling Injector. \n===================================")
    injector = subprocess.Popen('"C:\\Program Files\\Slime.Rancher.v1.4.1c\\UnityInjector.exe"', shell=True)
    time.sleep(10) # <-- sleep for 12''
    injector.terminate() # <-- terminate the process
    done_task("===================================\nInjector called")

def createShortcut():
    info("Create Desktop Shortcut!")
    desktop = winshell.desktop()
    path = os.path.join(desktop, "SlimeRancher Multiplayer.lnk")
    target = r"C:\\Program Files\\Slime.Rancher.v1.4.1c\\SlimeRancher.exe"
    wDir = r"C:\\Program Files\\Slime.Rancher.v1.4.1c\\"
    icon = r"C:\\Program Files\\Slime.Rancher.v1.4.1c\\SlimeRancher.exe"
    shell = Dispatch('WScript.Shell')
    shortcut = shell.CreateShortCut(path)
    shortcut.Targetpath = target
    shortcut.WorkingDirectory = wDir
    shortcut.IconLocation = icon
    shortcut.save()

    os.system("cls")
    info("Everything should be done! hf ^^")
    sys.exit(0)

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


def is_admin():
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False



##################################################################################################
##################################################################################################
##################################################################################################


if is_admin():
    initDownload()

    MainDownload()

    UnPack()
    installMultiplayer()
    createShortcut()

else:
    ctypes.windll.shell32.ShellExecuteW(None, "runas",sys.executable, __file__,None, 1)
