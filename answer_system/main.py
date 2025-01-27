import mysql.connector
import random
from time import sleep
from mysql.connector import errorcode

def setting():
    try: 
        cnx = mysql.connector.connect(
            user='pc',                         # 資料庫用戶名稱
            password='',  # 資料庫密碼
            host='',                   # 公網 IP
            database='questions_warehouse',        # 要連接的資料庫名稱（請改為你的資料庫名稱）
            port=3306                              # MySQL 默認埠號
        )
        cursor = cnx.cursor()
    except mysql.connector.Error as err:
        print(err)               
    return cursor, cnx 

def fetch( cursor, cnx, which_table, which_item, criteria): 
    #items:(id, questions, optionA, optionB, optionC, optionD, answer, explaintion, date, title, url)
    if criteria:
        query = (f"SELECT {which_item} FROM {which_table} WHERE {criteria}")
    else:
        query = (f"SELECT {which_item} FROM {which_table}")
    cursor.execute(query)
    box = []
    for goals in cursor:
        box.append(goals)
    return box

def show_tables(cursor):
    cursor.execute("SHOW TABLES")
    existed_tables = []
    for table in cursor:
        table = str(table[0])
        existed_tables.append(table)
    return existed_tables


cursor, cnx = setting()
while True:
    print('\n') 
    choice = input("Choose one type:" + '\n' + "(1)基隆市  (2)新北市  (3)臺北市  (4)桃園市  (5)新竹  (6)苗栗縣  (7)臺中市  (8)彰化縣  (9)南投縣  (10)雲林縣  (11)嘉義縣  (12)臺南市  (13)高雄市  (14)屏東縣  (15)臺東縣  (16)花蓮縣  (17)宜蘭縣  (18)連江縣  (19)金門縣  (20)澎湖縣  (21)國際")
    print('\n') 
    which_table = ['Keelung', 'New_Taipei', 'Taipei', 'Taoyuan', 'Hsinchu', 'Miaoli', 'Taichung',
                    'Changhua', 'Nantou', 'Yunlin', 'Chiayi', 'Tainan', 'Kaohsiung', 'Pingtung',
                    'Taitung', 'Hualien', 'Yilan', 'Lienchiang', 'Kinmen', 'Penghu', 'international'][int(choice)-1]
    if which_table not in show_tables(cursor):
        print(f"There is no question about '{which_table}' currently, choose other.")
        continue
    
    existed_id = fetch(cursor, cnx, which_table, 'id', None)
    number = random.choice(existed_id)
    criteria = f"id = {number[0]}"
    result = fetch(cursor, cnx, which_table, '*', criteria)
    # database.fetch = [(id, questions, optionA, optionB, optionC, optionD, answer, explaintion, date, title, url)]
    options = list(result[0][2:6]) 
    random_options = {}
    for i in range(0,4):
        orin_option = options.pop( random.randint(0, len(options)-1) )
        random_options[i] = orin_option.split(")")
    orin_answer = result[0][6].split("：")[1].strip().split(")")[0]
    for key, value in random_options.items():
        if orin_answer in value:
            answer = ["A", "B", "C", "D"][key]
    question_2 = (1000, result[0][1], random_options[0][1], random_options[1][1], random_options[2][1],
                  random_options[3][1], answer, result[0][7], result[0][8], result[0][9], result[0][10])
    
    print(result[0][1]) 
    print(f"A: {random_options[0][1]}")
    print(f"B: {random_options[1][1]}")
    print(f"C: {random_options[2][1]}")
    print(f"D: {random_options[3][1]}")
    reply = input("your answer is ? ")

    if reply == answer:
        print("\n恭喜你答對了！")
        print(f"正確答案是 {answer}" )
        print(f"\n答案解釋:\n{result[0][7]}" )
    
    elif reply == "BREAK":
        break
    
    else:
        print("\n很可惜答錯了...")
        print(f"正確答案是 {answer}" )
        print(f"\n答案解釋:\n{result[0][7]}" )
    
    sleep(6)
    