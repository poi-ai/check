import log
import mold
import re
import traceback
from bs4 import BeautifulSoup
from base import Base

class Calendar(Base):
    ''''''
    def __init__(self, oldest_date, latest_date):
        super().__init__()
        self.oldest_date = oldest_date
        self.latest_date = latest_date

    def main(self):
        '''主処理'''
        pass

        # TODO 日付計算処理

        # TODO 月ごとにループ for  
        '''
        # HTML取得
        try:
            soup = gethtml.soup(f'TODO')
        except Exception as e:
            self.error_output('JBISレーシングカレンダー取得処理でエラー', e, traceback.format_exc())
            return
        '''

        # TODO 後で消す
        soup = self.get_soup('calendar201001')

        # レーシングカレンダーテーブル取得
        try:
            hold_list = self.get_hold(soup)
        except Exception as e:
            self.error_output('レーシングカレンダー取得処理でエラー', e, traceback.format_exc())
            return

        # 開催情報切り出し
        try:
            extaction_hold_list = self.extraction_hold(hold_list)
        except Exception as e:
            self.error_output('開催情報切り出し処理でエラー', e, traceback.format_exc())
            return

    def get_hold(self, soup):
        '''レーシングカレンダーテーブルを取得する

        Args:
            soup(bs4.BeautifulSoup) : 対象ページのHTML

        Returns:
            list[[開催日, 競馬場ID],[開催日, 競馬場ID]...]
        '''

        # レーシングカレンダーテーブルの取得
        calendar_table = soup.find_all('table', class_ = 'tbl-calendar-01')

        # 取得失敗時のログ出力
        if len(calendar_table) == 0:
            self.logger.error('レーシングカレンダーテーブルが見つかりません')
            return
        elif len(calendar_table) > 1:
            self.logger.warning('レーシングカレンダーテーブルが複数見つかりました。一番上のテーブルを取得対象にします')

        table = calendar_table[0]

        # 開催ページのリンクを取得
        link_match = re.findall(r'<a href="/race/calendar/(\d+)/(\d+)/">', str(table))
        if link_match == None:
            self.logger.warning('レーシングカレンダーテーブル内に開催リンクが見つかりません')
            return None

        # タプルをリストにして返す
        return [list(item) for item in link_match]

    def extraction_hold(self, hold_list):
        '''指定した期間内に合致する開催情報を返す'''
        return [hold for hold in hold_list if self.oldest_date <= hold[0] <= self.latest_date]

if __name__ == '__main__':
    c = Calendar('20100117','20100125')
    c.main()
