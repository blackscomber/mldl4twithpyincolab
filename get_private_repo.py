import os
from getpass import getpass
import urllib.parse

user = input('User name: ')
password = getpass('Password: ')
password = urllib.parse.quote(password) # your password is converted into url format
repo_name = input('Repo name: ')
branch_name = input('Branch name: ')

if branch_name == "master":
  cmd_string = 'git clone https://{0}:{1}@github.com/{0}/{2}.git'.format(user, password, repo_name)
else:
  cmd_string = 'git clone -b {3} https://{0}:{1}@github.com/{0}/{2}.git'.format(user, password, repo_name, branch_name)

os.system(cmd_string)
cmd_string, password = "","" # removing the password from the variable