# Summary - Muhamad Affan

## CRUD Application
For the CRUD application, i'm choosing Python with Flask framework for the backend and postgresql as the database.

The data that will be used is an `employee` table with the following schema:
```
id          : UUID
name        : String
age         : Integer
email       : String
created_at  : Timestamp
updated_at  : Timestamp
```

### Documentation
#### Create
- URL     : `/employees/add`
- Description : Create a new employee entry
- Method  : `POST`
- Request Body :
  ```json
  {
    "name": String [Required],
    "age": Integer [Required],
    "email": String [Required]
  }
  ```
  Example:
  ```json
  {
    "name": "affan",
    "age": 25,
    "email": "foo+1@bar.com"
  }
  ```
- Response
  ```json
  {
    "employee": {
        "age": Integer,
        "created_at": Timestamp,
        "email": String,
        "id": UUID,
        "name": String,
        "updated_at": Timestamp
    },
    "message": String
  }
  ```
  Example:
  ```json
  {
    "employee": {
        "age": "25",
        "created_at": "2025-05-20 22:22:46.243212",
        "email": "foo+1@bar.com",
        "id": "14538b70-78ec-4d82-9cda-41deed583f60",
        "name": "affan",
        "updated_at": "2025-05-20 22:22:46.243212"
    },
    "message": "success"
  }
  ```

#### Read
- URL : `/employees/get`
- Description : Get all employee data
- Method : `GET`
- Response
  ```json
  {
    "employees": [
        {
          "age": Integer,
          "created_at": Timestamp,
          "email": String,
          "id": UUID,
          "name": String,
          "updated_at": Timestamp
        },
        {
          "age": Integer,
          "created_at": Timestamp,
          "email": String,
          "id": UUID,
          "name": String,
          "updated_at": Timestamp
        },
        .
        .
        .
    ],
    "message": String
  }
  ```

  Example :
  ```json
  {
    "employees": [
        {
            "age": "25",
            "created_at": "2025-05-15 01:41:49.399918",
            "email": "foo+2@bar.com",
            "id": "a7ed1626-046c-4e4e-b88b-e675a076a224",
            "name": "affan2",
            "updated_at": "2025-05-15 01:41:49.399918"
        },
        {
            "age": "25",
            "created_at": "2025-05-16 02:49:54.586036",
            "email": "foo+3@bar.com",
            "id": "5e796c6c-f96c-4a93-9582-b63a96fbb2d1",
            "name": "affan3",
            "updated_at": "2025-05-16 02:49:54.586036"
        }
    ]
    "message": "success"
  }
  ```

#### Update
- URL : `/employees/update/<email>`
- Description : Update employee data based on `<email>` that is given
- Method : `PATCH`
- Parameters:
    - `email` : String
- Request Body:
  ```json
  {
    "name": String [Optional],
    "age": Integer [Optional],
    "email": String [Optional]
  }
  ```
  > Note : despite all of it being optionals, at least one of the keys needs to be present in the body

  Example:
  URL : `/employees/update/foo@bar.com`
  ```json
  {
    "name": "affan-test"
  }
  ```

- Response
  ```json
  {
    "employee": {
        "age": Integer,
        "created_at": Timestamp,
        "email": String,
        "id": UUID,
        "name": String,
        "updated_at": Timestamp
    },
    "message": String
  }
  ```

  Example:
  ```json
  {
    "employee": {
        "age": "25",
        "created_at": "2025-05-15 01:41:35.721049",
        "email": "foo@bar.com",
        "id": "710972a0-a2b5-4c0e-8a24-8f120bc5957a",
        "name": "affan-test",
        "updated_at": "2025-05-20 22:29:27.659368"
    },
    "message": "success"
  }
  ```

#### Delete
- URL : `/employees/delete/<email>`
- Description : Delete an employee entry that has email based on `<email>` parameter.
- Method : `DELETE`
- Parameters :
    - `email` : String
- Response :
  Response Code `204`

