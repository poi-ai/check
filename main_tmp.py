import traceback
from base import Base

class XXX(Base):
    ''''''
    def __init__(self):
        super().__init__()

    def main(self):
        '''主処理'''

        # HTMLファイルからデータ取得
        soup = self.get_soup('HTML名')

        # try-except文
        try:
            hogehoge_list = self.hoge()
        except Exception as e:
            self.error_output('hogehogeでエラー', e, traceback.format_exc())
            return

if __name__ == '__main__':
    xxx = XXX()
    xxx.main()
