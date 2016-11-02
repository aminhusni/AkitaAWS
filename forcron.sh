#!/bin/sh
echo "Job Initiated" >> enc.log
python worker.py >> enc.log
python extencoder.py >> enc.log
