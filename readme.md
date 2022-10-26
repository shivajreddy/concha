# Concha API

##### Table of Contents  
[01. Scope of Project](#Scope)  
[02. Project Structure](#projectstructure)  
[03. Run Project Locally](#runlocally)  
[04. Run on GCP](#rungcp)  


<a name="Scope"/>
## Scope of project

Assignment Document : [GoogleDoc](https://docs.google.com/document/d/1Ucla0d4T7ykzz40NQbfbNpDTVlFaOqGh4y7P9nX16Ls/edit)  
Notion Doc: [NotionDoc](https://www.notion.so/shivareddy/Concha-Backend-Engineer-Test-Q-Discussion-93fe3866ca8f49c0bf88654983df8773)  
Postman Collection : [Postman](https://www.postman.com/blue-comet-93782/workspace/myspace/collection/19132019-dafc3e8a-2e92-48ad-9781-5bdb5c0967e5?action=share&creator=19132019)  

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
	├── server # "app" (python package) for BE app 
	│   ├── __init__.py # this file makes "app" a "Python package" 
	│   ├── main.py # "main" module, e.g. import app.main 
	│   ├── dependencies.py # "dependencies" module, e.g. import app.dependencies 
	│   ├── dependencies.py # "dependencies" module, e.g. import app.dependencies 
	│   │ 
	│   └── routers # "routers" is a "Python subpackage" 
	│       ├── __init__.py # makes "routers" a "Python subpackage" 
	│       ├── users.py # "users" submodule, e.g. import app.routers.items 
	│       └── audio_data.py # "audio_data" submodule, e.g. import app.routers.users 
	│  
	├── psql_db # "app" is a Python package 
	│   └── __init__.py # this file makes "app" a "Python package" 
	│  
	├── alembic # 
	│   ├── versions  #
	│   └── env.py  #
	│  
	├── run.py # starting point of the application 
	│  
	├── Dockerfile
	│  
	├── docker-compose-dev.yml
	│  
	├── docker-compose-prod.yml
	│  
	├── alembic.ini
	│  
	├── .env
	│  
	├── requirements.txt # only the required dependecies for the application
	│  
	├── Dockerfile
	│  
	├── Dockerfile
	│  
	└── readme.md # documentation for the project
```

<a name="runlocally"/>
## Run the project locally

#### Step 0: Prerequisites
[Choice of IDE](https://www.jetbrains.com/products/#type=ide), [Docker](https://www.docker.com/), [Python3.10](https://www.python.org/downloads/)

#### Step 1: Pull project
create a new empty project, and inside the root of the empty project: **pull** the repository by running the following command
```
git pull https://github.com/shivajreddy/concha.git
```

#### Step 2: Setup containers & Run
Create the docker containers using the `docker-compose-dev.yml` file and run the project with the following command in your terminal:
```
docker-compose -f docker-compose-dev.yml up
```

This command(utilizing the docker-compose-dev.yml) does all the heavy lifting of project setup on your local machine especially setting the dev environment:
	a: It First builds the image's using the `Dockerfile` which is in the root directory. Then it connects to your local machines port `8000`. In any case you want to run this project at a different port other than `8000`, you can change it in the `.env` file since the command in the dev compose file overrides the command in the `Dockerfile`
	b: sync the volumes for live changes, between the local machines project directory and containers project directory
	c: Create a postgress container dependancy, which will be initialized using the environment variables provided in `env` file
	d: a

#### Step 3: Initiate the Database using alembic
The project comes with the first alembic revision already set up, this revision basically creates all the tables with approriate conditions and relations. For any further changes in the Database schema in the future, you can easily modify(or add new) models in the `psql_db/models.py` and create a new revision using `alembic revision -m "<message related to the revision>"`, and then upgrade the database 

SSH to container's(`dev-server-1` which is running the application) terminal.
```
docker exec -it concha-dev-server-1 bash
```

Run the command
`alembic upgrade head`

Since there is already a revision that comes with the project, this command brings the database to this revision which in your case is intiating the DB with all the tables with correct schema.

#### Step 4: Running Tests



<a name="rungcp"/>
## Running project on GCP

#### Step 0: Prerequisites
Google Cloud Platform: [GCP](https://cloud.google.com/)  



## API Endpoints

TODO, document all end points
TODO, mention how to use /docs
