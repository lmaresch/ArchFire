#!/usr/bin/python

import os
import subprocess

class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

terminalSize = os.get_terminal_size(0)
rightSize = 20
leftSize = terminalSize.columns - rightSize

def printError(text):
    print(str('\t') + bcolors.FAIL + str(text) + bcolors.ENDC)

def printWarning(text):
    print(str('\t') + bcolors.WARNING + str(text) + bcolors.ENDC)

def printOK(text):
    print(str('\t') + bcolors.OKGREEN + str(text) + bcolors.ENDC)

def printStatusText(text):
    print(text.ljust(leftSize), end=' ')

def printStatusOK():
    text = '[ ' + bcolors.OKGREEN + 'OK' + bcolors.ENDC + ' ]'
    print(text.rjust(rightSize))

def printStatusWarn():
    text = '[' + bcolors.WARNING + 'WARN' + bcolors.ENDC + ']'
    print(text.rjust(rightSize))

def printStatusFail():
    text = '[' + bcolors.FAIL + 'FAIL' + bcolors.ENDC + ']'
    print(text.rjust(rightSize))

printStatusText('Checking if script is started by user \'root\'...')
if os.geteuid() != 0:
    printStatusFail()
    printError('Script can be executed as user \'root\' only!')
    exit(1)
printStatusOK()

printStatusText('Checking if package \'devtools\' is already installed...')
pacmanProc = subprocess.Popen(['pacman', '-Qi', 'devtools'], stdout = subprocess.PIPE, stderr = subprocess.PIPE)
pacmanProc.wait()
if pacmanProc.returncode == 0:
    printStatusOK()
else:
    printStatusWarn()
    printStatusText('Try to install \'devtools\' package with command \'pacman -S devtools\'...')
    pacmanProc = subprocess.Popen(['pacman', '-S', '--noconfirm', 'devtools'], stdout = subprocess.PIPE, stderr = subprocess.PIPE, universal_newlines=True)
    _, errorText = pacmanProc.communicate()
    if pacmanProc.returncode == 0:
        printStatusOK()
    else:
        printStatusFail()
        printError(errorText)
        exit(1)

archfire_path = os.path.dirname(os.path.realpath(__file__))
archfire_build = os.path.join(archfire_path, 'build')
printStatusText('Creating folder \'build\'...')
if os.path.exists(archfire_build):
    printStatusOK()
    printOK('Folder already exists.')
else:
    try:
        os.makedirs(archfire_build)
        printStatusOK()
        printOK('Folder successfully created.')
    except OSError as e:
        printStatusFail()
        printError(e.strerror)
        exit(1)