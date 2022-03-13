from pyasn1.type.univ import Null
#@title
# Decoding Lotto Info From Website

import pandas as pd
import requests
import json

from bs4 import BeautifulSoup
from urllib.request import urlopen
from vega_datasets import data

from tqdm import tqdm

# -------------------------------------------> 로또 데이터 웹 크롤링 ------------------------------------
  # 최고 회차 
def getMaxRoundNum() -> int:

    url = "https://dhlottery.co.kr/common.do?method=main"  
    html = requests.get(url)  #html = urlopen(url) 

    if html.text is not None:
      soup = BeautifulSoup(html.text, 'html.parser') #"lxml")
      tag = soup.find(name='strong', attrs={'id': 'lottoDrwNo'})
    else:
      raise Exception('Error getting data from {}'.format(url))
    
    return int(tag.text)

# 로또 Json URL : https://www.dhlottery.co.kr/common.do?method=getLottoNumber&drwNo= + (회차번호)
# 로또 회차 Json 구조
#     {"totSellamnt":103479378000,"returnValue":"success","drwNoDate":"2022-02-19",
#      "firstWinamnt":1811116822,"drwtNo6":45,"drwtNo4":39,"firstPrzwnerCo":14,"drwtNo5":43,
#      "bnusNo":31,"firstAccumamnt":25355635508,"drwNo":1003,"drwtNo2":4,"drwtNo3":29,"drwtNo1":1}

def getLottoWinInfo(minDrwNo, maxDrwNo):
    drwtNo1 = []
    drwtNo2 = []
    drwtNo3 = []
    drwtNo4 = []
    drwtNo5 = []
    drwtNo6 = []
    bnusNo = []
    drwNoDate = []
    roundNo = []

    for i in tqdm(range(minDrwNo, maxDrwNo+1)):
        req_url = "https://www.dhlottery.co.kr/common.do?method=getLottoNumber&drwNo=" + str(i)   
        req_lotto = requests.get(req_url)
        lottoNo = req_lotto.json()
        if not lottoNo["returnValue"]=="fail":
          drwtNo1.append(lottoNo["drwtNo1"])
          drwtNo2.append(lottoNo["drwtNo2"])
          drwtNo3.append(lottoNo["drwtNo3"])
          drwtNo4.append(lottoNo["drwtNo4"])
          drwtNo5.append(lottoNo["drwtNo5"])
          drwtNo6.append(lottoNo["drwtNo6"])
          bnusNo.append(lottoNo["bnusNo"])
          drwNoDate.append(lottoNo["drwNoDate"])
          roundNo.append(lottoNo["drwNo"])
        else:
          print("Parsing result is ", lottoNo["returnValue"], '\n')
          continue


    lotto_dict = {"RoundNo":roundNo, "Date":drwNoDate, "Num1":drwtNo1, "Num2":drwtNo2, "Num3":drwtNo3, 
                  "Num4":drwtNo4, "Num5":drwtNo5, "Num6":drwtNo6, "bnsNum": bnusNo}

    df_lotto = pd.DataFrame(lotto_dict)
    df_lotto.index = df_lotto.index + 1 

    return df_lotto

#--------------------------- 여기서부터는 구글드라이브 파일 처리---------------------------------------#
# Import Modules for Google Drive API
import gspread

from googleapiclient.http import MediaFileUpload
from googleapiclient.discovery import build

from google.colab import auth
from google.colab import files

import os, sys

# Helpful message to display if the CLIENT_SECRETS_FILE is missing.
MISSING_CLIENT_SECRETS_MESSAGE = """
WARNING: Please configure OAuth 2.0
To make this sample run you will need to populate the client_secrets.json file
found at:
  %s
with information from the APIs Console
<https://code.google.com/apis/console#access>.
""" 



def uploadDataFilesToMyDrive(filelocation):
  print ('Authenticating...')  
  auth.authenticate_user()

  if not os.path.isfile('{name}.csv'.format(name=filelocation)):
    print("'{0}' not found, upload .csv file".format(filelocation))
    uploaded = files.upload()

  if not os.path.isfile('{name}.json'.format(name=filelocation)):
    print("'{0}' not found, upload .json file".format(filelocation))
    uploaded = files.upload()
    
  drive_service = build('drive', 'v3')
  

  LOTTO_DATA_FILENAME='lottoWinInfo_{min}_{max}'.format(min=g_minNum, max=g_maxNum)  
  
  #--------------- For .csv -----------------------------------------------------------------------
  _uploadfile(drive_service
              , fileName=LOTTO_DATA_FILENAME
              , mimeType='text/csv')

  #--------------- For .json -----------------------------------------------------------------------
  _uploadfile(drive_service
              , fileName=LOTTO_DATA_FILENAME
              , mimeType='application/json')
  
  #--------------- For .gsheet -------------------------------------------
  _uploadfile(drive_service
              , fileName=LOTTO_DATA_FILENAME
              , mimeType='application/vnd.google-apps.spreadsheet')


