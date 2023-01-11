import log
import mold
import re
from bs4 import BeautifulSoup

def main():
    logger = log.Logger()

    print('-------------------------')


    for html_name in ['kitasan', 'sunday']:
        soup = BeautifulSoup(open(f'{html_name}.html', encoding='utf-8'), 'lxml')

        title = soup.find('title').text

        horse_name = title[:title.find('｜')]

        m = re.search('(.+)\((.+)\)', horse_name)
        if m != None:
            horse_name = m.groups()[0]
            country = m.groups()[1]
        else:
            country = 'JPN'

        profile = soup.find_all('table', class_ = 'tbl-data-05 reset-mb-40')

        if len(profile) == 0:
            logger.error('プロフィールテーブルが見つかりません')
            return
        elif len(profile) > 1:
            logger.warning('プロフィールテーブルが複数見つかりました。一番上のテーブルを取得対象にします')

        matches = re.findall(r'<.+>(.+?)</.+>', mold.rm_charcode(str(profile[0])))

        print(matches)

        #texts = [mold.rm(tag.get_text()) for tag in tags]
        #print(texts)


        print('-------------------------')

if __name__ == '__main__':
    main()