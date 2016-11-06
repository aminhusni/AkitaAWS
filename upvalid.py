#!/usr/bin/python

import os
import string
import subprocess

def traverse():
	output = subprocess.check_output(['find' , './testsubject', '-type', 'd', '-links', '2'])


def searchAndDestroy():
	output = subprocess.check_output(['find', './testsubject', '-name', '*', '-size', '0'])
	print("0kb Files:")
	print output
	#subprocess.call(['find', './testsubject', '-name', '*', '-size', '0', '-delete'])
	output = subprocess.check_output(['find', './testsubject', '-name', '*[^.jpg]'])
	print("Non jpeg Files")
	print output
