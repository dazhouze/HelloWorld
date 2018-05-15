'''
pip can not install myseq-connector beacause of unbuntu 16.04
try source code and sudo install
'''
import mysql.connector
conn = mysql.connector.connect(user='root', password='password', database='test')
cousor = conn.cursor()

#create list
cursor.execute('create table user (id varchar(20) primary key, name varchar(20))')
cursor.execute('insert into user (id, name) value (%s, %s)', ['1', 'Michael'])
cursor.execute('insert into user (id, name) value (%s, %s)', ['3', 'Zhou Ze'])
print(cursor.rowcount)
conn.commit()
conn.close()
#inquire
cursor = conn.cursor()
cursor.execute('select * from user where id = %s', ('1',))
values = cursor.fetchall()
print(value)
cursor.execute('select * from user where id = %s', ('2',))
values = cursor.fetchall()
print(value)
cursor.execute('select * from user where id = %s', ('3',))
values = cursor.fetchall()
print(value)
cursor.close()
conn.close()
