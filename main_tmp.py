import traceback
from base import Base

class XXX(Base):
    ''''''
    def __init__(self):
        super().__init__()

    def main(self):
        '''�����'''

        # HTML�ե����뤫��ǡ�������
        soup = self.get_soup('HTML̾')

        # try-exceptʸ
        try:
            hogehoge_list = self.hoge()
        except Exception as e:
            self.error_output('hogehoge�ǥ��顼', e, traceback.format_exc())
            return

if __name__ == '__main__':
    xxx = XXX()
    xxx.main()
