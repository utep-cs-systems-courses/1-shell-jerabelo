import os, sys, re

#method that prints a prompt string specified by shell variable PS1.
def print_string(input):
    if (len(input)):
        return '$'
    else:
        args = []
        for item in input.split():
            args.append(item)
            return args


#method for changing directory
def change_directory(location):
    try:
        os.chdir(location)
    except FileNotFoundError:
        os.write(1,(f'file{args[1]} not found!\n').encode())


def get_current_directory:
    getcwd():
