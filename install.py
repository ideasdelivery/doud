#!/usr/bin/python

import os
import platform
import re
import getpass
from subprocess import call


class Installer:

    def __init__(self):
        dist = platform.dist()
        self.user = getpass.getuser()
        self.file = False
        self.platform = {"system": platform.system(),
                         "dist": (dist[0].lower(), re.search("[0-9]{1,10}", dist[1].lower()).group(0), dist[2].lower()),
                         "release": platform.uname()[2],
                         "uname": platform.uname()}

        self.minKernelVersion = {
            "ubuntu": "3.11.0-15-generic",
            "centos": "3.10.0-229.el7.x86_64"
        }
        self.genericInstallation = {
            "ubuntu": [
                ['apt-get', 'update'],
                ["apt-get", "install", "-y", "apt-transport-https",
                            "ca-certificates"],
                ["apt-key", "adv", "--keyserver", "hkp://p80.pool.sks-keyservers.net:80",
                    "--recv-keys", "58118E89F3A912897C070ADBF76221572C52609D"],
                ["touch", "/etc/apt/sources.list.d/docker.list"]
            ],
            "centos": [
                ["yum", "update"]

            ]
        }
        self.dependenciesByVersion = {
            "ubuntu": {
                "16": {
                    "commands": [
                        ["apt-get", "update"],
                        ["apt-get", "install", "-y", "linux-image-extra-" +
                            self.platform["release"]]
                    ],
                    "docker_file": "/etc/apt/sources.list.d/docker.list",
                    "repo_content": ["deb https://apt.dockerproject.org/repo ubuntu-xenial main"]
                },
                "14": {
                    "commands": [
                        ["apt-get", "install", "-y", "apparmor"]
                    ],
                    "docker_file": "/etc/apt/sources.list.d/docker.list",
                    "repo_content": ["deb https://apt.dockerproject.org/repo ubuntu-trusty main"]
                },
                "12": {
                    "commands": [["apt-get", "install", "-y", "apparmor"]],
                    "min_kernel": "3.13",
                    "update_kernel": [
                        ["apt-get", "install", "-y",
                            "linux-image-generic-lts-trusty"]
                    ],
                    "docker_file": "/etc/apt/sources.list.d/docker.list",
                    "repo_content": ["deb https://apt.dockerproject.org/repo ubuntu-precise main"]
                }
            },
            "centos": {
                "7": {
                    "docker_file": "/etc/yum.repos.d/docker.repo",
                    "repo_content": [
                        "[dockerrepo]",
                        "name=Docker Repository",
                        "baseurl=https://yum.dockerproject.org/repo/main/centos/7/",
                        "enabled=1",
                        "gpgcheck=1",
                        "gpgkey=https://yum.dockerproject.org/gpg"
                    ]
                }
            }
        }
        self.afterDependenciesInstallation = {
            "ubuntu": [
                ["apt-get", "update"],
                ["apt-get", "purge", "lxc-docker"],
                ["apt-cache", "policy", "docker-engine"],
                ["apt-get", "update"],
                ["apt-get", "install", "-y", "docker-engine"],
                ["service", "docker", "start"]
            ],
            "centos": [
                ["yum", "update"],
                ["yum", "install", "-y", "docker-engine"],
                ["service", "docker", "start"]
            ]
        }
        self.afterInstallationCommand = {
            "ubuntu": {
                "*": [["groupadd", "docker"],
                      ["usermod", "-aG", "docker", self.user]]
            }
        }

    def checkDependencies(self):
        if(self.platform["dist"][0] in self.minKernelVersion):
            print("supported system")
            dist = self.platform["dist"][0]
            # TODO:decide witch format is good.
            releaseRequired = re.sub(
                "[a-zA-Z]", "", self.minKernelVersion[dist])
            releaseVersion = re.sub("[a-zA-Z]", "", self.platform["release"])
            if(releaseRequired <= releaseVersion and self.minKernelVersion[dist] <= self.platform["release"]):
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
        print("dist_name: " + dist_name)
        print("dist_version: " + dist_version)
        versionDependencies = self.dependenciesByVersion[
            dist_name][dist_version]
        if("commands" in versionDependencies):
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
        docker_file = open(versionDependencies["docker_file"], "w")
        repos = versionDependencies["repo_content"]
        try:
            for repo in repos:
                docker_file.write(repo + "\n")
        finally:
            docker_file.close()

    def afterInstallConfiguration(self):
        dist_name = self.platform["dist"][0]
        dist_version = self.platform["dist"][1]
        if dist_name in self.afterInstallationCommand:
            command_version = self.afterInstallationCommand[dist_name]
            if(dist_version in command_version or "*" in command_version):
                if("*" in command_version):
                    dist_version = "*"
                for command in command_version[dist_version]:
                    call(command)

    def installDockerComposer(self):
        commands = [["curl", "-L", "https://github.com/docker/compose/releases/download/1.8.0/docker-compose-" +
                     self.platform["uname"][0] + "-" + self.platform["uname"][5], "-o",  "/usr/local/bin/docker-compose"],
                    ["chmod", "+x", "/usr/local/bin/docker-compose"]]
        for(command in commands):
            call(command)

    def install(self):
        if(self.checkDependencies()):
            installation = self.genericInstallation[self.platform["dist"][0]]
            for execution in installation:
                call(execution)
            installDocker = self.afterDependenciesInstallation[
                self.platform["dist"][0]]
            for execution in installDocker:
                call(execution)

            self.installDockerComposer()

Installer = Installer()

Installer.install()
