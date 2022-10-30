FROM python:3.10

# set the working directory
WORKDIR /usr/src/app

# copy the requiremens.txt to working directory
COPY ./requirements.txt ./


# install all the dependencies
RUN pip install --no-cache-dir --upgrade -r requirements.txt

COPY . .

# start the uvicorn app
CMD ["uvicorn", "server:app", "--host", "0.0.0.0", "--port", "8080"]
