import mold
import traceback
import re
from base import Base

class Result(Base):
    ''''''
    def __init__(self, date, baba_id, race_no):
        super().__init__()
        self.date = date
        self.baba_id = baba_id
        self.race_no = race_no

    def main(self):
        '''主処理'''

        # HTMLファイルからデータ取得
        soup = self.get_soup('result20230105_106_11')

        # ヘッダのレース番号・レース名を取得
        race_header = soup.find_all('div', class_ = 'hdg-l2-06-container')
        if len(race_header) == 0:
            # TODO 取得失敗ログ
            return
        elif len(race_header) >= 2:
            # TODO 複数取れたので一番上から取るログ
            pass

        # TODO 間に空白が入ってるレースで調査
        race_name = re.search(f'{self.race_no}R (.*) ', race_header[0].text)
        if race_name == None:
            pass # TODO ログでレース名取得に失敗
        else:
            self.race_name = race_name.groups()[0].strip()

        # タイトルの横につく画像からTODOを取得
        str_race_header = str(race_header)
        # TODO ここにstr_race_headerの画像から判断できる情報を取得

        # レース概要を取得
        race_summary = soup.find_all('div', class_ = 'box-note-01')
        if len(race_summary) == 0:
            # TODO 取得失敗ログ
            return
        elif len(race_summary) >= 2:
            # TODO 複数取れたので一番上から取るログ
            pass

        # コース情報
        course_summary = re.search('(.)(\d+)M', str(race_summary[0].find('em')))
        if course_summary == None:
            pass # TODO ログでレース名取得に失敗
        else:
            self.race_type, self.distance = course_summary.groups()

        # レース条件
        race_condition_summary = str(race_summary[0].find_all('li', class_ = 'first-child')[0])

        # 年齢条件
        age_term_match = re.search('サラ系(.)歳(.)', race_condition_summary)
        if age_term_match == None:
            pass # TODO ログでレース名取得に失敗
        else:
            if age_term_match.groups()[1] == '上':
                self.age_term = mold.full_to_half(age_term_match.groups()[0]) + '歳上'
            else:
                self.age_term = mold.full_to_half(age_term_match.groups()[0]) + '歳'

        # 国籍条件 country_term
        if '（国際）' in race_condition_summary:
            self.country_term = '国際'
        ### elif TODO 混合確認

        # 地方条件 local_term
        if '（特指）' in race_condition_summary:
            self.local_term = '特指'
        ### elif TODO カク指、マル指確認

        # 斤量条件
        if 'ハンデ' in race_condition_summary:
            self.load_type = 'ハンデ'
        ### elif TODO 定量、別定、馬齢確認

        # 性別条件 TODO 牝限、牝牡(セ以外)限定確認
        pass

        # クラス名のないタグ内から情報取得
        for li in race_summary[0].find_all('li'):
            # 天候
            weather_match = re.search('天候：(.+)</li>', str(li))
            if weather_match != None:
                self.weather = mold.rm(weather_match.groups()[0])

            # 馬場状態(芝)
            grass_condition_match = re.search('芝：(.+)</li>', str(li))
            if grass_condition_match != None:
                self.grass_condition = mold.rm(grass_condition_match.groups()[0])

            # 馬場状態(ダ) TODO match条件確認(ダかダートか)
            dirt_condition_match = re.search('ダート：(.+)</li>', str(li))
            if dirt_condition_match != None:
                self.dirt_condition = mold.rm(dirt_condition_match.groups()[0])

            # 1着賞金
            first_prize_match = re.search('1着：(.+)円', str(li))
            if first_prize_match != None:
                self.first_prize = first_prize_match.groups()[0].replace(',', '')

            # 2着賞金
            second_prize_match = re.search('2着：(.+)円', str(li))
            if second_prize_match != None:
                self.second_prize = second_prize_match.groups()[0].replace(',', '')

            # 3着賞金
            third_prize_match = re.search('3着：(.+)円', str(li))
            if third_prize_match != None:
                self.third_prize = third_prize_match.groups()[0].replace(',', '')

            # 4着賞金
            fourth_prize_match = re.search('4着：(.+)円', str(li))
            if fourth_prize_match != None:
                self.fourth_prize = fourth_prize_match.groups()[0].replace(',', '')

            # 5着賞金
            fifth_prize_match = re.search('5着：(.+)円', str(li))
            if fifth_prize_match != None:
                self.fifth_prize = fifth_prize_match.groups()[0].replace(',', '')

        exit()

        # try-except文
        try:
            hogehoge_list = self.hoge()
        except Exception as e:
            self.error_output('hogehogeでエラー', e, traceback.format_exc())
            return

if __name__ == '__main__':
    result = Result('20230105', '106', '11')
    result.main()
