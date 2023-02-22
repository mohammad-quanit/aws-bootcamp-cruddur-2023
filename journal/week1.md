# Week 1 — App Containerization

## Run locally & containerizing the Backend (Python Flask App)

After watching your live stream, below are the steps I've done to run BE environment locally & then containerize python application

<br />

### **Run BE Server locally & Dockerized it**

``` bash
cd backend-flask
export FRONTEND_URL="*"
export BACKEND_URL="*"
pip install -r requirements.txt
python3 -m flask run --host=0.0.0.0 --port=4567

```
After running these commands, i've made sure that

- Click the unlock button to make the port public for access
- Access the BE server using `http://127.0.0.1:4567/api/activities/home`

``` bash
gitpod /workspace/aws-bootcamp-cruddur-2023/backend-flask (week-1) $ python3 -m flask run --host=0.0.0.0 --port=4567
 * Debug mode: off
WARNING: This is a development server. Do not use it in a production deployment. Use a production WSGI server instead.
 * Running on all addresses (0.0.0.0)
 * Running on http://127.0.0.1:4567
 * Running on http://10.0.5.2:4567
Press CTRL+C to quit
```

- Gets the response in JSON below
``` json
// 20230219235348
// http://127.0.0.1:4567/api/activities/home

[
  {
    "created_at": "2023-02-17T18:53:48.046050+00:00",
    "expires_at": "2023-02-24T18:53:48.046050+00:00",
    "handle": "Andrew Brown",
    "likes_count": 5,
    "message": "Cloud is very fun!",
    "replies": [
      {
        "created_at": "2023-02-17T18:53:48.046050+00:00",
        "handle": "Worf",
        "likes_count": 0,
        "message": "This post has no honor!",
        "replies_count": 0,
        "reply_to_activity_uuid": "68f126b0-1ceb-4a33-88be-d90fa7109eee",
        "reposts_count": 0,
        "uuid": "26e12864-1c26-5c3a-9658-97a10f8fea67"
      }
    ],
    "replies_count": 1,
    "reposts_count": 0,
    "uuid": "68f126b0-1ceb-4a33-88be-d90fa7109eee"
  },
 ...
]
```

<br />

### **Add Dockerfile**

Created a file in backend-flask folder named `Dockerfile` and added below steps

``` dockerfile
FROM python:3.10-slim-buster

WORKDIR /backend-flask

COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt

COPY . .

ENV FLASK_ENV=development

EXPOSE ${PORT}
CMD [ "python3", "-m" , "flask", "run", "--host=0.0.0.0", "--port=4567"]
```

### **Build Dockerfile**

``` bash
docker build -t backend-flask:1.0 ./backend-flask
```


<br />


### **Run Frontend Server locally & Dockerized it**


``` bash
cd frontend-react-js
npm install
npm start
```
After running these commands, i've made sure that

- Click the unlock button to make the port public for access
- Access the BE server using `http://127.0.0.1:3000/`
- I've created an account and succesfully able to see cruddr application UI


### **Add Dockerfile**

Created a file in frontend-react-js folder named `Dockerfile` and added below steps

``` dockerfile
FROM node:16.18-alpine

ENV PORT=3000

COPY . /frontend-react-js
WORKDIR /frontend-react-js
RUN npm install
EXPOSE ${PORT}
CMD ["npm", "start"]
```

Bonus Step: I've used `node:16.18-alpine` image and was able to reduce image size from 1.6gb to 458mb. As Alpine is a lightweight Linux distribution that is designed to be resource-efficient, which makes it an excellent choice for building container images that require a small footprint.

### **Build Dockerfile**

``` bash
docker build -t frontend-react-js:1.0 ./frontend-react-js
```

Uptil now, I was able to create `images` for both of the Dockerfiles i.e one for Backend & other one for Frontend.


But rather than creating and managing two seperate docker containers, I've create `docker-compose.yml` to manage both containers simultaneously.

Below is the `docker-compose.yml` code:

``` docker
version: "3.8"
services:
  backend-flask:
    environment:
      FRONTEND_URL: "https://3000-${GITPOD_WORKSPACE_ID}.${GITPOD_WORKSPACE_CLUSTER_HOST}"
      BACKEND_URL: "https://4567-${GITPOD_WORKSPACE_ID}.${GITPOD_WORKSPACE_CLUSTER_HOST}"
    build: ./backend-flask
    ports:
      - "4567:4567"
    volumes:
      - ./backend-flask:/backend-flask
  frontend-react-js:
    environment:
      REACT_APP_BACKEND_URL: "https://4567-${GITPOD_WORKSPACE_ID}.${GITPOD_WORKSPACE_CLUSTER_HOST}"
    build: ./frontend-react-js
    ports:
      - "3000:3000"
    volumes:
      - ./frontend-react-js:/frontend-react-js

  dynamodb-local:
    user: root
    command: "-jar DynamoDBLocal.jar -sharedDb -dbPath ./data"
    image: "amazon/dynamodb-local:latest"
    container_name: dynamodb-local
    ports:
      - "8000:8000"
    volumes:
      - "./docker/dynamodb:/home/dynamodblocal/data"
    working_dir: /home/dynamodblocal

  db:
    image: postgres:13-alpine
    restart: always
    environment:
      - POSTGRES_USER=postgres
      - POSTGRES_PASSWORD=password
    ports:
      - '5432:5432'
    volumes:
      - db:/var/lib/postgresql/data

# the name flag is a hack to change the default prepend folder
# name when outputting the image names
networks:
  internal-network:
    driver: bridge
    name: cruddur

volumes:
  db:
    driver: local
```

After creating `docker-compose.yml` file, I was able to up and running both of my containers simultaneously. Below is the screenshot:

![Docker ps](../_docs/assets/compose-containers.png)

<br />

### **Setup AWS DynamoDB & Postgres Locally**

