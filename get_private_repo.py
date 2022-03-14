import os
from getpass import getpass
import urllib.parse

user = input('User name: ')
password = getpass('Password: ')
password = urllib.parse.quote(password) # your password is converted into url format
repo_name = input('Repo name: ')
branch_name = input('Branch name: ')

cmd_string = 'git push https://{user}:{password}@github.com/{user}/{repo_name}.git'.format(user=user, password=password, repo_name=repo_name)
#git push https://<username>:<password>@github.com/<username>/<repository-name>

# if branch_name == "master":
#   cmd_string = 'git clone https://{user}:{password}@github.com/{user}/{repo_name}.git'.format(user=user, password=password, repo_name=repo_name)
# else:
#   cmd_string = 'git clone -b {branch_name} https://{user}:{password}@github.com/{user}/{repo_name}.git'.format(user=user, password=password, repo_name=repo_name, branch_name=branch_name)

os.system(cmd_string)
cmd_string, password = "","" # removing the password from the variable

#git clone https://username:password@github.com/path_to/myRepo.git