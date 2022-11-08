# Concha API


## About the Concha API
This documentation describes how to use the Concha API using production deployment, Postman, or cURL.  
When you make a request to the REST API, you will specify an HTTP method and a path that follow a specific schema. Additionally, you might also specify request headers and path, query, or body parameters (Ex. Authorization info in header for protected routes). The API will return the response status code, response headers, and potentially a response body.

[![Build and Deploy Code 🚀](https://github.com/shivajreddy/concha/actions/workflows/build-deploy.yml/badge.svg)](https://github.com/shivajreddy/concha/actions/workflows/build-deploy.yml)

##### Table of Contents  
[01. Scope of Project](#Scope)  
[02. Project Structure](#projectstructure)  
[03. Run Project Locally](#runlocally)  
[04. Run on GCP](#rungcp)  


<a name="Scope"/>
## Scope of project

Assignment Document : [GoogleDoc](https://docs.google.com/document/d/1Ucla0d4T7ykzz40NQbfbNpDTVlFaOqGh4y7P9nX16Ls/edit)  
Notion Doc: [NotionDoc](https://www.notion.so/shivareddy/Concha-Backend-Engineer-Test-Q-Discussion-93fe3866ca8f49c0bf88654983df8773)  
Postman Collection : [Postman](https://www.postman.com/blue-comet-93782/workspace/concha/overview)

| *Stack*                       | *Technology*           | 
|:----------------------------- |:---------------------- |
| Backend                       | FastAPI                |
| Database                      | PSQL                   |
| Database Migration            | Alembic                |
| O.R.M                         | SQLAlchemy             |
| API Platform                  | Postman                |
| Authorization, Authentication | Bcrypt, JWT            |
| Version Control               | Git                    |
| Application Devlopment        | Docker, Docker Compose |
| Cloud                         | GCP                    |

<a name="projectstructure"/>
## Project Structure

```
	<project-root>
	│  
	├── server                      # "app" (python package) for BE app 
	│   ├── __init__.py             # this file makes "app" a "Python package" 
	│   ├── main.py                 # "main" module, e.g. import app.main 
	│   ├── dependencies.py         # "dependencies" module, e.g. import app.dependencies 
	│   ├── dependencies.py         # "dependencies" module, e.g. import app.dependencies 
	│   │ 
	│   └── routers                 # "routers" is a "Python subpackage" 
	│       ├── __init__.py         # makes "routers" a "Python subpackage" 
	│       ├── users.py            # "users" submodule, e.g. import app.routers.items 
	│       └── audio_data.py       # "audio_data" submodule, e.g. import app.routers.users 
	│  
	├── psql_db              # "app" is a Python package 
	│   └── __init__.py      # this file makes "app" a "Python package" 
	│  
	├── alembic              # Datbase migrations
	│   ├── versions 
	│   └── env.py 
	│  
	├── tests                # tests package
	│   ├── database.py      # database settings for running tests
	│   ├── test_user.py     # tests for /user route
	│   └── test_audio.py    # tests for /audio-data route
	│  
	├── Dockerfile           # Dockerfile to build docker image for the project
	│  
	├── docker-compose-dev.yml    # Docker compose file for dev environment
	│  
	├── docker-compose-prod.yml   # Docker compose file for dev environment
	│  
	├── alembic.ini
	│  
	├── .env                # all the environment variables for the project
	│  
	├── requirements.txt    # only the required dependecies for the application
	│  
	└── readme.md           # documentation for the project
```

<a name="runlocally"/>
## Run the project locally

#### Step 0: Prerequisites
[Choice of IDE](https://www.jetbrains.com/products/#type=ide), [Docker](https://www.docker.com/), [Python3.10](https://www.python.org/downloads/), [Postgres](https://postgresapp.com/downloads.html) | [PgAdmin](https://www.pgadmin.org/download/pgadmin-4-windows/)

#### Step 1: Clone project
create a new empty project folder, and navigate to this project directory in your terminal. **Clone** the repository by running the command:
```bash
git clone https://github.com/shivajreddy/concha.git
```

#### Step 2: Setup Docker containers & Run
Create the docker images and respective containers altogether using the `docker-compose-dev.yml` file. This project embraces Docker compose, to run the Concha Server on local machine and on the server. To start create images, create containers using those images, and starting running the app, simply run the command:
```bash
docker compose -f docker-compose-dev.yml up
```
in this `-f` refers to compose and build docker containers using the give file.

To tear down the contaiers simply run.
```bash
docker compose -f docker-compose-dev.yml down
```

Docker Compose does all the heavy lifting of project setup on your local machine especially setting the dev environment:
	a: It First builds the image's using the `Dockerfile` which is in the root directory. Then it connects to your local machines port `8000`. In any case you want to run this project at a different port other than `8000`, you can change it in the `.env` file since the command in the dev compose file overrides the command in the `Dockerfile`
	b: sync the volumes for live changes, between the local machines project directory and containers project directory
	c: Create a postgress container dependancy, which will be initialized using the environment variables provided in `env` file
	d: And link the `server` container of python app to the PSQL container.

#### Step 3: Initiate the Database using alembic
The project comes with the first alembic revision already set up, this revision basically creates all the tables with approriate conditions and relations. For any further changes in the Database schema in the future, you can easily modify(or add new) models in the `psql_db/models.py` and create a new revision using `alembic revision -m "<message related to the revision>"`, and then upgrade the database 

SSH to container's(`dev-server-1` which is running the application) terminal. (Assuming that concha-dev-server-1 is the name of container, if you have changed it, then use the new containers name instead, which you can find using `docker container ls` command)
```bash
docker exec -it concha-dev-server-1 bash
```

now you are in the terminal of the container that is running the python app. so for the very first time the app runs(either local machine or server) we have to start the database migrataions, so that our database is upto date with the modal schema defined in the project. to achieve this run the command:
```bash
alembic upgrade head
```

Since there is already a revision that comes with the project, this command brings the database to this revision which in your case is intiating the DB with all the tables with correct schema.

#### Step 4: Running Tests

Before running tests, you have to make sure you are using the correct python environment on your local machine. First create virtual environment in the project directory, for example lets call this environment `venv`. To create your virtual environment, with your terminal pointing to project's root directory run `python -m venv venv` this will create the `venv` virtual environment, and now install all the dependencies in the virtual environment, using the 'requirements.txt' file that holds all the necessary dependancies. To do this run: `python -m pip install -r requirements.txt`

You must create a local database which we can use for testing the application. Create a new database with name `concadb_test`
```bash
pytest
```

Since 'pytest' is one of the dependancies you installed earlier, this command will start pytest, which will start collecting all the tests, and run them. You can use `-s` flag for pytest for displaying print statements in your tests, `-v` for verbose(more details), `-x` to stop tests if there is any error found.

Postman Collection : [Postman](https://www.postman.com/blue-comet-93782/workspace/concha/overview)

<a name="rungcp"/>
## Running project on GCP

#### Step 0: Prerequisites
Google Cloud Platform: [GCP](https://cloud.google.com/)  

#### Step 1: Create a VM instance
Choose the CPU cores and Memory depending on the amount of traffic that the server must handle.

#### Step 2: Create a Network Tag
Go to `vpc networks` > `Firewall` > `CREATE FIREWALL RULE`. Name this rule as `allow8000` and choose the network-tag name as `allow8000` and for IPv4 ranges write `0.0.0.0/0`, and the checkt `TCP` and TCP ports as "8000".
Now go back to VM instances, choose your newly created instance and select 'EDIT' and and the network-tag `allow8000` to this instance.

TL;DR GCP by default doesn't allow 8000 port on your VM instances, so you have to create a firewall rule to allow 8000 port to be open to the external IP's. Because FastAPI by default run's the app on port 8000 and we want to keep using that to be consistent.

#### Step 3: Clone the project, Run the server
create a new empty project folder, and navigate to this project directory in your terminal. **Clone** the repository by running the command:
```bash
$ git clone https://github.com/shivajreddy/concha.git
$ cd concha
```

Run the server using:
```bash
docker compose -f docker-compose-prod.yml up -d
```
This will start the docker containers and run the app in **detached** mode

SSH to container's(`dev-server-1` which is running the application) terminal. (Assuming that concha-dev-server-1 is the name of container, if you have changed it, then use the new containers name instead, which you can find using `docker container ls` command)
```bash
docker exec -it concha-dev-server-1 bash
```

now you are in the terminal of the container that is running the python app. so for the very first time the app runs(either local machine or server) we have to start the database migrataions, so that our database is upto date with the modal schema defined in the project. to achieve this run the command:
```bash
alembic upgrade head
```

#### Step 4: 


#### Step x : Running Tests on the server
This project has Github action as part of CI/CD to automatically run all the tests on a linux machine provided by GitHub, by using the GitHub action. The build sequence is written in 'build-deploy.yml' file, which can be found at `.github/workflows/build-deploy.yml` in your project source directory.


## Making a request
To make a request, first find the HTTP method and the path(end point) for the operation that you want to use. For example, the "Get all Users" operation uses the `GET` method and the `{base-url}/user/all` path.

## API Endpoints

- [ ] Show how to read and use swagger ui, mention how to use /docs

| *Method* | *Endpoint* | Query params | Form-data   | Description                                        |
|:--------: |:---------- | :------------: | :-----------: | :-------------------------------------------------- |
| GET      | /user/all  | No | no | example description alskdfjalksjdflasjdflkasjdfklj |

> Search for a user
```
{{concha}}/user/search
```
Description: search for a user in the DB using either name or email but not both

