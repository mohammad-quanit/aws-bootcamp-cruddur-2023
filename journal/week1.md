# Week 1 — App Containerization

## Run locally & containerizing the Backend (Python Flask App)

After watching your live stream, below are the steps I've done to run BE environment locally & then containerize python application

<br />

### **Run BE Server locally & tested it**

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

## **Build Dockerfile**

``` bash
docker build -t  backend-flask ./backend-flask
```


<br />
