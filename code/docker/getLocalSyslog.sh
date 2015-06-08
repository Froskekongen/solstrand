mkdir syslog
cd syslog
rm syslog*
cp /var/log/syslog* ./
for i in *.gz; do gunzip $i; done
find . -type f -name 'syslog*' -exec cat {} + >> 1syslog.txt
rm syslog*
iconv -f=ISO-8859-1 -t=UTF-8 1syslog.txt > syslog.txt
rm 1syslog.txt
