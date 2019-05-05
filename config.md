### configuration
- to generate the config, run queue-plus atleast once
#### data/config.json
- client: what settings to use when connecting to the desired server
    - online: if the server is in online more
    - host: ip address of the server
    - port: port of the server (if none use 25565)
    - log_level: set the level based on how much you want to see in the console
- server: what setting to use for the proxy server
    - online: if the proxy should be in online mode
    - host: the hostname that you want the proxy to listen to
    - port: the port you want the proxy to listen to (normally 25565)
    - log_level: set the level based on how much you want to see in the console
- bridge: represents an instance of a connection between the server and the client
    - log_level: set the level based on how much you want to see in the console
- plugins: all the plugins
    - log_level: set the level based on how much you want to see in the console
- safe_disconnect: when you disconnect you wont disconnect the client
- version: [protocol version of minecraft](https://wiki.vg/Protocol_version_numbers)
#### data/accounts.csv
following the csv format input your accounts info here. Example in the default file.
#### bots/anti_afk/config.json
- randomize:
    - enabled: whether to randomize anti-afk loop
    - min: sets the minimum for a randomized variable by imputing a percentage (between 0 and 1)
- walk:
    - speed: how fast to move one block (in ticks)
    - smoothing: if you want to smooth out walking animations (multiplier)
    - distance: how far should be traveled in a direction before returning (in blocks)
 - fequency: how often to run the anti-afk measures
#### plugins/bridge/waiting_server/config.json
 - host: the waiting server ip
 - port: the waiting server port (normally 25565)
 - online: if the server is in online mode
#### bots/config.json: configure what accounts are running what bots
- bots: Array of all bot packages
    - \<{}\>: represents an array item
        - package: normally the folder or filename of the bot
        - class: The initiating class
- accounts: Array of all account related settings
    - \<{}\> represents an array item
        - username: The username (**CaSe Sensitive**) of the account. This is based on accounts.csv not when the account authenticates.
        - bots: An array of bot packages
            - \<package\>: the package name of a resisted bot

