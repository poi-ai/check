import mold
import pandas as pd
import traceback
import re
from base import Base


class Race(Base):
    '''JBISから馬柱を取得する'''
    def __init__(self, date, baba_id, race_no):
        super().__init__()
        self.date = date
        self.baba_id = baba_id
        self.race_no = race_no

    def main(self):
        '''主処理'''

        # HTMLファイルからデータ取得
        soup = self.get_soup('race20230127_220_1')

        # レース概要を取得
        try:
            self.get_race_summary(soup)
        except Exception as e:
            self.error_output('レース概要取得処理でエラー', e, traceback.format_exc())

        # レース結果情報を取得
        try:
            self.get_horse_data(soup)
        except Exception as e:
            self.error_output('出走馬情報取得処理でエラー', e, traceback.format_exc())

    def get_race_summary(self, soup):
        '''レース概要を取得'''

        # ヘッダのレース番号・レース名を取得
        race_header = soup.find_all('div', class_ = 'box-inner reset-pt-10')
        if len(race_header) == 0:
            self.logger.error('JBIS出走表ページでタイトルの取得に失敗しました')
            return
        elif len(race_header) >= 2:
            self.logger.warning('JBIS出走表ページでタイトルクラスが複数見つかりました。最初のタグから抽出を行います。')

        # TODO 間に空白が入ってるレースで調査
        race_name = re.search(f'(.*)　(.*)', race_header[0].text)
        if race_name == None:
            self.logger.error('JBIS出走表ページでレース名の取得に失敗しました')
        else:
            self.race_name,self.horse_class = race_name.groups()

        # タイトルの横につく画像からTODOを取得
        str_race_header = str(race_header)
        # TODO ここにstr_race_headerの画像から判断できる情報を取得

        # レース概要を取得
        race_summary = soup.find_all('div', class_ = 'box-note-01')
        if len(race_summary) == 0:
            self.logger.error('JBIS出走表ページでレース概要の取得に失敗しました')
            return
        elif len(race_summary) >= 2:
            self.logger.warning('JBIS出走表ページでレース概要クラスが複数見つかりました。最初のタグから抽出を行います。')

        # コース情報
        course_summary = re.search('(.)(\d+)M', str(race_summary[0].find('em')))
        if course_summary == None:
            self.logger.error('JBIS出走表ページでコース情報の取得に失敗しました')
        else:
            self.race_type, self.distance = course_summary.groups()

        # レース条件
        race_condition_summary = str(race_summary[0].find_all('li', class_ = 'first-child')[0])

        # 馬齢条件
        age_term_match = re.search('サラ系(.)歳(.)', race_condition_summary)
        if age_term_match == None:
            self.logger.error('JBIS出走表ページで馬齢条件の取得に失敗しました')
        else:
            if age_term_match.groups()[1] == '上':
                self.age_term = mold.full_to_half(age_term_match.groups()[0]) + '歳上'
            else:
                self.age_term = mold.full_to_half(age_term_match.groups()[0]) + '歳'

        # 国籍条件
        if '（国際）' in race_condition_summary:
            self.country_term = '国際'
        elif '（混合）' in race_condition_summary:
            self.country_term = '混合'

        # 地方条件
        if '（特指）' in race_condition_summary:
            self.local_term = '特指'
        elif '（指定）' in race_condition_summary: # TODO カク指、マル指
            self.local_term = '指定'

        # 斤量条件
        if '定量' in race_condition_summary:
            self.load_type = '定量'
        elif '馬齢' in race_condition_summary:
            self.load_type = '馬齢'
        elif '別定' in race_condition_summary:
            self.load_type = '別定'
        elif 'ハンデ' in race_condition_summary:
            self.load_type = 'ハンデ'

        # 性別条件
        if '牡・牝' in race_condition_summary:
            self.gender_term = '牡牝'
        elif '牝' in race_condition_summary:
            self.gender_term = '牝'

        # クラス名のないliタグ内から情報取得
        for li in race_summary[0].find_all('li'):
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

        return

    def get_race_():
        pass

    def hogehoge(self):
        # try-except文
        try:
            hogehoge_list = self.hoge()
        except Exception as e:
            self.error_output('hogehogeでエラー', e, traceback.format_exc())
            return

if __name__ == '__main__':
    race = Race('20230127','220','1')
    race.main()
