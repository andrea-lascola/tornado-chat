A Simple python-tornado Chat using WebSocket - Mongodb - Redis(ToRedis)

The purpose of the project is to test these functionalities:
### Tornado

    - WebSocket
    - AsyncDb connection(In progress)
    - UiWidgets (Todo)
    - Authentication (In progress)
### Redis

    - publish-subscribe api (every new connection subscribe to channel waiting for messages)
### MongoDb

    - Storage(connection/disconnection - messages)
    - Server side aggregations
    - Replica Set (Todo)
    - Sharded (Todo)
### Plotly

    - Basic Charting (In progress)
   
The app is still under development, a lot of work have to be done before it can be considered an alpha version


# Installation

    docker-compose up
    
or just:

    pip install -r requirements.txt
    python src/app.py
    (you need a redis available at localhost:6379 and a mongodb available at localhost:27017)        


# Pages:

    chat : http://localhost:8887/?user=andrew&channel=all (replace user and channel as you want)

    dashboard : http://localhost:8887/dashboard (protected by a login page just to test the auth with tornado)


# Todo
    
App

    [ ] Better autentication
    [ ] pages navigation
    [ ] use tornado widget UI : (http://www.tornadoweb.org/en/stable/guide/templates.html) 
    

Charts

    [V] [Bar] Messages per day
    [ ] [List] last x messages
    [ ] [List] last x accesses
    [ ] Widget colors
    [ ] [Number] medium chat duration (per user) (connect date - disconnect date)
