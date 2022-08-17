###########
# BUILDER #
###########

# pull official base image
FROM python:3.10-buster as builder

# set work directory
RUN mkdir /usr/src/app
WORKDIR /usr/src/app

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# install psycopg2 dependencies
RUN apt-get update && apt-get install -y postgresql gcc python3-dev musl-dev g++ gettext

# lint
RUN pip install --upgrade pip
COPY . .

# install dependencies
COPY ./requirements.txt .
RUN pip wheel --no-cache-dir --no-deps --wheel-dir /usr/src/app/wheels -r requirements.txt

#########
# FINAL #
#########

# pull official base image
FROM python:3.10-buster

# create the app users
RUN addgroup --system master && adduser --system master && adduser master master

# create the appropriate directories
ENV HOME=/home/master/
ENV APP_HOME=/home/master/app
RUN mkdir $APP_HOME
RUN mkdir /home/master/app/staticfiles
RUN mkdir /home/master/app/mediafiles
RUN mkdir /home/master/app/logs
WORKDIR $APP_HOME

# install dependencies
RUN apt-get update && apt-get install -y libpq-dev
COPY --from=builder /usr/src/app/wheels /wheels
COPY --from=builder /usr/src/app/requirements.txt .
RUN pip install --no-cache /wheels/*

# copy entrypoint.sh
COPY ./docker/backend/entrypoint.sh $APP_HOME
RUN sed -i 's/\r$//g'  $APP_HOME/entrypoint.sh
RUN chmod +x  $APP_HOME/entrypoint.sh

# copy project
COPY . $APP_HOME

# chown all the files to the app users
RUN chown -R master:master $APP_HOME

# change to the app users
USER master

# run entrypoint.sh
ENTRYPOINT ["/home/master/app/entrypoint.sh"]
