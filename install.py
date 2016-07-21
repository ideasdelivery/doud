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
            "ubuntu": [
                ['apt-get', 'update'],
                ["apt-get", "install", "apt-transport-https",
                            "ca-certificates"],
                ["apt-key", "adv", "--keyserver", "hkp://p80.pool.sks-keyservers.net:80",
                    "--recv-keys", "58118E89F3A912897C070ADBF76221572C52609D"]
            ]
        }
        self.versionDependencies = {
            "ubuntu": {
                "16.04": {
                    "commands": [
                        ["apt-get", "update"],
                        ["apt-get", "install", "linux-image-extra-" +
                            self.platform["release"]]
                    ]},
                "14.04": {
                    "commands": [["apt-get", "install", "-y", "apparmor"]]
                },
                "12.04": {
                    "commands": [["apt-get", "install", "-y", "apparmor"]],
                    "min_kernel": "3.13",
                    "update_kernel": [
                        ["apt-get", "install", "linux-image-generic-lts-trusty"]
                    ]
                }
            }
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
                self.installDependencies()
                return True
            else:
                print("system does not meet the dependencies.")
        else:
            print("-".join(self.platform.dist) + " platform not supported!")

        return False

    def installDependencies(self):
        dist_name = self.platform["dist"][0]
        dist_version = self.platform["dist"][1]
        versionDependencies = self.versionDependencies[dist_name][dist_version]
        commands = versionDependencies["commands"]
        for command in commands:
            call(command)
        if("min_kernel" in versionDependencies):
            if(versionDependencies["min_kernel"] <= self.platform["release"]):
                print("system meets dependencies.")
                return True
            else:
                print("updating kernel.")
                if("update_kernel" in versionDependencies):
                    for command in versionDependencies["update_kernel"]:
                        dist(command)

    def install(self):
        if(self.checkDependencies()):
            installation = self.installation[self.platform["dist"][0]]
            for execution in installation:
                call(execution)

Installer = Installer()

Installer.install()
