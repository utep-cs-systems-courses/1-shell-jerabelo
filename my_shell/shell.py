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

#method for displaying core commands of a shell
def menu(commands):
    if commands[0] == "exit":
        sys.exit(1)
    elif commands[0] == "cd":
        cd_command(commands)
    elif commands.__contains__("|"):
        run_pipe(commands)
    elif commands.__contains__('tar'):
        archive(commands)
#creating child using fork
    child = os.fork()
    #if no child exists, exit
    if child < 0:
        sys.exit(1)
    elif child == 0: #child 1 executing
        #redirection for writing into file
        if commands.__contains__(">"):
            #closing standard fd for writting in
            os.close(1)
            #open 2nd command,create file if it doesn't exist & open for writing
            os.open(commands[2], os.O_CREAT | os.O_WRONLY)
            #making child writing fd inheritable
            os.set_inheritable(1, True)
            commands = commands[:1]
        #redirection for displaying contents out
        elif commands.__contains__("<"):
            #closing standard fd for reading
            os.close(0)
            os.open(commands[2], os.O_RDONLY)
            # making child reading fd inheritable
            os.set_inheritable(0, True)
            commands = commands[:1]
        execute(commands)
    else:
        childPidCode = os.wait()

#method for changing path based on path
def cd_command(path):
    print(path)
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

#method for checking all directories & splitting to check viable path
def execute(commands):
    for dir in re.split(":", os.environ['PATH']):  # try each directory in the path
        program = "%s/%s" % (dir, commands[0])
        try:
            os.execve(program, commands, os.environ)  # try to exec program
        except FileNotFoundError:
            pass
    os.write(2, ("Child: Error: Could not exec %s\n" % commands[0]).encode())
    sys.exit(1)

#pipe method
def run_pipe(commands):
    (r, w) = os.pipe()
    for rw in (r,w):
        os.set_inheritable(r,True)
    p1 = os.fork()
    # only needs to write at the write end
    if p1 < 0:
        os.write(1,'Filed to forked.'.encode())
        sys.exit(1)
    elif p1 == 0: #closing the standard fd for reading (r)
        os.close(1) #close writing fd
        #duplicate writing fd
        os.dup(w)
        os.set_inheritable(1,True)
        for rw in (r,w):
            os.close(rw)
        commands = commands[0:commands.index("|")] #get command up to pipe symbol
        #execute commands
        execute(commands)
        sys.exit(1)
    else:
        #create 2nd fork
        p2 = os.fork()
        if p2 < 0:
            os.write(1,'Failed to fork second child'.encode())
            sys.exit(1)
            #if p2 has has been foked > 0
        elif p2 == 0:
            # close standard reading fd
            os.close(0)
            #duplicate reading fd
            os.dup(r)
            os.set_inheritable(0,True)
            for rw in (r,w):
                os.close(rw)
                # get commmand after pipe symbol
            commands = commands[commands.index("|") + 1:]
            execute(commands)
            sys.exit(1)
        else:
            childPidCode = os.wait()
            for rw in (r,w):
                os.close(rw)
            childPidCode = os.wait()

#working on archiving method
#design when sender send archieve file, find typ eof file, what bytes belong to first file, and second
#encode info about length of file and file name, everything else if extra, you can add
#extract original files from archive
def archive(commands):
    file = commands[1]
    path = os.getcwd()
    full_path = file + "/" + path
    execute(full_path)

if '__main__' == __name__:
    main()