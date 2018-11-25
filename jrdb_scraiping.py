import os
import file_move
import sys
import pdb
import datetime
import shutil
from log.logger import Logger
from unzip import unzip
from file_download import FileDownload

# ログ準備
log = Logger().logger

def scraiping(type):
  # ファイルダウンロード
  try:
    # FileDownloadインスタンス化
    file_download = FileDownload(type)
    if (type == 'Kyi' or type == 'Sed' or type == 'Ukc' or type == 'Bac' or type == 'Kab' or type == 'Cyb'):
      file_download.download()
    else:
      file_download.downloadLatest()
    # 対象ファイルの取得
    file_names = file_download.getFileNames()
  except Exception as e:
    log.error(e)
    log.error('ファイルが正常にダウンロードされませんでした。')
    sys.exit()

  # ファイルアップロード・削除
  for file_name in file_names:
    # 正常にファイルがダウンロードできている場合
    if os.path.exists('/home/ec2-user/tmp_jrdb_data/' + file_name):
      try:
        # zip 解凍
        res = unzip(file_name)
        if (res['result'] == 0):
          remote_path_year = '/home/ec2-user/jrdb_data/20'+file_name[3:5]+"/"
          remote_path_type = remote_path_year + file_name[:3]
          file_move.move('/home/ec2-user/tmp_jrdb_data/'+res['file_name'], remote_path_year, remote_path_type, res['file_name'])
        else:
          log.error('文字コードの変換に失敗しました。')
          sys.exit()
      except Exception as e:
        log.error(e)
        log.error('ファイルのアップロードに失敗しました。要リカバリ (filename=' + file_name + ')')
        sys.exit()
    else:
      log.error('ファイルが正常にダウンロードされませんでした。')
      sys.exit()

  # ディレクトリを削除
  try:
    shutil.rmtree('/home/ec2-user/tmp_jrdb_data')
  except Exception as e:
    log.error(e)
    log.error('ディレクトリの削除に失敗しました。')
