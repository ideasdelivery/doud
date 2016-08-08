#!/usr/bin/python

import argparse
import re
import sys
from subprocess import call


parser = argparse.ArgumentParser()
parser.add_argument("-clusters", help="display list of clusters")
print(parser.parse_args())


class Doud:

    def __init__(self):
        self.servers_file = "./servers_file.conf"
        self.help_str = {
            "addChildServer <server_ip>": "you can add a child server ip, but first they have to add the ssh key of this server on the other!"}

    def addChildServer(self, server_ip):
        pattern = re.compile("[0-9.]{7,15}")
        if(pattern.match(server_ip)):
            file = open(self.servers_file, "a")
            file.write(server_ip)
            file.close()
            print("Server: " + server_ip + " added success!")
        else:
            print("Invalid IP: " + server_ip)

    def run(self, command):
        file = open(self.servers_file, "r")
        for line in file:
            call(["ssh", line, "-l", "root", "\"" + command + "\""])
        file.close()

    def hello(self):
        print("Hello Human!\nwhat do you want to do? (help)")
        command = False
        while(not command == "exit"):
            command = raw_input("$doud: ")
            command = str(command)
            print(command)

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
