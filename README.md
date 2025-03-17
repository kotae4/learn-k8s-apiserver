# kubernetes-experiment-apiserver

**NOTE:** This hogs all the CPU and crashes every component in kubernetes cluster and brings the node it's running on down. [Remaking from scratch in .NET](https://github.com/kotae4/learn-k8s-apiserver-net). Easier to remake than to debug.

**A simple API served via fastapi.**

Learning about kubernetes core concepts with a simple, microservice-based application. It's very messy and a lot of stuff is hardcoded, but that's okay because it's just for learning.

The [learn-k8s-webapp](https://github.com/kotae4/learn-k8s-webapp) microservice, its own deployment in the k8s cluster, is a flask app that serves the frontend and talks to the API.<br>
The **learn-k8s-apiserver** microservice, a separate deployment in the cluster, is a fastapi app that handles requests from the webapp backend and talks to the database.<br>
The database is external (exists outside the cluster). This example will use a local mariadb DB, but could be adapted to use AWS RDS or some other cloud provider's RDBMS.<br>

## Containerization

Networking:
```bash
# to begin:
docker network create learn-k8s-network
# once done:
docker network remove learn-k8s-network
```

Building:
```bash
docker build -t learn-k8s-apiserver:latest .
```

Running:
```bash
docker run --rm -d --name apiserver --network learn-k8s-network -p 27525:27525 -e DB_HOST=mysqldb -e DB_PORT=3306 learn-k8s-apiserver
```

Cleaning up:
```bash
docker stop apiserver
docker rm apiserver
```

## Notes on running

It expects a database (mariadb, but mysql is fine too) to be hosted @ `db.local.testapp.private:3306` with username `badmin` and password `vagrant`. Configured in `config.py`, via .env file, or via environment variables.

For local development, you can spin up a mysql database like this:
```bash
docker pull mysql:8.4.4
```

```bash
docker run -d --network learn-k8s-network -p 23306:3306 --name mysqldb --hostname mysqldb -e MYSQL_DATABASE=appdb -e MYSQL_USER=badmin -e MYSQL_PASSWORD=vagrant -e MYSQL_ROOT_PASSWORD=vagrant mysql:8.4.4
```

The [learn-k8s-webapp](https://github.com/kotae4/learn-k8s-webapp) microservice expects this API to be served at `http://api.testing.private:27525`.

Command for running manually:
`uvicorn learn-k8s-apiserver.main:app --host 0.0.0.0 --port 27525 --log-config=learn-k8s-apiserver/log_conf.yaml --reload --reload-dir learn-k8s-apiserver`.