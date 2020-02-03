# hello-flask
Let's try flask, twitter api and graylog

# Requirements
- Docker
- docker-compose

# How to Run
- First, check docker-compose file, add you own twitter keys (lines 11~14);
- In docker-compose file, edit the graylog external uri (line 47) 
- ./run.sh
- Access graylog in your browser and install content_pack.json
- Import postman_collection.json in your postman

# API Routes

| Method   | URI                 | Name         | Description                                                          |
|----------|---------------------|--------------|----------------------------------------------------------------------|
| GET-HEAD | /tag/STRING         | GetByTag     | Get the last 100 tweets by tag                                       |
| GET-HEAD | /highfollower       | HighFollower | Get top 5 followed users from tweets given by a static array of tags |

# Architecture Design

![](https://raw.githubusercontent.com/leoddias/hello-flask/master/design.png)

# Graylog Dashboard

![](https://raw.githubusercontent.com/leoddias/hello-flask/master/dashboard.png)