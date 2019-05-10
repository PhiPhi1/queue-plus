# Queue Plus
version: ALPHA v0.3.2
### features:
- plugins
- hot swappable accounts
- waiting server
- waiting room
- configurable
- queue boss bar
- account connection management
- anti-afk
- anti-kick
- auto-reconnect
- bots
- whitelist

### commands:
- ```/phelp```: lists all commands
- ```/connect <session id>```: switch to another session 
- ```/sessions```: lists all sessions by id and name
- ```/accounts```: list all accounts by id and name
- ```/showqueue [<session id>]```: shows a boss bar for the queue of a session id, if none is input it will show all
- ```/hidequeue [<session id>]```: shows a boss bar for the queue of a session id, if none is input it will show all
- ```/wait [<account id>]```: sends you to a waiting server with the login info of the account id, if no account is input it will default to the first one
- ```/disconnect [<session id>]```: disconnects a session, if none is input it will disconnect the current one
- ```/reconnect <account id>```: reconnects a session by account id. ***warning: there are no protections against connecting an already connected account***
- ```/pwhitelist <add|remove|disable|enable|list>```: sets up a whitelist. Use "*" as a wildcard for a variable and "auto" to automatically set a username uuid or ip.
## installation
### automatic
- [Windows](https://github.com/the-emperium/queue-plus/releases/tag/0.3.2)
### manual
- [installation guide](https://github.com/the-emperium/queue-plus/blob/master/install.md)
## configuration
- [configuration guide](https://github.com/the-emperium/queue-plus/blob/master/config.md)
## starting
### automatic
- windows: run the ```start.bat```
### manual
 - open a command window inside the program folder
 - run ```python start.py```
## troubleshooting
### wont start
check:
- all the requirements were properly installed
- your profile information is correct
- the server connection info is correct
- if your still having issues take a screenshot of the console and post an issue
### wont exit
- before killing the process with a process manager try ```CTRL + C```
