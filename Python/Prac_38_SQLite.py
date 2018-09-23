import sqlite3
'''
conn = sqlite3.connect('test.db')
cursor = conn.cursor()
cursor.execute('create table usr (id varchar(20) primary key, name varchar(20))')
cursor.execute('insert into usr (id, name) values (\'1\', \'Michael\')')
print(cursor.rowcount)
cursor.close()
conn.commit()
conn.close()
'''
conn = sqlite3.connect('test.db')
cursor = conn.cursor()
cursor.execute('select * from usr where id=?', ('1',))
values = cursor.fetchall()
print(values)
