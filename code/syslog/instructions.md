# copy some syslog and convert it to utf-8
cp /var/log/syslog $PWD
iconv -f=ISO-8859-1 -t=UTF-8 syslog > syslog2.txt
rm syslog
mv syslog2.txt syslog.txt
rm syslog2.txt
#then run
# sudo docker run -it -v $PWD:$PWD --link elasticsearch:elasticsearch --rm logstash bash
# make sure the elasticsearch index is up and running
# inside container run
# logstash -f sl.conf
