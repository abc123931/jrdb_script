import zipfile
import subprocess

def unzip(file_name):
  res = {}
  # zipファイルを解凍する。
  with zipfile.ZipFile('/home/ec2-user/tmp_jrdb_data/' + file_name, 'r') as inputFile:
    inputFile.extractall('/home/ec2-user/tmp_jrdb_data/')
  # 解凍したファイルをUTF-8に変換
  res['file_name'] = file_name.replace('zip', 'txt')
  res['result'] = subprocess.call(['nkf', '-w', '--overwrite', '/home/ec2-user/tmp_jrdb_data/' + res['file_name']])
  
  return res
