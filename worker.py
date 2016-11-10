#!/usr/bin/python

import mysql.connector
import time
import datetime
from datetime import datetime
from datetime import timedelta
import subprocess
import os
import glob

db = mysql.connector.connect(host="localhost",user="akitausermanager",password="akitausers",database="akitaLaravel")
db2 = mysql.connector.connect(host="localhost",user="akitausermanager",password="akitausers",database="akitaLaravel")
cursor = db.cursor()
cursor2 = db2.cursor()

yesterday = datetime.now()
#Change time delta to  0 to encode today's picture(override)
yesterday = yesterday - timedelta(days=1)

today = yesterday.strftime("%Y-%m-%d")
#Process date is the real date of today
processdate = time.strftime("%Y-%m-%d")

#debug----------------------------
print(datetime.now())
print("Muxing has started")

#This gets the id_camera, id_user and ftp_id and ftpuser.userid for all unprocessed camera.
sql1 = "SELECT c.id, u.id, u.ftpuser_id, ftpuser.userid FROM cameras AS c INNER JOIN users AS u ON c.user_id=u.id INNER JOIN ftpuser ON ftpuser.id=u.ftpuser_id WHERE c.processing_date < '"+processdate+"'"
cursor.execute(sql1)
row = cursor.fetchone()
while row is not None:
    
    todaypattern = yesterday.strftime("%Y%m%d")
    #Set original date for reference point which is today.
    original_date = datetime.strptime(today, '%Y-%m-%d')
    new_date = datetime.strptime(today, '%Y-%m-%d')
    #Get all the relevant information.
    cameraid = row[0]
    userid = row[1]
    ftpid = row[2]
    ftpuser = row[3]
    #Mark that the camera has been worked on.
    sql2 = "UPDATE `cameras` SET `processing_date` = '"+processdate+"' WHERE `cameras`.`id` = "+str(cameraid)
    #DRY RUN
    cursor2.execute(sql2)
    db2.commit()

    #Navigates into camera directory.
    os.environ['curcamera'] = "/mnt/buffer/users/"+ftpuser+"/"+str(cameraid)
    os.chdir(os.environ['curcamera'])
    #Process up to 7 days for a single camera.
    while True:
        #Process datetime into computer format.
        videodatecomp = datetime.strptime(todaypattern, "%Y%m%d").date()
        videodatestr = videodatecomp.strftime("%Y-%m-%d")
        #Setup some patterns.
        filepattern = "*"+todaypattern+"*.jpg"
        countpattern = "ls "+filepattern+" | wc -l"
        outputpattern = "/mnt/buffer/output/"+todaypattern+str(ftpuser)+str(cameraid)+".avi"
        outputfilename = todaypattern+str(ftpuser)+str(cameraid)
        #print(countpattern)
        #Starts the muxing process.
        fileflag = glob.glob(filepattern)
	filecount = len(glob.glob(filepattern))
	if filecount != 0:
	    print(filecount)
        if fileflag:
            subprocess.call(['ffmpeg','-loglevel' ,'warning','-y','-framerate', '30', '-pattern_type', 'glob', '-i', filepattern, '-c:v', 'copy', outputpattern])
        #See if file had been successfully created.
            if os.path.isfile(outputpattern) == True:   
                sql2 = "INSERT INTO `videos` (`id`, `videodate`, `camera_id`, `filepath`, `filename`) VALUES (NULL, '"+videodatestr+"', '"+str(cameraid)+"', '"+outputpattern+"', '"+outputfilename+"')"
                #DRY RUN
		cursor2.execute(sql2)
                db2.commit()
		print("Muxed:"+filepattern)
                subprocess.call(['find', '-name', filepattern, '-delete'])
                #delete all pictures by current pattern. 
        #Reduce the date until target of 7 days of backlog.
        #This needs to be fixed to a proper date processing function.
        delta = original_date - new_date
        if delta.days < 7:
            new_date = new_date - timedelta(days=1)
            todaypattern = new_date.strftime("%Y%m%d")
        else: 
            break

    row = cursor.fetchone()

cursor.close()
cursor2.close()
db.close()
db2.close()


