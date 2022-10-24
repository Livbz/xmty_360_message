import sqlite3, time
class dbfun:
    @staticmethod
    def insert_into_db(companynames, accountnumbers, usertypes, voltages, volumns):
        datas = []
        for companyname, accountnumber, usertype, voltage, volumn in zip(companynames, accountnumbers, usertypes,
                                                                         voltages, volumns):
            datas.append((companyname, accountnumber, usertype, voltage, volumn, time.time()))
        conn = sqlite3.connect('database.db')
        with conn:
            sql = 'insert into file (company_name, account_number, electricity_type, voltage, volumn, time) ' \
                  'values(?,?,?,?,?,?)'
            conn.executemany(sql, datas)
