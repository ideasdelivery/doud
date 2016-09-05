# Doud

Doud is a platform in develpment for manage docker images in your own clod.

## how it works?

Doud only requires to add the parent's server ssh key on all the child servers and python 2.x installed.
then you can run ./doud.py and add a child Server.

### add ssh-key to child servers
add the server's ssh-key to all the child servers. Check [generating ssh-key](https://help.github.com/articles/generating-an-ssh-key/).
you can copy the key and add it to ~/.ssh/authorized_keys on the child server.

## Demo

![gif](http://imgur.com/4iGs2lp)


### 1. start doud
execute doud.py

```
./doud.py


Hello Human! ٩(̾●̾ _•̃̾)۶
what do you want to do? (help)
$doud:
```

### 2. addChildServer
run doud and addChildServer

  ./doud.py

```
$doud: addChildServer [server_ip]
```
replace the [server_ip]

### 3. Test connection

in doud, execute the command run "ls"

```
$doud: run "ls"
```

check ips or keys if some connection errors appear. You can check the ips in ".servers_file.conf".

### 4. installDocker

This command will install docker on all servers

```
$doud: installDocker
```

### 5. check docker version in servers
check the docker version installed on child servers.

```
$doud: run "docker --version"
```

### run command in only one server:

Example width random local ip

```
$doud: run_in 192.168.1.53 "docker --version"
```

### list all servers:

```
$doud: servers
```

response:
```
$doud:
* ip_server1
* ip_server2
* ...
* ip_serverN
```


#### Anotations:

* you can exit doud width "ctrl + c"

## future functionalities
* you will be able to install docker image and balance between servers width only a few commands in doud.
* backup and deployt images in all servers from doud.
* more

## That's all for now...
doud is in development. So if you want to help please make an issue or a pull request!
