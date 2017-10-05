## To Build

To run:

Install docker for Mac:
https://docs.docker.com/docker-for-mac/#/download-docker-for-mac

Check out Cloudmatch from github
Now, create a conda environment 
```
conda create --name cloudmatch python=2 django libxml2 lxml
source activate cloudmatch
pip install -r requirements.txt
```

cd into web/ and add a few runtime directories (note: we'll fix this with a real install someday)
```
ln -s ../pyfalcon pyfalcon
mkdir output
```

Then turn on the services we're running in Docker
```
docker run --name cmpostgres -d -p 5432:5432 postgres
docker run --name cmrabbitmq --hostname rmq -d -p 15672:15672 -p 5672:5672 rabbitmq:3-management
```

(If you've rebooted your machine, just restart the containers:
```
docker start cmpostgres
docker start cmrabbitmq
```

Then, start turning on the frontend

```
# Not sure you actually still need these two exports
export DATABASE_HOST=localhost
export BROKER_URL=amqp://guest:guest@localhost//
```

The first time you run an instance, or if you've blown the database away, you have to run these two commands:
```
cd web/
source activate cloudmatch
python manage.py migrate
python manage.py createsuperuser (use admin/password123)
```

Now, create two windows - in the first:
```
cd web/
source activate cloudmatch
celery -A cloudmatch worker -E -l info --concurrency=3 
```

and in the second window
```
cd web/
source activate cloudmatch
python manage.py runserver 0.0.0.0:8000
```

Go to `localhost:8100/frontend/`

Add a job at the bottom. You get redirected back to the list of jobs in the system. 
A background task gets kicked off in `forms.py` when you create the job (look for the job_add.delay(job.id) bit).
That background task is in `tasks.py` and is running in a separate process (in fact, in a separate container).
For now all it does is create a directory for the job and runs the debug blocker

This depends on having pyfalcon somewhere in django path. The easiest way to solve that is to just symlink the pyfalcon/ directory to this directory.
(be careful not to check it in twice in that case...)
Someday we'll make it an entry into requirements.txt and install it in the python lib directory...

You may also need to create an output/ directory in the directory that you ran docker-compose

A couple of TODOs:
- refactor to turn the views and forms into common code - the only difference between them is really deciding which pairs we pick
- debug_blocker doesn't return all columns - on walmart, for example, it drops pricing
- which negative pairs should we be taking? I'm taking the tail of the top200candidates.csv, after removing the marked positive examples
- If the additional examples aren't edited at all, do we just accept what the user enters?


Old stuff:

```
docker-compose build
docker-compose up
```
(The docker-compose up command for the first time often has some race conditions as postgres creates tables. I'll fix it for real sometime but for
now, consider hitting 'control-c' and running docker-compose up again)

(Note: that cloudmatch_web_1 might be named something else. Run ```docker ps``` and look for web_1 for the name)


In another window 
```
docker exec -it cloudmatch_web_1 bash
```
(after that docker exec, you'll be running in the container)
