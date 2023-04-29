import sqlite3
import datetime

class WebSql():
    conn = sqlite3.connect('web.pd',check_same_thread=False)

    creat_table_video = '''
        CREATE TABLE IF NOT EXISTS VIDEO
            (ID INT,
            VIDEO INT
            );
        '''

    creat_table_record='''
        CREATE TABLE IF NOT EXISTS RECORD
            (ID INT,
            DATE DATE,
            RECORD TEXT
            );
        '''
    #更新video状态
    insert_table_video_values = 'INSERT INTO VIDEO VALUES ({},{});'
    #插入操作记录
    insert_table_record_values = 'INSERT INTO RECORD VALUES ({},"{}","{}");'
    select_table_values = 'SELECT * FROM {};'
    update_table_values = 'UPDATE VIDEO SET VIDEO = {1} WHERE ID = {0};'

    c = conn.cursor()

    def __init__(self,count = 6):
        self.conn.execute(self.creat_table_video)
        self.conn.execute(self.creat_table_record)
        self.save_web()
        cursor = self.c.execute(self.select_table_values.format('VIDEO'))
        result = cursor.fetchall()
        if len(result) == 0:
            for i in range(count):
                self.c.execute(self.insert_table_video_values.format(i+1,0))

    def update_video(self,id,value):
        self.c.execute(self.update_table_values.format(id,value))
        self.c.execute(self.select_table_values.format('VIDEO'))

    # 插入记录 传入id，记录
    def insert_record(self,id, record):
        dt = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.c.execute(self.insert_table_record_values.format(id,dt,record))

    #选择，查询
    def select(self,table):
        cursor = self.c.execute(self.select_table_values.format(table))
        rows = []
        for row in cursor:
            rows.append(row)
        return rows

    def save_web(self):
        self.conn.commit()

    def close(self):
        self.conn.close()

# ws = WebSql()
# ws.insert_record(1,'test')
# t = ws.select('RECORD')
# print(t)
# ws.save_web()