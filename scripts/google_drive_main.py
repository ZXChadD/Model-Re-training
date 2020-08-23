from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive
import os
import glob

## authenticate ##
gauth = GoogleAuth()
gauth.LoadCredentialsFile("mycreds.txt")

## train folder for full annotations ##
drive = GoogleDrive(gauth)
file_list = drive.ListFile({'q': "'1FZafJnC76WuEXXjmufw3JQ9IV7PBx_OK' in parents and trashed=false"}).GetList()

## directory to store the files ##
local_download_path = '../models/checkpoint_full/train/'

## remove old files ##
files = glob.glob(local_download_path)
for f in files:
    os.remove(f)

for i, file1 in enumerate(sorted(file_list, key = lambda x: x['title']), start=1):
    file1.GetContentFile(local_download_path + file1['title'])
    print('Downloaded {} from GDrive ({}/{})'.format(file1['title'], i, len(file_list)))


