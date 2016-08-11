#!/usr/bin/python
# coding: utf-8
# import argparse
import os
import re
import readline
import signal
import sys
from subprocess import call
import subprocess


# parser = argparse.ArgumentParser()
# parser.add_argument("-clusters", help="display list of clusters")
# print(parser.parse_args())

class Doud:

    def __init__(self):
        self.servers_file = "./servers_file.conf"
        self.help_str = {
            "addChildServer <server_ip>": "you can add a child server ip, but first they have to add the ssh key of this server on the other!",
            "run <command>": "run command in all childs server"}
        commands = ["run", "addChildServer", "installDocker"]

        def completer(text, state):
            options = [i for i in commands if i.startswith(text)]
            if state < len(options):
                return options[state]
            else:
                return None

        readline.parse_and_bind("tab: complete")
        readline.set_completer(completer)

        def signal_handler(signal, frame):
            print(" bye!\n\nᕙ༼ ,,ԾܫԾ,, ༽ᕗ\n")
            sys.exit(0)
        signal.signal(signal.SIGINT, signal_handler)

    def addChildServer(self, server_ip):
        pattern = re.compile("[0-9.]{7,15}")
        if(pattern.match(server_ip)):
            file = open(self.servers_file, "a")
            file.write(server_ip + "\n")
            file.close()
            print("Server: " + server_ip + " added success!")
        else:
            print("Invalid IP: " + server_ip)

    def installDocker(self):
        if(os.path.isfile(self.servers_file)):
            file = open(self.servers_file, "r")
            for line in file:
                ip = line.rstrip("\n")
                print("==============")
                print("Copying file in server "+ip)
                print("==============")
                call(["scp", "./install.py", "root@"+ip+":."])
                print("\n")
                if(not self.checkSuccessCommand(ip, "python --version")):
                    print("checking apt or yum...")
                    if(self.checkSuccessCommand(ip, "apt --version")):
                        print("apt checked! now installing python 2.")
                        if(self.checkSuccessCommand(ip, "apt-get install -y python")):
                            print("done! python instaled!")
                        else:
                            print("Error installing python!")
                            return
                    elif(self.checkSuccessCommand(ip, "yum --version")):
                        print("yum checked! now installing python 2.")
                        if(self.checkSuccessCommand(ip,"yum install -y python")):
                            print("done! python instaled!")
                        else:
                            print("Error installing python!")
                            return
                else:
                    print("python is current installed!")
            file.close()
            self.run("./install.py")
        else:
            print("not server for install docker, please addChildServer!")

    def checkSuccessCommand(self, ip, command):
        command = "\'\'" + command  +"\'\'"
        process = subprocess.Popen(["ssh", ip, "-l", "root", command],
                         stdout=subprocess.PIPE)
        while True:
            nextline = process.stdout.readline()
            if nextline == '' and process.poll() is not None:
                break
            sys.stdout.write(nextline)
            sys.stdout.flush()
        exitCode = process.returncode

        return (exitCode == 0)

    def run(self, command):
        if(os.path.isfile(self.servers_file)):
            file = open(self.servers_file, "r")
            for line in file:
                ip = line.rstrip("\n")
                print("==============")
                print("Running in server " + ip)
                print("==============")
                call(["ssh", ip, "-l", "root", "\"" + command + "\""])
                print("\n")
            file.close()
        else:
            print("not server for run commands, please addChildServer!")

    def hello(self):
        print("Hello Human! ٩(̾●̮̮̃̾ _•̃̾)۶ \nwhat do you want to do? (help)")
        command = False
        while(not command == "exit"):
            command = raw_input("$doud: ")
            command = str(command)

            if("help" == command or "" == command):
                self.help()
            if("addChildServer" in command):
                command_det = command.split(" ")
                self.addChildServer(command_det[1])
            if("run" in command):
                command_det = command.split(" ")[1:]
                self.run(" ".join(command_det))
            if("installDocker" in command):
                self.installDocker()

    def help(self):
        print(self.help_str)

doud = Doud()
doud.hello()
