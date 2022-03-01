import sys,os,re

#method that checks if ps1 is passed if not,sets default '$'
def token():
    if 'PS1' in os.environ:
        #set os.enviorn
        os.environ['PS1'] == 'PS1'
        return os.environ['PS1']
    else:
        os.environ['PS1'] == "$ "
        #set os.environ and then return
        return os.environ['PS1']

def menu(commands):
    if commands[0] == "exit":
        sys.exit(1)
    elif commands[0] == "cd":
        cd_command(commands)
    elif commands.__contains__("|"):
        commands = pipe_commands(commands)
        (r,w) = os.pipe()
        os.set_inheritable(0,True)
        os.set_inheritable(1,True)
        #closing output
        os.close(0)
        os.dup(r)
        execute(commands)
    child = os.fork()
    if child < 0:
        sys.exit(1)
    elif child == 0:
        if commands.__contains__(">"):
            os.close(1)
            os.open(commands[2], os.O_CREAT | os.O_WRONLY)
            #making child writing fd inheritable
            os.set_inheritable(1, True)
            commands = commands[:1]

        elif commands.__contains__("<"):
            os.close(0)
            os.open(commands[2], os.O_RDONLY)
            # making child reading fd inheritable
            os.set_inheritable(0, True)
            commands = commands[:1]
        execute(commands)
    else:
        childPidCode = os.wait()

def cd_command(path):
    if len(path) > 1:
        try:
            os.chdir(path[1])
        except Exception:
            print("cd: no such file or directory: {}".format(path[1]))
    else:
        os.chdir(os.path.expanduser("~"))

def main():
    while True:
        path = f"{os.getcwd()} $"
        os.write(1, path.encode())
        commands = os.read(0, 1000).decode().split()
        menu(commands)
        continue

def execute(commands):
    for dir in re.split(":", os.environ['PATH']):  # try each directory in the path
        program = "%s/%s" % (dir, commands[0])
        try:
            os.execve(program, commands, os.environ)  # try to exec program
        except FileNotFoundError:
            pass
    os.write(2, ("Child: Error: Could not exec %s\n" % commands[0]).encode())
    sys.exit(1)

def pipe_commands(commands):
    for line in commands:
        cmds = line.split('|')
        return cmds


if '__main__' == __name__:
    main()