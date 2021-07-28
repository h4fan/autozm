#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sqlite3

db_str = 'ipport.db'

conn = sqlite3.connect(db_str)

c = conn.cursor()

# Create table
c.execute('''CREATE TABLE records
             (cidrstr text, ip text, port text, service text,hostname text,app text,title text)''')

conn.commit()

conn.close()
