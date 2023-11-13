# kubernetes-experiment-apiserver

**A simple API served via fastapi.**

Learning about kubernetes core concepts with a simple, microservice-based application. It's very messy and a lot of stuff is hardcoded, but that's okay because it's just for learning.

The [learn-k8s-webapp](github.com/kotae4/learn-k8s-webapp) microservice, its own deployment in the k8s cluster, is a flask app that serves the frontend and talks to the API.<br>
The **learn-k8s-apiserver** microservice, a separate deployment in the cluster, is a fastapi app that handles requests from the webapp backend and talks to the database.<br>
The database is external (exists outside the cluster). This example will use a local mariadb DB, but could be adapted to use AWS RDS or some other cloud provider's RDBMS.<br>

## Building

`docker build -t learn-k8s-apiserver:latest .`

## Running

`docker run --name apiserver -p 27036:27036 learn-k8s-apiserver`

It expects a database (mariadb, but mysql is fine too) to be hosted @ `db.testing.private:3306` with username `root` and password `toor`. Configured in `database.py`.

The [learn-k8s-webapp](github.com/kotae4/learn-k8s-webapp) microservice expects this API to be served at `http://api.testing.private:27036`.

Command for running manually (run from one directory up):
`uvicorn apiserver.main:app --host 0.0.0.0 --port 27036 --log-config=apiserver/log_conf.yaml --reload --reload-dir apiserver`.