
1. Get mongodb docker image
 - sudo docker pull mongo

2. Get enron data
 - getSomeDatasets.sh

3. Start mongo docker
 - sudo docker run --name mongo-enron --link docker_elasticsearch_1:elasticsearch -v $PWD:/enrondata -p 41000:27017 -d mongo

4. Attach process to docker
 - sudo docker exec -it mongo-enron bash
 - restore enron data
  - mongorestore --port 27017 /enrondata/dump/
