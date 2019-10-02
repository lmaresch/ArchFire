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

archfire_path = os.path.dirname(os.path.realpath(__file__))
archfire_build = os.path.join(archfire_path, 'build')
archfire_build_bootstrap = os.path.join(archfire_build, 'root')
archfire_logs = os.path.join(archfire_path, 'logs')

def printError(text):
    for line in text.splitlines():
        print(str('\t') + bcolors.FAIL + str(line) + bcolors.ENDC)

def printWarning(text):
    for line in text.splitlines():
        print(str('\t') + bcolors.WARNING + str(line) + bcolors.ENDC)

def printOK(text):
    for line in text.splitlines():
        print(str('\t') + bcolors.OKGREEN + str(line) + bcolors.ENDC)

def printStdout(text):
    for line in text.splitlines():
        print(str('\t') + str(line))

def printStatusText(text):
    print(text.ljust(leftSize), end = ' ', flush = True)

def printStatusOK():
    text = '[ ' + bcolors.OKGREEN + 'OK' + bcolors.ENDC + ' ]'
    print(text.rjust(rightSize))

def printStatusWarn():
    text = '[' + bcolors.WARNING + 'WARN' + bcolors.ENDC + ']'
    print(text.rjust(rightSize))

def printStatusFail():
    text = '[' + bcolors.FAIL + 'FAIL' + bcolors.ENDC + ']'
    print(text.rjust(rightSize))

def createDirectory(dirname):
    printStatusText('Creating folder \'' + dirname + '\'...')
    if os.path.exists(dirname):
        printStatusOK()
        printOK('Folder already exists.')
    else:
        try:
            os.makedirs(dirname)
            printStatusOK()
            printOK('Folder successfully created.')
        except OSError as e:
            printStatusFail()
            printError(e.strerror)
            exit(1)

def executeProcess(command, text = '', stdout = False, stderr = False, warnOnError = False, log = False, logName = ''):
    if len(text) == 0:
        text = 'Executing command \'' + ' '.join(command) + '\'...'
    printStatusText(text)
    proc = subprocess.Popen(command, stdout = subprocess.PIPE, stderr = subprocess.PIPE, universal_newlines=True)
    textOut, textErr = proc.communicate()
    if log:
        if len(logName) == 0:
            logName = os.path.basename(command[0])
        f = open(os.path.join(archfire_logs, logName + '.log'), 'w')
        if len(textOut) > 0:
            f.write(textOut)
        if len(textErr) > 0:
            f.write(textErr)
        f.close()
    if proc.returncode == 0:
        printStatusOK()
        if stdout:
            printStdout(textOut)
        return True
    else:
        if warnOnError:
            printStatusWarn()
        else:
            printStatusFail()
        printError(textErr)
        return False

printStatusText('Checking if script is started by user \'root\'...')
if os.geteuid() != 0:
    printStatusFail()
    printError('Script can be executed as user \'root\' only!')
    exit(1)
printStatusOK()

createDirectory(archfire_build)
createDirectory(archfire_logs)
if not executeProcess(['/usr/bin/pacman', '-Qi', 'devtools'], text = 'Checking if package \'devtools\' is already installed...', warnOnError = True, log = True, logName = 'pacman_Qi'):
    printWarning('Package \'devtools\' is not installed.')
    if not executeProcess(['/usr/bin/pacman', '-S', '--noconfirm', 'devtools'], log = True, logName = 'pacman_S_devtools'):
        exit(1)

if not os.path.exists(archfire_build_bootstrap):
    if not executeProcess(['/usr/bin/mkarchroot', archfire_build_bootstrap, 'base-devel'], text = 'Installing toolchain...', log = True):
        exit(1)

if not executeProcess(['/usr/bin/arch-nspawn', archfire_build_bootstrap, '/usr/bin/pacman', '-Syu'], text = 'Updating toolchain', log = True):
    exit(1)

