import subprocess
import os

def move(local_file, remote_path_year, remote_path_type, remote_file):
  # 年のディレクトリがない場合作る
  try:
    os.chdir(remote_path_year)
  except:
    result = subprocess.call(['mkdir', remote_path_year])
    if (result == 0):
      subprocess.call(['cd', remote_path_year], shell=True)
    else:
      raise Exception("年のディレクトリに移動することができませんでした。")

  # タイプのディレクトリがない場合作る
  try:
    os.chdir(remote_path_type)
  except:
    result = subprocess.call(['mkdir', remote_path_type])
    if (result == 0):
        subprocess.call(['cd', remote_path_type], shell=True)
    else:
      raise Exception("タイプのディレクトリに移動することができませんでした。")
  
  try:
    subprocess.check_call(['mv', local_file, remote_file])
  except:
    raise Exception("ファイルの移動に失敗しました。")
  
