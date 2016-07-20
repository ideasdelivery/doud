#!/usr/bin/python3

import os
import platform
import re

from subprocess import call


class Installer:

    def __init__(self):
        dist = platform.dist()
        self.platform = {"system": platform.system(),
                         "dist": (dist[0].lower(), dist[1].lower(), dist[2].lower()),
                         "release": platform.uname()[2]}
        self.dependencies = {
            "ubuntu": "3.11.0-15-generic"
        }
        self.installation = {
            "ubuntu": [['apt-get', 'update'],
                       ["apt-get", "install", "apt-transport-https", "ca-certificates"]]
        }

    def checkDependencies(self):
        if(self.platform["dist"][0] in self.dependencies):
            print("supported system")
            dist = self.platform["dist"][0]
            # TODO:decide witch format is good.
            releaseRequired = re.sub("[a-zA-Z]", "", self.dependencies[dist])
            releaseVersion = re.sub("[a-zA-Z]", "", self.platform["release"])
            if(releaseRequired <= releaseVersion and self.dependencies[dist] <= self.platform["release"]):
                print("system meets dependencies.")
                return True
            else:
                print("system does not meet the dependencies.")
        else:
            print("-".join(self.platform.dist) + " platform not supported!")

        return False

    def install(self):
        if(self.checkDependencies()):
            installation = self.installation[self.platform["dist"][0]]
            for execution in installation :
                call(execution)

Installer = Installer()

Installer.install()
