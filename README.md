Python AWS Backup
================

Simple Python backup script for backing up files on Amazon S3

Testing
------------
* Make sure you have the config.yaml filled out before you run the test.
* Script comes with test dir and files.


```
 pdfs/dummy.pdf
```
```
dirs = [
        './pdfs'
        ]
```        
Requirements
------------

This script requires boto. To install boto simply run -

```
pip install boto
```

Configuration
-------------

The script requires the following configuration parameters

**AWS**

Open config.yaml and enter the information below

* Access Key - _aws_access_key_
* Secret Key - _aws_secret_key_
* Bucket - _aws_bucket_

**Directories**

You can backup as many directories as you like. Simply define it as a list and include the full path, e.g.

```
dirs = [
        '/path/to/dir',
        '/path/to/dir',
        ]
```

Crontab
-------

Sample cron to run backup every day at 23.00.

```
0 23 * * * python ~/scripts/backup.py
```