### Deployment
For the deployment, i am using [digitalocean](https://www.digitalocean.com/) cloud provider. The app can be acces through this address : [http://170.64.206.172/](http://170.64.206.172/)

I am using the provider's VM product (droplet) with the following stack:
- App containerization using docker (will be explained further in section below)
- NGINX server as a reverse-proxy
- Postgresql database installed in the VM

## Containerization
Here's the Dockerfile to create an image for the apps with explanation for each line
```Docker
# Using existing python 3.9 as the base image
FROM python:3.9-slim-buster

# Installing dependency package for SQLAlchemy and psycopg2 as DB Driver
RUN apt-get update \
    && apt-get -y install libpq-dev gcc

# Exposing port that will be used
EXPOSE 5000

# Copying requirements file to the image
COPY requirements.txt .
# Installing the requirements
RUN python -m pip install -r requirements.txt

# Move to /app directory
WORKDIR /app
# Copying codebase to the /app directory
COPY . /app

# running the application
CMD ["gunicorn", "--bind", "0.0.0.0:5000", "app:app"]
```

The image will be pushed to container registry in [dockerhub](https://hub.docker.com/) with tag `appan/flask-app-2:latest`

### Pushing image to registry
Command : 
```shell
docker push appan/flask-app-2:latest
```

Result :

![](/assets/img/docker-push.png)

Result on dockerhub :

![](/assets/img/dockerhub.png)

### Pulling image from registry
To pull the image, i will be pulling it to my digitalocean VM

Command :
```shell
docker pull appan/flask-app-2:latest
```

Result :

![](/assets/img/docker-pull.png)

### Listing image
Command :
```shell
docker image ls
```

Result :

![](/assets/img/docker-ls.png)

### Run and list container

Run container command :
```shell
docker run -p 5000:5000 -d --env-file .env --network=host --name flask-app appan/flask-app-2:latest
```

flags :
```
-p 5000:5000 : publish container port 5000 to host port 5000
-d : run the container in detached mode
--env-file .env : export .env file to the container
--network=host : using network mode "host" to enable accessing local postgres database
```

List container command :
```shell
docker ps
```

Result :

![](/assets/img/docker-ps.png)

## Kubernetes

### Deployment
YAML deployment [file](/kubernetes/deployment.yaml):
```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: flask-app-2
spec:
  selector:
    matchLabels:
      app: flask-app-2
  template:
    metadata:
      labels:
        app: flask-app-2
    spec:
      containers:
      - name: flask-app-2
        image: appan/flask-app-2
        resources:
          requests:
            memory: "64Mi"
            cpu: "100m"
          limits:
            memory: "128Mi"
            cpu: "500m"
        ports:
        - containerPort: 5000
        env:
        - name: DB_USERNAME
          value: dev
        - name: DB_PASSWORD
          value: dev
        - name: DB_URL
          value: host.minikube.internal
        - name: DB_NAME
          value: flask_db
```
- `metadata.name`: The name of the deployment
- `spec.selector.matchLabels`: The labels selector for the deployment
- `template.metadata.labels` : The labels of the deployment
- `spec.containers` :
    - `name` : The name of the container that will be deployed in the pods
    - `image` : The name of the image that will be used to create the container
    - `resources.requests.memory` : The provisioned memory for each pod
    - `resources.requests.cpu` : The provisioned cpu for each pod
    - `resource.limits.memory` : The limit of memory that each pod can use
    - `resource.limits.cpu` : The limit of cpu that each pod can use
    - `ports.containerPort` : The ports that will be published by the container
    - `env.*` : The environment variables that will be used inside the pods

### Accessing App From Outside The Cluster
To expose kubernetes pods over a network, we can use kubernetes object called `Service`. Kubernetes provides 4 types of Services which are :

- `ClusterIP`

  This service exposes pods over internal cluster IP which will make pods accesible through the cluster's internal network. Since it only expose on the cluster's internal, we can't access it from outside the cluster

- `NodePort`

  Expose a static port from the node in the cluster so that it can be reachable from network outside the cluster. With this service, we can access the pods through the node's IP address and the nodeport that we chose.

- `LoadBalancer`

  Expose the pods using an external loadbalancer. The loadbalancer will forward the request to the cluster's node. But since kubernetes does not support a loadbalancer component, we have to use a third-party provider for this service.

- `ExternalName`

  Creates a mapping from the service to an external DNS hostname.

For this project, I will be using `NodePort` service to expose the deployment and make it accessible from outside the cluster.

Service YAML [file](/kubernetes/service.yaml)
```yaml
apiVersion: v1
kind: Service
metadata:
  name: flask-svc
spec:
  selector:
    app: flask-app-2
  type: NodePort
  ports:
  - port: 5000
    targetPort: 5000
    nodePort: 30000
```

The service will expose node `30000` on the cluster and maps it towards port `5000` of the deployment's pods

### List Pods

Command :
```shell
kubectl get pods
```

Result :

![](/assets/img/kubectl-get-pods.png)

### List Services

Command :
```shell
kubectl get service
```

Result :

![](/assets/img/kubectl-get-services.png)

### Pods vs Deployments
Pods is a smallest unit of work in kubernetes. It encapsulates one or more application's containers. The containers inside a pod shares resources such as storage and IP address. The containers can comunicate each other through localhost.

Deployments is a kubernetes object with the purpose to manage a set of pods. Deployments offer additional functionalities to manage pods such as :
- Self Healing

  Allowing pods to automatically replace crashed pods so it will match the desired number of replicas that's already been declared

- Scaling

  Adding / Reducing number of pods replicas

- Updates

  Updating all the pods replicas using update strategy such as `RollingUpdate` or `Recreate`

- Rollback

  Rolling back the pods the the previous version

## Ansible

### Pros and Cons

#### Pros
- Simple

  Ansible notebook implementation that is using YAML which have a rather declarative nature makes it easier to understand, more readable, and more simple to write for a sets of basic tasks.

- Agentless

  Ansible's push-based design through SSH means that it can easily run without having to actually install it on the target machines. This simplify running the notebook to any given machines without having to set it up first

- Security

  By communicating through SSH encryption, ansible offers an extended security in remote machines management.

- Flexible

  Ansible's flexibility to integrate with various system and platforms such as cloud providers (GCP, Azure, AWS etc.), containerization (Docker, Kubernetes etc.) Makes it reliable to use in various environments and use cases

- Scalability

  Ansible can handle managing execution on multiple machines, although it came with the downside of limiting the performances as the number of machine scales.

#### Cons

- Stateless

  Ansible's stateless nature which doesn't track the state beyond executing the described tasks makes it virtually difficult to track state of the machine/system that we are going to manage.

- SSH Overhead

  Communicating over SSH might add an additional overhead latency that can slower the process compared to running using an agent-based tools.

- Performance

  Despite its ability to scale and manage multiple systems, it came with a catch that the growing number of systems being managed can take a toll towards its performance due to lack of the built-in state tracking and SSH connection overhead

- Complexity

  Although ansible is great for running sets of basic tasks, it might add more layer of complexity when the tasks being executed grow more and more complex.

- Limited Support on Windows

  Ansible has a limited support on windows compared to Unix/Linux which makes it more difficult to manage system if we are using windows.

### Running Playbook

Here's the playbook YAML to install docker and run the container
```yaml
- hosts: localhost
  become: true

  tasks:
    - name: Install packages
      apt:
        pkg:
          - apt-transport-https
          - ca-certificates
          - curl
          - software-properties-common

    - name: Add Docker GPG Key
      apt_key:
        url: https://download.docker.com/linux/ubuntu/gpg
        state: present

    - name: Add Docker Repository
      apt_repository:
        repo: deb https://download.docker.com/linux/ubuntu jammy stable
        state: present

    - name: Install Docker
      apt:
        pkg: docker-ce
        state: latest
        update_cache: true

    - name: Pull Image
      community.docker.docker_image:
        name: "appan/flask-app-2:latest"
        source: pull

    - name: Run Container
      community.docker.docker_container:
        name: "flask-app"
        image: "appan/flask-app-2:latest"
        ports:
          - 5000:5000
        detach: true
        env_file: ../.env
        network_mode: host
```

To test it, I will be executing the playbook on an empty VM that still don't have docker installed

#### Executing the playbook

```shell
ansible-playbook playbooks/playbook.yaml -l localhost -u root
```

Result:

![](/assets/img/ansible-playbook.png)

#### Checking the image

```shell
docker image ls
```

![](/assets/img/ansible-docker-image.png)

#### Ensuring the container is running

Container is running

![](/assets/img/ansible-docker-ps.png)

Listening on port `5000`

![](/assets/img/ansible-netstat.png)