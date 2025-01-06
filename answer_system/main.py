import mysql.connector
import random
from time import sleep
from mysql.connector import errorcode

def setting():
    try:
        cnx = mysql.connector.connect(user='root', password='999999',host='127.0.0.1',database='questions_warehouse')
    except mysql.connector.Error as err:
        if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
            print("Something is wrong with your user name or password")
        elif err.errno == errorcode.ER_BAD_DB_ERROR:
            print("Database does not exist")
        else:
            print(err)
    # else:
    #     print('successfully connected to mysql service.')
        
    cursor = cnx.cursor()
    return cursor, cnx

def fetch(cursor, cnx, which_table, which_item, criteria):
    #items:(id, questions, optionA, optionB, optionC, optionD, answer, explaintion, date)
    if criteria:
        query = (f"SELECT {which_item} FROM {which_table} WHERE {criteria}")
    else:
        query = (f"SELECT {which_item} FROM {which_table}")
    cursor.execute(query)
    box = []
    for goals in cursor:
        box.append(goals)
    # cursor.close()
    # cnx.close()
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
    choice = input("Choose one type:" + '\n' + "(1)基隆市  (2)新北市  (3)臺北市  (4)桃園市  (5)新竹  (6)苗栗縣  (7)臺中市  (8)彰化縣  (9)南投縣  (10)雲林縣  (11)嘉義縣  (12)臺南市  (13)高雄市  (14)屏東縣  (15)臺東縣  (16)花蓮縣  (17)宜蘭縣  (18)連江縣  (19)金門縣  (20)澎湖縣  (21)國際國際")
    print('\n') 
    which_table = ['keelung', 'new_taipei', 'taipei', 'taoyuan', 'hsinchu', 'miaoli', 'taichung',
             'changhua', 'nantou', 'yunlin', 'chiayi', 'tainan', 'kaohsiung', 'pingtung',
             'taitung', 'hualien', 'yilan', 'lienchiang', 'kinmen', 'penghu', 'international'][int(choice)-1]
    if which_table not in show_tables(cursor):
        print(f"There is no question about '{which_table}' currently, choose other.")
        continue
    
    existed_id = fetch(cursor, cnx, which_table, 'id', None)
    sequence = ['questions', 'optionA', 'optionB', 'optionC', 'optionD', 'answer', 'explaination']
    number = random.choice(existed_id)
    criteria = f"id = '{number[0]}'"
    result = fetch(cursor, cnx, which_table, '*', criteria)
    
    print(result[0][1])
    print(result[0][2])
    print(result[0][3])
    print(result[0][4])
    print(result[0][5])
    reply = input("your answer is ? ")
    
    for i in ('A', 'B', 'C', 'D'):
        if i in result[0][6]:
            correct_answer = i

    if reply == correct_answer:
        print('\n',"恭喜你答對了！")
        print(result[0][6])
        print(result[0][7])
    else:
        print('\n',"很可惜答錯了...")
        print(result[0][6])
        print(result[0][7])
        
    # print(result[0][7])
    
    sleep(6)
    