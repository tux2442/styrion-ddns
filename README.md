# Styrion DNS Updater
This Python Script updates DNS entries on the Styrion provider. It can update an arbitrary amount of entries, based on a config.

The script can run as SystemD Service

## Installation

Clone Gitrepo to an installation path (eg ```/opt/ddns-styrion```)
```shell
git clone https://github.com/tux2442/styrion-ddns
```

Add a system user for Service
````shell
sudo user add -r ddns-updater
````

Configure the service based on the ```settings_example.ini``` with the ```/etc/ddns-styrion/config.ini```

Link SystemD-service to install it and start it
```shell
ln -s INSTALLATIONPATH /etc/systemd/system
systemctl daemon-reload
systemctl start styrion-dns-update
```

Update an IP with a get request
```
http://SERVER-IP:8000/?ip=PUBLIC-IP
```