def _uploadfile(service, fileName, mimeType):
  searchfile_metadata = {
      'name': fileName,
      'mimeType': mimeType,
      'parents': '1WXbbz1f0QEdltlsYEFpqt_21zm-vkDQq' #Colab Notebooks
  }
  print(searchfile_metadata, '\n')
  items = searchFromDrive(service, searchfile_metadata)
  print(items, '\n')

  #When the file in the specific folder, use 'parents':["parent id"]
  uploadfile_metadata = {
      'name': fileName,
      'mimeType': mimeType,
      'parents': [items[0].get('parents') if items else '1WXbbz1f0QEdltlsYEFpqt_21zm-vkDQq']   #Colab Notebooks
  }
  __uploadfile(service, uploadfile_metadata, items[0] if items else None )
  

def __uploadfile(service, meta_data, file):

  filelocation=''

  if meta_data['mimeType'] == 'text/csv' or  meta_data['mimeType'] =='application/vnd.google-apps.spreadsheet':
    filelocation='{name}.csv'.format(name=meta_data['name'])    
  elif meta_data['mimeType']=='application/json':
    filelocation='{name}.json'.format(name=meta_data['name'])

  print('Guessed type - ', mimetypes.guess_type(filelocation)[0])

  media = MediaFileUpload( filelocation, #'content/drive/MyDrive/Colab Notebooks/lottoWinInfo.csv',
                        mimetype= mimetypes.guess_type(filelocation)[0],#meta_data['mimeType'],
                        resumable=True)

  print(meta_data)
  if file is None:
    file = service.files().create( 
                                    body=meta_data
                                    , media_body=media
                                    , fields='id, name, parents, mimeType' 
                                  ).execute()
    print('Created {2} {3} File ID: {0}, {1}'.format(file.get('id'), file.get('parents')
    , file.get('mimeType'), file.get('name')))
  else:
    file = service.files().update(
                                    fileId=file.get('id')
                                    , media_body=media
                                    , fields='id, name, parents, mimeType'
                                    ).execute()
    print('Updated {2} {3} File ID: {0}, {1}'.format(file.get('id'), file.get('parents')
    , file.get('mimeType'), file.get('name')))

  print('==============================================================================')

'''
@meta_data
EXAMPLE: folder_metadata = {
      'name': "Colab Notebooks",
      'mimeType': 'application/vnd.google-apps.folder',
      'parents': '0AJWOtiRiz6tlUk9PVA'
  }
'''
def searchFromDrive(service, meta_data):  
  page_token = None  
  while True:
      print("Searching.....")
      response = service.files().list(q="name='{name}' and mimeType='{mimeType}' and parents='{parents}'"
                                          .format(
                                              name=meta_data['name']
                                              , mimeType=meta_data['mimeType']
                                              , parents=meta_data['parents']
                                              )
                                          , spaces='drive'
                                          , fields='nextPageToken, files(id, name, mimeType, parents)'
                                          , pageToken=page_token).execute()
      
      for file in response.get('files', []):
          # Process change
          print ('Found file: %s (%s) - type:%s parents:%s ' % (file.get('name'), file.get('id'), file.get('mimeType'), file.get('parents')))
      page_token = response.get('nextPageToken', None)
      if page_token is None:
          break

  return response.get('files', [])

from pandas.io.parsers.readers import read_csv
from typing_extensions import Literal
import mimetypes

from google.colab import data_table
data_table.enable_dataframe_formatter() # table style


def mount(path):
  from google.colab import drive
  
  mntPath = path#'/content/drive'
  if not os.path.ismount(mntPath):
    drive.mount(mntPath)
  else:
    print("Aleady Mounted at ", mntPath)

def updateLottoData(_min=1, _max=getMaxRoundNum()):   
  #mount('/content/drive')

  global g_minNum, g_maxNum
  g_minNum=_min
  g_maxNum=_max
  targetFileName = "./lottoWinInfo_{min}_{max}".format(min=_min,max=_max)

  jsonfilename = '{filename}.json'.format(filename=targetFileName)
  csvfilename = '{filename}.csv'.format(filename=targetFileName)

  print(jsonfilename, csvfilename)

  if not (os.path.isfile(csvfilename) and os.path.isfile(jsonfilename)):
    df = getLottoWinInfo(g_minNum, g_maxNum)
    df.to_csv(csvfilename)
    df.to_json(jsonfilename)
    print('\n', df, '\n')   
  
  DownloadtoComputer(jsonfilename)
  DownloadtoComputer(csvfilename)
  
  uploadDataFilesToMyDrive(targetFileName)


def DownloadtoComputer(fileName):  

  if os.path.isfile(fileName):
    files.download(fileName)