#enron dataset
#wget 'https://www.cs.cmu.edu/~./enron/enron_mail_20150507.tgz'
## http://mongodb-enron-email.s3-website-us-east-1.amazonaws.com/
# enron data in mongodb format
mkdir data
wget 'https://s3.amazonaws.com/mongodb-enron-email/enron_mongo.tar.bz2'
tar jxf enron_mongo.tar.bz2 -C data/
