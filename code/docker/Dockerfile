FROM logstash:latest

ADD syslog/syslog.txt /logdata/syslog/syslog.txt
ADD vpdata/iconproducts.csv /logdata/vpdata/iconproducts.txt
ADD vp.conf /logdata/vp.conf
ADD sl.conf /logdata/sl.conf

RUN logstash agent -f /logdata/vp.conf < /logdata/vpdata/iconproducts.txt
RUN logstash agent -f /logdata/sl.conf < /logdata/syslog/syslog.txt

CMD ["bash"]
