# -*- coding: utf-8 -*-
"""
Created on Wed Jun  8 14:19:00 2022

@author: HP
"""

import sqlite3

conn = sqlite3.connect('history.db')
c = conn.cursor()
c.execute('''CREATE TABLE CHAT
       (NUMBER  INT  PRIMARY KEY   NOT NULL,
       TIME  TEXT  NOT NULL,
       MY_MESSAGE    TEXT,
       AI_MESSAGE    TEXT
       );''')
print("数据表创建成功")
conn.commit()
conn.close()
