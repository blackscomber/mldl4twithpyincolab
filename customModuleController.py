from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive
from google.colab import auth, files
from oauth2client.client import GoogleCredentials

#from .files import GoogleDriveFile

import sys, os

'''
<mimeType>
.py : 'application/x-python-code'
.ipynb : 'application/vnd.google.colaboratory'

<id>
root
Colab Notebooks: 1WXbbz1f0QEdltlsYEFpqt_21zm-vkDQq
'''

local_location='/content/notebooks'
drive_github_location='/content/drive/MyDrive/ColabNotebooks/mldl4trading'
current_location=local_location

colab_folderId = '1WXbbz1f0QEdltlsYEFpqt_21zm-vkDQq'
mldl4t_folderId = '1M8Db9NtqjU0_ybY49OCtZWldWT0C99d9'
current_folderId = mldl4t_folderId

class CustomModules():
  def __init__(self, loaction:str=current_location):
    auth.authenticate_user()
    self._gauth = GoogleAuth()
    self._gauth.credentials = GoogleCredentials.get_application_default()
    self._drive = GoogleDrive(self._gauth)
    self._currentLocation = loaction
    
  # Authenticate and create the PyDrive client.
  # This only needs to be done once per notebook.
  def createFile(self, title : str, mimeType : str, parentId : str=current_folderId):
    
    try:
      if(os.path.exists('{location}/{module}'.format(location=current_location, module=title))):
      #with open('{location}/{module}'.format(location=current_location, module=title), 'r') as f:
        print('I am here55 at {location}/{module}'.format(location=current_location, module=title))
    except:
      module = self._drive.CreateFile({'title': title, 'mimeType':mimeType, 'parents':[{"kind": "drive#fileLink","id": parentId}] })
      print(module)
      module.Upload()
    
    # module = self._drive.CreateFile({'title': title, 'mimeType':mimeType, 'parents':[{"kind": "drive#fileLink","id": parentId}] })
    # module.get
    # print(module)
    # module.Upload()
    # #if self._drive.get('title')
    # t = GoogleDriveFile(self._gauth)
    # t.Upload()

    

  # 'root' in parents for folderId is 'MyDrive'
  def listModules(self, folderId:str=current_folderId):
    file_list = self._drive.ListFile({'q': "'{folderId}' in parents".format(folderId=folderId)}).GetList()    

    for f in file_list:
      print('title: %s, id: %s, mimetype: %s' % (f['title'], f['id'],f['mimeType']))