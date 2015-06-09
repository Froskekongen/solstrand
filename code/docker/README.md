Instructions

1. Get docker images using getImages.sh
 - getImages.sh needs to be run with sudo

2. Start elasticsearch and kibana
 - docker-compose up -d

3. Get some log data
 - run getLocalSyslog.sh and getVPdata.sh

4. Build docker logstash image
 - sudo docker build -t froskekongen/logstasher .

5. Run logstash image
 - sudo docker run -it --link docker_elasticsearch_1:elasticsearch --rm froskekongen/logstasher

Courtesy of https://github.com/babadofar/bbuzz_code for the vinmonopolet templates
