FROM logstash:latest

ADD syslog/syslog.txt /logdata/syslog/syslog.txt
ADD vpdata/iconproducts.csv /logdata/vpdata/iconproducts.txt
ADD vp.conf /logdata/vp.conf
ADD sl.conf /logdata/sl.conf
ADD ingestlogstashes.sh /logdata/ingestlogstashes.sh
ADD mappingVP.json /logdata/mappingVP.json

RUN chmod +x /logdata/ingestlogstashes.sh

WORKDIR /logdata


CMD ["/logdata/ingestlogstashes.sh"]
