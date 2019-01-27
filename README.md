# python-decora_wifi-cli
Leviton Decora wifi switch command line interface, written in Python, utilizing libraries written by Tlyakhov.

Command line control of Leviton Decora Smart WiFi Switches & Dimmers.
Only the required libraries to run this new interface are included with this download and none of Tlyakhov's libraries have been changed.
See tlyakhov/python-decora_wifi for more information about the original code.

You require the switch id(s) to send ON, OFF or 0-100 (for dimmer model) commands to your switch(es) through the Leviton cloud.  To generate a list of the switch ID's currently registered to your account, provide your email address and password on the command line as follows:
```
Decora-cli.py [email] [pswd] ?
```
Yields an output, such as:
```
Permission id#12345 (Accountid#9876)
Residence  id#9876  (your address)
Switch1    id#45678 (Familyroom)
Switch2    id#67890 (Livingroom)
Switch3    id#23456 (Bedroom)
```
Once you know your switch id(s), you can execute one or multiple commands on the same line:
```
Decora-cli.py [email] [pswd] [id#:ON|OFF|0-100] <[id#:ON|OFF|0-100]> <etc.>
```

Example:
```
Decora-cli.py johnsmith@gmail.com password123 67890:ON 45678:OFF 23456:50
```
The program executes the events and returns an output, such as:
```
1. #67890 ON (Livingroom)
2. #45678 OFF (Familyroom)
3. #23456 50% (Bedroom)
```
FYI, the original user interface by Tlyakhov is included with the file download:
```
cli-test.py
```
