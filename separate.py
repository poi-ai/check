import re

# nar.log.txtを開く
with open('nar.log.txt', 'r', encoding='utf-8') as f:
    # 1行ずつ処理する
    for line in f:
        # 正規表現で「(race_id:①)の②」に合致する文字列を検索する
        match = re.search(r'\(race_id:(\d+)\)の(.+)', line)
        # 合致する文字列が見つかった場合
        if match:
            # ①を取り出す
            race_id = match.group(1)
            # ②を取り出す
            text = match.group(2)
            # nar_clustering.csvに「①,②」という形で出力する
            with open('nar_clustering.csv', 'a') as g:
                g.write(f'{race_id},{text}\n')

# jra.log.txtを開く
with open('jra.log.txt', 'r', encoding='utf-8') as f:
    # 1行ずつ処理する
    for line in f:
        # 正規表現で「(race_id:①)の②」に合致する文字列を検索する
        match = re.search(r'\(race_id:(\d+)\)の(.+)', line)
        # 合致する文字列が見つかった場合
        if match:
            # ①を取り出す
            race_id = match.group(1)
            # ②を取り出す
            text = match.group(2)
            # jra_clustering.csvに「①,②」という形で出力する
            with open('jra_clustering.csv', 'a') as g:
                g.write(f'{race_id},{text}\n')