import time
import pdb
import os
from os.path import join, dirname
from dotenv import load_dotenv
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from datetime import datetime, timedelta

class FileDownload:
  def __init__(self, type):
    self.file_names = []
    self.type = type
    self.date = datetime.now()
    options = Options()
    # ヘッドレスモードを有効にする（次の行をコメントアウトすると画面が表示される）。
    options.add_argument('--headless')
    options.add_argument('--disable-popup-blocking')
    # ChromeのWebDriverオブジェクトを作成する。
    self.driver = webdriver.Chrome(chrome_options=options)

    # ヘッドレスChromeでファイルダウンロードするにはここが必要
    self.driver.command_executor._commands["send_command"] = ("POST", '/session/$sessionId/chromium/send_command')
    self.driver.execute("send_command", {
        'cmd': 'Page.setDownloadBehavior',
        'params': {
            'behavior': 'allow',
            'downloadPath': '/home/ec2-user/tmp_jrdb_data/' # ダウンロード先
         }
    })

    # ログイン情報
    dotenv_path = join(dirname(__file__), '.env')
    load_dotenv(dotenv_path)
    member_num = os.environ.get("MEMBER_NUM") # 環境変数の値を代入
    password = os.environ.get("PASSWORD") # 環境変数の値を代入
    # JRDBにログイン
    self.driver.get('http://' + member_num + ':' + password + '@' + 'www.jrdb.com/member/n_index.html')
    time.sleep(3)

  def download(self):
    #各データのダウンロード画面を表示
    self.driver.get('http://www.jrdb.com/member/datazip/' + self.type + '/index.html')
    time.sleep(3)

    # 単体データコーナーの最新のファイルを入手
    ul = self.driver.find_elements_by_tag_name('ul')[1]
    for i in range(0, 2):
      li = ul.find_elements_by_tag_name('li')[i]
      li.find_elements_by_tag_name('a')[0].click()
      # ファイル名取得
      print(li.find_elements_by_tag_name('a')[0].text)
      self.file_names.append(li.find_elements_by_tag_name('a')[0].text)
      time.sleep(3)
    # クローム閉じる
    self.driver.quit()

  def downloadLatest(self):
    # 土曜日を取得(いつ実行しても最新のものを取れるよう調整)
    if self.date.weekday() < 3:
      saturday = self.date+timedelta(-(self.date.weekday() + 2)) 
    else:
      saturday = self.date+timedelta(5 - self.date.weekday())
    
    # ファイル名取得
    file_name = self.type.upper()+saturday.strftime('%Y%m%d')[2:]+'.zip'

    # カテゴリ選択
    if self.type == 'Kza':
      category = 'Ks'
    elif self.type == 'Cza':
      category = 'Cs'
    elif self.type == 'Kta':
      category = 'Kta'
    elif self.type == 'Mza':
      category = 'Ms'
    else:
      raise Exception('カテゴリがありません')

    # ファイルダウンロード
    self.driver.get('http://www.jrdb.com/member/datazip/'+category+'/'\
      +saturday.strftime('%Y')+'/'+file_name)
    time.sleep(3)
    self.file_names.append(file_name)
    # クローム閉じる
    self.driver.quit()
  
  def getFileNames(self):
    return self.file_names
