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
default_location='/content/notebooks'

class CustomModules():
  def __init__(self, current_loaction:str=default_location):
    auth.authenticate_user()
    self._gauth = GoogleAuth()
    self._gauth.credentials = GoogleCredentials.get_application_default()
    self._drive = GoogleDrive(self._gauth)
    self._currentLocation = current_loaction
    
  # Authenticate and create the PyDrive client.
  # This only needs to be done once per notebook.
  def createFile(self, title : str, mimeType : str, parentId : str='1WXbbz1f0QEdltlsYEFpqt_21zm-vkDQq'):
    
    try:
      if(os.path.exists('/content/notebooks/{module}'.format(module=title))):
      #with open('/content/notebooks/{module}'.format(module=title), 'r') as f:
        print('| am already here444!!!')
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
  def listModules(self, folderId:str='1WXbbz1f0QEdltlsYEFpqt_21zm-vkDQq'):
    file_list = self._drive.ListFile({'q': "'{folderId}' in parents".format(folderId=folderId)}).GetList()    

    for f in file_list:
      print('title: %s, id: %s, mimetype: %s' % (f['title'], f['id'],f['mimeType']))