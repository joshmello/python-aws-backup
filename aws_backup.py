#!/usr/bin/python

import datetime
import os
import string
import tarfile
import yaml

from boto.s3.connection import S3Connection
from boto.s3.key import Key

from datetime import timedelta


with open("config.yaml", 'r') as ymlfile:
    cfg = yaml.load(ymlfile)

    aws_access_key = cfg['aws']['aws_access_key']
    aws_secret_key = cfg['aws']['aws_secret_key']
    aws_bucket = cfg['aws']['aws_bucket']


dirs = [
        './pdfs'
]

# Script Configuration
today = datetime.date.today()
previous = today - timedelta(days = 7)

# File Backups
for d in dirs:

    file = d.split('/')[::-1][0]

    print '[FILE] Creating archive for ' + file

    tar = tarfile.open(os.path.join('/tmp/', file + '-' + str(today) + '.files.tar.gz'), 'w:gz')
    tar.add(d)
    tar.close()

# Establish S3 Connection
s3 = S3Connection(aws_access_key, aws_secret_key)
b = s3.get_bucket(aws_bucket)

# Send files to S3
for f in dirs:

    file = f.split('/')[::-1][0] + '-' + str(today) + '.files.tar.gz'

    print '[S3] Uploading file archive ' + file + '...'

    k = Key(b)
    k.key = file
    k.set_contents_from_filename('/tmp/' + file)
    k.set_acl("public-read")

    os.remove('/tmp/' + file);

    print '[S3] Clearing previous file archive ' + file + '...'

    # Conserve monthly backups (Previous Month)
    if previous != str(datetime.datetime.today().year) + '-' + str(datetime.datetime.today().month) + '-1':
        # Clean up files on S3
        k = Key(b)
        k.key = f.split('/')[::-1][0] + '-' + str(previous) + '.files.tar.gz'
        b.delete_key(k)