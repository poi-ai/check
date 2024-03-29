import mold
import traceback
import re
from base import Base

class Result(Base):
    '''JBISからレース結果を取得する'''
    def __init__(self, date, baba_id, race_no):
        super().__init__()
        self.date = date
        self.baba_id = baba_id
        self.race_no = race_no

    def main(self):
        '''主処理'''

        # HTMLファイルからデータ取得
        soup = self.get_soup('result20230105_106_11')

        # レース概要を取得
        try:
            self.get_race_summary(soup)
        except Exception as e:
            self.error_output('レース概要取得処理でエラー', e, traceback.format_exc())

        # レース結果情報を取得
        try:
            self.get_horse_result(soup)
        except Exception as e:
            self.error_output('出走馬結果取得処理でエラー', e, traceback.format_exc())

        # ラップタイムを取得
        try:
            self.get_lap(soup)
        except Exception as e:
            self.error_output('ラップタイム取得処理でエラー', e, traceback.format_exc())

        # コーナー通過順位を取得
        try:
            self.get_corner_rank(soup)
        except Exception as e:
            self.error_output('コーナー通過順位取得処理でエラー', e, traceback.format_exc())

    def get_race_summary(self, soup):
        '''レース概要を取得'''

        # ヘッダのレース番号・レース名を取得
        race_header = soup.find_all('div', class_ = 'hdg-l2-06-container')
        if len(race_header) == 0:
            self.logger.error('JBISレース結果ページでタイトルの取得に失敗しました')
            return
        elif len(race_header) >= 2:
            self.logger.warning('JBISレース結果ページでタイトルクラスが複数見つかりました。最初のタグから抽出を行います。')

        # TODO 間に空白が入ってるレースで調査
        race_name = re.search(f'{self.race_no}R (.*) ', race_header[0].text)
        if race_name == None:
            self.logger.error('JBISレース結果ページでレース名の取得に失敗しました')
        else:
            self.race_name = race_name.groups()[0].strip()

        # タイトルの横につく画像からTODOを取得
        str_race_header = str(race_header)
        # TODO ここにstr_race_headerの画像から判断できる情報を取得

        # レース概要を取得
        race_summary = soup.find_all('div', class_ = 'box-note-01')
        if len(race_summary) == 0:
            self.logger.error('JBISレース結果ページでレース概要の取得に失敗しました')
            return
        elif len(race_summary) >= 2:
            self.logger.warning('JBISレース結果ページでレース概要クラスが複数見つかりました。最初のタグから抽出を行います。')

        # コース情報
        course_summary = re.search('(.)(\d+)M', str(race_summary[0].find('em')))
        if course_summary == None:
            self.logger.error('JBISレース結果ページでコース情報の取得に失敗しました')
        else:
            self.race_type, self.distance = course_summary.groups()

        # レース条件
        race_condition_summary = str(race_summary[0].find_all('li', class_ = 'first-child')[0])

        # 馬齢条件
        age_term_match = re.search('サラ系(.)歳(.)', race_condition_summary)
        if age_term_match == None:
            self.logger.error('JBISレース結果ページで馬齢条件の取得に失敗しました')
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

        return

    def get_horse_result(self, soup):
        '''レース結果情報を取得'''

        # レース結果テーブルからデータ取得
        # リンクから各種IDをとるためpd.read_htmlは使わない
        result_tables = soup.find_all('table', class_ = 'tbl-data-04 cell-align-c')
        if len(result_tables) == 0:
            self.logger.error('JBISレース結果ページで結果テーブルの取得に失敗しました')
            return
        elif len(result_tables) >= 2:
            self.logger.warning('JBISレース結果ページで結果テーブルが複数見つかりました。最初のタグから抽出を行います。')

        # 各行(=各馬)ごとにデータを取得する
        for row_index, tr in enumerate(result_tables[0].find_all('tr')):
            # 最初の行はカラム名なので飛ばす
            if row_index == 0: continue

            # 着順取得
            self.rank = mold.rm(tr.find('th').text)

            # 列を行ごとに区切って対応するデータを取得
            td = tr.find_all('td')

            # 枠番、馬番取得
            self.frame_no = mold.rm(td[0].text)
            self.horse_no = mold.rm(td[1].text)

            # 競走馬ID、競走馬名取得 TODO 出身国、ブリンカー、地方マーク取得
            horse_id_match = re.search('<a href="/horse/(.+)/"><em>(.+)</em>', str(td[2]))
            if horse_id_match is None:
                self.logger.error('JBISレース結果ページで競走馬IDの取得に失敗しました')
            else:
                self.horse_id, self.horse_name = horse_id_match.groups()

            # 父名・母名・セレクトセール情報取得
            for li in td[2].find_all('li'):
                # 父名
                father_match = re.search('父：<a href="/horse/(.+)/">(.+)</a>', str(li))
                if father_match != None:
                    self.father_id, self.father_name = father_match.groups()

                # 母名
                mother_match = re.search('母：<a href="/horse/(.+)/">(.+)</a>', str(li))
                if mother_match != None:
                    self.mother_id, self.mother_name = mother_match.groups()

                # セレクトセール情報
                select_sale_match = re.search('<a href="/seri/(.+)/(.+)/">(.+)</a>', str(li))
                if select_sale_match != None:
                    self.select_sale_year, self.select_sale_id, self.select_sale_name = select_sale_match.groups()

                select_sale_price_match = re.search('(\d+)\.(\d+)万円', str(li))
                if select_sale_price_match != None:
                    self.select_sale_price = str(int(select_sale_price_match.groups()[0]) * 10000 + int(select_sale_price_match.groups()[1]) * 1000)

            # 性別・馬齢
            self.gender= td[3].text[:1]
            self.age = td[3].text[1:]

            # 騎手ID・騎手名・斤量 TODO 減量マーク取得
            jockey_match = re.search('"/race/jockey/(.+)/">(.+)</a><br/>(\d\d\.\d)</td>', str(td[4]))
            if jockey_match != None:
                self.jockey_id, self.jockey_name, self.load = jockey_match.groups()

            # 走破タイム・着差・通過順位・上がり3F・スピード指数・人気
            self.goal_time = mold.change_seconds(td[5].text)
            self.diff = td[6].text
            self.pass_rank = td[7].text
            self.agari = td[8].text
            self.sp_shisu = td[9].text
            self.popular = td[10].text

            # 馬体重・馬体重増減
            weight_match = re.search('<td>(.+)<br/>（(.+)）</td>', str(td[11]))
            if weight_match != None:
                self.weight, self.weight_change = weight_match.groups()

            # 調教師ID・調教師名・調教師所属
            trainer_match = re.search('<a href="/race/trainer/(.+)/">(.+)</a><br/>（(.+)）', str(td[12]))
            if trainer_match != None:
                self.trainer_id, self.trainer_name, self.trainer_belong = trainer_match.groups()

            # 馬主ID・馬主名
            owner_match = re.search('<a href="/race/owner/(.+)/">(.+)</a><br/>', str(td[13]))
            if owner_match != None:
                self.owner_id, self.owner_name = owner_match.groups()

            # 生産牧場ID・生産牧場名
            breeder_match = re.search('<a href="/breeder/(.+)/">(.+)</a>', str(td[13]))
            if breeder_match != None:
                self.breeder_id, self.breeder_name = breeder_match.groups()

            '''
            print(self.rank)
            print(self.frame_no)
            print(self.horse_no)
            print(self.horse_id)
            print(self.horse_name)
            print(self.father_id)
            print(self.father_name)
            print(self.mother_id)
            print(self.mother_name)
            print(self.select_sale_year)
            print(self.select_sale_id)
            print(self.select_sale_name)
            print(self.select_sale_price)
            print(self.gender)
            print(self.age)
            print(self.jockey_id)
            print(self.jockey_name)
            print(self.load)
            print(self.goal_time)
            print(self.diff)
            print(self.pass_rank)
            print(self.agari)
            print(self.sp_shisu)
            print(self.popular)
            print(self.weight)
            print(self.weight_change)
            print(self.trainer_id)
            print(self.trainer_name)
            print(self.trainer_belong)
            print(self.owner_id)
            print(self.owner_name)
            print(self.breeder_id)
            print(self.breeder_name)
            '''

    def get_lap(self, soup):
        '''ラップタイムを取得する'''

        # ラップタイムテーブルの存在チェック
        if '<h3 class="hdg-l3-01"><span>タイム</span></h3>' not in str(soup):
            self.logger.info('ラップタイムテーブルが存在しません')
            return

        # テーブル一覧を取得
        tables = soup.find_all('table', class_ = 'tbl-data-05')

        # ラップタイムテーブルは一番上にある
        lap_time_table = tables[0]

        # 一行ずつチェック
        for tr in lap_time_table.find_all('tr'):
            if tr.find('th').text == '上がり':
                self.agari_4f, self.agari_3f = mold.rm_nl(tr.find('td').text).split('-')

            if tr.find('th').text == 'ハロンタイム':
                self.lap_time = tr.find('td').text

    def get_corner_rank(self, soup):
        '''コーナー通過順位を取得する'''

        # ラップタイムテーブルの存在チェック
        if '<h3 class="hdg-l3-01"><span>コーナー通過順位</span></h3>' not in str(soup):
            self.logger.info('コーナー通過順位テーブルが存在しません')
            return

        # テーブル一覧を取得
        tables = soup.find_all('table', class_ = 'tbl-data-05')

        # ラップタイムテーブルがなければ一番上、あれば二番目から取得
        if '<h3 class="hdg-l3-01"><span>タイム</span></h3>' in str(soup):
            corner_rank_table = tables[1]
        else:
            corner_rank_table = tables[0]

        # 一行ずつチェック
        for tr in corner_rank_table.find_all('tr'):
            if tr.find('th').text == '1コーナー':
                self.corner1_rank = mold.rm_nl(tr.find('td').text).replace(',', '|')

            if tr.find('th').text == '2コーナー':
                self.corner2_rank = mold.rm_nl(tr.find('td').text).replace(',', '|')

            if tr.find('th').text == '3コーナー':
                self.corner3_rank = mold.rm_nl(tr.find('td').text).replace(',', '|')

            if tr.find('th').text == '4コーナー':
                self.corner4_rank = mold.rm_nl(tr.find('td').text).replace(',', '|')

if __name__ == '__main__':
    result = Result('20230105', '106', '11')
    result.main()