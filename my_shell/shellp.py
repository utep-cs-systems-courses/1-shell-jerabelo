import os, sys, re

#Method for checking ps1 variable and returning current shell ps1
def check_prompt():
    try:
        sys.ps1
    except AttributeError:
        sys.ps1 = "$ "
        return sys.ps1

#Method for taking in commands and executing them
def execute_commands():
    commands = input(f'{sys.ps1}').split(" ")
    pid = os.getpid()
    os.write(2, ("Fork with PID: %d\n" % pid).encode())
    child = os.fork()
    if child < 0:
        os.write(2,("error: Failed to fork with PID: %d\n" % pid).encode())
        sys.exit(1)
    elif child == 0:
        if commands == 'cd':
            os.write(2, "cd command executing...\n".encode())
        else:
            for directory in re.split(":", os.enviorn['PATH']):
                prog = "%s/%s" % (directory, commands[0])
                try:
                    os.execve(prog, commands, os.environ)
                except FileNotFoundError:
                    pass # fail quietly
                os.write(1,("%s command not found.\n" % commands[0]).encode())
                sys.exit(1)
            else:
                child_pid_code = os.wait()

def main():
    while True:
        check_prompt()
        execute_commands()

main()

