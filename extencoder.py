#!/usr/bin/python

import mysql.connector
import subprocess
import os

db = mysql.connector.connect(host="localhost",user="akitausermanager",password="akitausers",database="akitaLaravel")
db2 = mysql.connector.connect(host="localhost",user="akitausermanager",password="akitausers",database="akitaLaravel")
cursor = db.cursor()
cursor2 = db2.cursor()

sql1 = "SELECT videos.filepath, videos.filename, videos.id FROM `videos` WHERE `encoded` = 0"
cursor.execute(sql1)
row = cursor.fetchone()

os.environ['curen'] = "/home/Akita/encoded/"
os.chdir(os.environ['curen'])
while row is not None:
    filepath = row[0]
    filename = row[1]
    videoid = row[2]
    outfilename = filename+".mp4"
    sql2 = "UPDATE `videos` SET `encoded` = 1 WHERE `videos`.`id` ="+str(videoid)
    cursor2.execute(sql2)
    db2.commit()
    subprocess.call(['ffmpeg', '-y', '-i', filepath, '-c:v', 'libx264', '-preset', 'medium', '-crf', '22', '-c:a', 'copy', outfilename])
    subprocess.call(['rm', '-f', filepath])
    row = cursor.fetchone()

cursor.close()
cursor2.close()
db.close()
db2.close()