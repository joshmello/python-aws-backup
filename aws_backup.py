#!/usr/bin/python

import datetime
import os
import string
import tarfile
import boto3

from datetime import timedelta
s3 = boto3.resource('s3')
bucket_name = 'mybucket'

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

# Send files to S3
for f in dirs:

    file = f.split('/')[::-1][0] + '-' + str(today) + '.files.tar.gz'

    print '[S3] Uploading file archive ' + file + '...'
    s3.meta.client.upload_file('/tmp/' + file, bucket_name, file)

    os.remove('/tmp/' + file);