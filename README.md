# weather

Install Python version
```
pyenv isntall 3.9.14
```

Create Python virtualenv
```
pyenv virtualenv 3.9.14 weather
```

Activate Python virtualenv
```
pyenv activate weather
```

Add virtualenv to Jupyter notebook
```
pip install --user ipykernel
python -m ipykernel install --user --name=weather
```

Install `kcat` to easily talk with Kafka on Docker
```
brew install kcat
```


### Useful commands
List Kafka topics:
```
docker exec -it kafka-broker kafka-topics.sh --bootstrap-server localhost:9092 --list
```

Delete Kafka topic:
```
docker exec -it kafka-broker kafka-topics.sh --bootstrap-server localhost:9092 --delete --topic <TOPIC_NAME>
```


### Useful resources:

Setting up Kafka on Docker: \
https://hackernoon.com/setting-up-kafka-on-docker-for-local-development



