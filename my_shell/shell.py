import os,re,sys

path = os.getcwd()
dir_list = os.listdir(path)

def CurrPath():
    os.write(path)

def ChangePath(args):
    try:
        os.chdir(args)
    except FileNotFoundError:
        os.write(f'file{args[1]} not found!\n'.encode())

def main(*args):
    while(True):
        os.fork()
        if len(args) == 0:
            os.write('$ ')
            prompt = input()
            if prompt == 'ls':
                CurrPath()
            elif prompt == 'dir':
                os.write('File & directories: ')
                os.write(dir_list)
                continue




