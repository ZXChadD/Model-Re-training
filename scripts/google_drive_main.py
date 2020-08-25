from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive
import os
import glob

# authenticate
gauth = GoogleAuth()
gauth.LoadCredentialsFile("mycreds.txt")
drive = GoogleDrive(gauth)

# train folder for full annotations
train_file_list = drive.ListFile({'q': "'1HAEC8CQkcgFmGO9YL399AopIYkXTaBRK' in parents and trashed=false"}).GetList()

# directory to store the files
train_download_path = '../models/checkpoint_full/train/'

for i, file1 in enumerate(sorted(train_file_list, key=lambda x: x['title']), start=1):
    file1.GetContentFile(train_download_path + file1['title'])
    print('Downloaded {} from GDrive ({}/{})'.format(file1['title'], i, len(train_file_list)))

# eval folder for full annotations
eval_file_list = drive.ListFile({'q': "'1DHvC7AqnpnSThcvLjHBMf0z8AGeQwH_L' in parents and trashed=false"}).GetList()

# directory to store the files
eval_download_path = '../models/checkpoint_full/eval/'

for i, file2 in enumerate(sorted(eval_file_list, key=lambda x: x['title']), start=1):
    file2.GetContentFile(eval_download_path + file2['title'])
    print('Downloaded {} from GDrive ({}/{})'.format(file2['title'], i, len(eval_file_list)))
