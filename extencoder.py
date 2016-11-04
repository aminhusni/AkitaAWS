#!/usr/bin/python

import mysql.connector
import subprocess
import os, sys
import boto3

db = mysql.connector.connect(host="localhost",user="akitausermanager",password="akitausers",database="akitaLaravel")
db2 = mysql.connector.connect(host="localhost",user="akitausermanager",password="akitausers",database="akitaLaravel")
cursor = db.cursor()
cursor2 = db2.cursor()
s3 = boto3.resource('s3')
transcoder = boto3.client('elastictranscoder')

muxedpath = "/mnt/buffer/output/"
muxfiles = os.listdir(muxedpath)
#Upload everything into S3 first. 
for file in muxfiles:
    filepath = muxedpath+file
    s3.meta.client.upload_file(filepath, 'akitainput', file)
    #Debug purposes

#Start creating encoding jobs
sql1 = "SELECT videos.filename, videos.id FROM `videos` WHERE `encoded` = 0"
cursor.execute(sql1)
row = cursor.fetchone()

while row is not None:
    filename = row[0]
    videoid = row[1]
    #DRY RUN
    sql2 = "UPDATE `videos` SET `encoded` = 1 WHERE `videos`.`id` ="+str(videoid)
    cursor2.execute(sql2)
    db2.commit()
    response = transcoder.create_job(
        PipelineId='1477483372572-td13z7',
Input={'Key': filename+".avi", 'FrameRate': 'auto', 'Resolution': 'auto', 'AspectRatio': 'auto', 'Interlaced': 'auto', 'Container': 'auto'},
Output={'Key': filename+".webm",'PresetId': '1478113500926-8cdl3u'}
)
    row = cursor.fetchone()
    print("Uploaded:"+filename)
cursor.close()
cursor2.close()
db.close()
db2.close()
print("External encoder ran successfully")
print("\n")
