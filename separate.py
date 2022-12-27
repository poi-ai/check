import time
import re
import requests
from bs4 import BeautifulSoup

def error_search(association):
    with open(f'{association}.log.txt', 'r', encoding='utf-8') as f:
        # 1行ずつ処理する
        for line in f:
            # 正規表現で「(race_id:race_id)のerror_massage」に合致する文字列を検索する
            match = re.search(r'\(race_id:(\d+)\)の(.+)', line)
            # 合致する文字列が見つかった場合
            if match:
                # race_idを取り出す
                race_id = match.group(1)
                # error_massageを取り出す
                text = match.group(2)

                # 中止事由の枠を取得
                cause = get_discontinued_message(race_id, association)

                # clustering.csvをUTF-8で開く
                with open(f'{association}_clustering.csv', 'a', encoding='utf-8') as g:
                    # clustering.csvに「race_id,error_massage」という形で出力する
                    g.write(f'{race_id},{text},{cause}\n')

def get_discontinued_message(race_id, association):
    if association == 'jra':
        url = f'https://race.netkeiba.com/race/result.html?race_id={race_id}&rf=race_list'
    else:
        url = f'https://nar.netkeiba.com/race/result.html?race_id={race_id}&rf=race_list'

    time.sleep(1)

    r = requests.get(url)
    soup = BeautifulSoup(r.content, 'lxml')

    cause = soup.find('div', 'Race_Infomation_Box')
    if cause != None:
        return cause.text
    else:
        return ''

error_search('jra')
error_search('nar')