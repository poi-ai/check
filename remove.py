import csv
import pandas as pd

def get_remove_race_id():
    # id.txtを開く
    with open('id.txt') as f:
        # 一行ずつ文字列を抜き出す
        lines = f.readlines()

    # スペースを除去した文字列を格納するリスト
    id_list = []

    # 一行ずつ処理する
    for line in lines:
        # スペースを除去してリストに挿入
        id_list.append(str(line.strip()))

    # 重複するものを除去して返す
    return list(set(id_list))

def remove_race_id(csv_name, id_list = get_remove_race_id()):
    # 出力用のデータを格納するリスト
    output_data = []

    # レースIDの格納してある行番号
    race_id_index = 0

    # csvを読み込む
    with open(f'{csv_name}.csv', 'r', encoding='utf-8') as f:
        reader = csv.reader(f)

        # 一行ずつ読み込む
        for index, row in enumerate(reader):

            # カラム列取得
            if index == 0:
                for column_index, column_name in enumerate(row):
                    # カラム名がrace_idなら変数に保管
                    if 'race_id' == column_name:
                        race_id_index = column_index
                output_data.append(row)
            else:
                # race_idを取得
                race_id = row[race_id_index]
                # race_idがid_listに存在するか判定
                if not str(race_id) in id_list:
                    output_data.append(row)

    df = pd.DataFrame(output_data[1:], columns=output_data[0])

    # CSV出力
    df.to_csv(f'{csv_name}2.csv', index=False, line_terminator='\n')

def remove_duplication_horse_id(assosiation):

    # 出力用のデータを格納するリスト
    output_data = []

    # csvを読み込む
    with open(f'{assosiation}_horse_char_info.csv', 'r', encoding='utf-8') as f:
        reader = csv.reader(f)

        # リスト格納
        csv_data = [row for row in reader]

    # リストをソート
    csv_data.sort()

    # 重複をはじく
    for index in range(len(csv_data)):
        if len(csv_data) - 1 != index:
            if csv_data[index][0] != csv_data[index + 1][0]:
                output_data.append(csv_data[index])

    df = pd.DataFrame(output_data[1:], columns=output_data[0])

    # CSV出力
    df.to_csv(f'{assosiation}_horse_char_info2.csv', index=False, line_terminator='\n')

assosiation = 'jra'
'''
remove_race_id(f'{assosiation}_horse_char_info')
remove_race_id(f'{assosiation}_horse_race_info')
remove_race_id(f'{assosiation}_horse_result')
remove_race_id(f'{assosiation}_race_info')
remove_race_id(f'{assosiation}_race_progress_info')
'''

remove_duplication_horse_id(assosiation)