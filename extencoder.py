#!/usr/bin/python

import mysql.connector
import subprocess
import os, sys

db = mysql.connector.connect(host="localhost",user="akitausermanager",password="akitausers",database="akitaLaravel")
db2 = mysql.connector.connect(host="localhost",user="akitausermanager",password="akitausers",database="akitaLaravel")
cursor = db.cursor()
cursor2 = db2.cursor()
s3 = boto3.resource('s3')
transcoder = boto3.client('elastictranscoder')

muxedpath = "/home/Akita/output/"
muxfiles = os.listdir(muxedpath)
#Upload everything into S3 first. 
for file in muxfiles:
    filepath = muxedpath+file
    s3.meta.client.upload_file(filepath, 'akitainput', file)
    #Debug purposes
    print("Uploaded:"+file)

#Start creating encoding jobs
sql1 = "SELECT videos.filename, videos.id FROM `videos` WHERE `encoded` = 0"
cursor.execute(sql1)
row = cursor.fetchone()

while row is not None:
    filename = row[1]
    videoid = row[2]
    sql2 = "UPDATE `videos` SET `encoded` = 1 WHERE `videos`.`id` ="+str(videoid)
    cursor2.execute(sql2)
    db2.commit()
    response = transcoder.create_job(
        PipelineId='1477483372572-td13z7',
Input={'Key': filename+".avi", 'FrameRate': 'auto', 'Resolution': 'auto', 'AspectRatio': 'auto', 'Interlaced': 'auto', 'Container': 'auto'},
Output={'Key': filename+".webm",'PresetId': '1351620000001-100250'}
)
    row = cursor.fetchone()

cursor.close()
cursor2.close()
db.close()
db2.close()