import sqlite3
import time


def dict_factory(cursor, row):
    d = {}
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]

    return d


def main():
    conn = sqlite3.connect('database.db')
    with conn:
        conn.execute('''
        CREATE TABLE file (
        company_name TEXT,
        account_number TEXT,
        electricity_type TEXT,
        volumn TEXT,
        voltage TEXT,
        time float,
        id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT DEFAULT 0);
        ''')


def main1():
    conn = sqlite3.connect('database.db')
    with conn:
        sql = 'insert into file (account_number, electricity_type, voltage, time) values(?,?,?,?)'
        datas = [('10236558', 'bossiness', '12V', time.time())]
        conn.executemany(sql, datas)


if __name__ == '__main__':
    a = 2222222
    if a == 0:
        main()
    if a == 1:
        main1()
    else:
        conn = sqlite3.connect('database.db')
        with conn:
            print("_________________")
            conn.row_factory = dict_factory
            sql = 'select * from file'
            for i in conn.execute(sql).fetchall():
                print(i)

