import os
from getpass import getpass
import urllib.parse

user = input('User name: ')
email = input('Email: ')
password = getpass('Password: ')
password = urllib.parse.quote(password) # your password is converted into url format


# !git config --global user.name "{your_username}"
# !git config --global user.email "{your_email_id}"
# !git config --global user.password "{your_password}"

cmd1_string = 'git config --global user.name "{your_username}'.format(your_username=user)
cmd2_string = 'git config --global user.email "{your_email_id}'.format(your_email_id=email)
cmd3_string = 'git config --global user.password "{your_password}'.format(your_password=password)

os.system(cmd1_string)
os.system(cmd2_string)
os.system(cmd3_string)

cmd3_string, password = "","" # removing the password from the variable