# rest-api-assignment
An API's app based on Flask and Flask Rest Framework.

A REST API is an architectural style for an API that uses HTTP requests to access and use data. That data can be used to GET, PUT, POST and DELETE data types, commonly refers as CRUD operations.

This project is a REST API server that ingests metrics from its clients and
generates on-demand stats reports. This utilizes [Flask](https://flask.palletsprojects.com/en/1.1.x/), [SQLAlchemy](https://www.sqlalchemy.org/) and [Marshmallow](https://flask-marshmallow.readthedocs.io/en/latest/). When running the application, it creates a `db.sqlite` file in the project's root directory which is database file containing all the data. You can delete this file when the testing completes.

## Requirements

1. [Python](https://www.python.org/) (Recommended 3.6+)
2. [Pip3](https://pip.pypa.io/en/stable/)
3. [Virtualenv](https://virtualenv.pypa.io/en/stable/)

## Setup Instructions
Follow these instructions to setup the project locally on your machine.

1. Clone the project repository.
    ```bash
    $ git clone https://github.com/marshmallo/rest-api-assignment.git
    ```
2. Change to the project's root directory.
    ```bash
    $ cd rest-api-assignment/
    ```
3. Create a virtual environment of name `.venv` in project's root directory. Use python version that you are using.
    ```bash
    $ virtualenv --python=python3.6 .venv
    ```
4. Activate the virtual environment.
    ```bash
    $ source .venv/bin/activate
    ```
5. Install the project requirements.
    ```bash
    $ pip3 install -r requirements.txt
    ```
6. Run the application using the python version that you are using (Recommended only in Development.)
    ```bash
    $ python3.6 app.py
    ```
7. Deactivate the virtual environment.
    ```bash
    $ deactivate
    ```

## In Production

To run the app in Production use [Gunicorn](https://gunicorn.org/), a production-grade WSGI server.

1. Repeat the setup instructions from [1-5].
2. Run the application using gunicorn in Production.
    ```bash
    $ gunicorn --bind 0.0.0.0:8080 wsgi:app
    ```
3. Deactivate the virtual environment.
    ```bash
    $ deactivate
    ```
## Docker Setup

Install [Docker](https://docs.docker.com/get-docker/), then build the image and run the application container from the project's root directory as follows:

1. Build the image.
    ```bash
    $ docker build --tag flask-rest-api:latest .
    ```
2. Run the container and publish the container’s port to the host machine.
    ```bash
    $ docker run -it -p 8080:8080 --name <any-name> flask-rest-api:latest
    ```
3. Run container in background. (Optional)
    ```bash
    $ docker run -dit -p 8080:8080 --name <any-name> flask-rest-api:latest
    ```

## Test the API

To test the API you can run the application locally or launch a docker container as described above. 

The API exposes the following endpoints:

1. Ingestion
    ```
    Method: POST
    Path: /metrics
    ```
   Headers:
    ```
    content-type: application/json
    ```
    JSON body structure:
    ```
    {
        "percentage_cpu_used": <integer between 0-100 >,
        "percentage_memory_used": <integer between 0-100 >
    }
    ```
    Sample curl requests:
    ```bash
    $ curl \
        -XPOST \
        -H "Content-Type: application/json" \
        --data '{"percentage_cpu_used": 55, "percentage_memory_used": 90}' \
        http://127.0.0.1:8080/metrics
    ```
    ```bash
    $ curl \
        -XPOST \
        -H "Content-Type: application/json" \
        --data '{"percentage_cpu_used": 210, "percentage_memory_used": 35}' \
        http://127.0.0.1:8080/metrics
    ```
    Responses:
    1. `200`: **OK** (If data ingested successfully).
    2. `500`: **Internal Server Error** (If anything wrong such as Integer value out of defined range).

2. Report Generation
    ```
    Method: GET
    Path: /report
    ```
   Headers:
    ```
    content-type: application/json
    ```
   JSON body structure:
    ```
    [
        {
            "ip": <IP address of machine>,
            "percentage_cpu_used": <maximum cpu %>,
            "percentage_memory_used": <maximum memory %>
        },
        ...
    ]
    ```
   Sample curl request:
    ```bash
    $ curl \
        -XGET \
        -H "Content-Type: application/json" \
        http:// 127.0.0.1:8080/report
   
   
    [
        {
            "ip": "172.17.0.1",
            "percentage_cpu_used": 55,
            "percentage_memory_used": 90 
        }
    ]
    ```
   Responses:
    1. `200`: **OK** (Success).
    2. `500`: **Internal Server Error** (Something's Wrong).
    
## Recommendations

1. Avoid running the application in Development mode, rather use *Gunicorn* to run the application in Production.
2. Use [Postman](https://www.postman.com/), an API client to test the API's instead of *curl*. Use it when running the application with *Gunicorn* and to see the response codes.
   