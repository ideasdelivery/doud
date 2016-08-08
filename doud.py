#!/usr/bin/python
# coding: utf-8
# import argparse
import os
import re
import readline
import signal
import sys
from subprocess import call


# parser = argparse.ArgumentParser()
# parser.add_argument("-clusters", help="display list of clusters")
# print(parser.parse_args())

class Doud:
    def __init__(self):
        self.servers_file = "./servers_file.conf"
        self.help_str = {
            "addChildServer <server_ip>": "you can add a child server ip, but first they have to add the ssh key of this server on the other!",
            "run <command>":"run command in all childs server"}
        commands = ["run","addChildServer"]
        def completer(text, state):
            options = [i for i in commands if i.startswith(text)]
            if state < len(options):
                return options[state]
            else:
                return None

        readline.parse_and_bind("tab: complete")
        readline.set_completer(completer)

        def signal_handler(signal,frame):
            print("\nᕙ༼ ,,ԾܫԾ,, ༽ᕗ bye!")
            sys.exit(0)
        signal.signal(signal.SIGINT, signal_handler)

    def addChildServer(self, server_ip):
        pattern = re.compile("[0-9.]{7,15}")
        if(pattern.match(server_ip)):
            file = open(self.servers_file, "a")
            file.write(server_ip+"\n")
            file.close()
            print("Server: " + server_ip + " added success!")
        else:
            print("Invalid IP: " + server_ip)

    def run(self, command):
        if(os.path.isfile(self.servers_file)):
            file = open(self.servers_file, "r")
            for line in file:
                ip = line.rstrip("\n")
                print("==============")
                print("Running in server "+ip)
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

    def help(self):
        print(self.help_str)

doud = Doud()
doud.hello()
