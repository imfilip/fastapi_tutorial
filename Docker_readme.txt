How to use docker:
We will create first container for python app:
1) Create Dockerfile.
2) Think about next commands - the order is important for optimalization purpose.
3) After the Dockerfile is ready, you can build your container from image you created:
docker build -t fastapi .
docker build -t [name of container] [relative path to Dockerfile]

a) You can check a list of your all docker images:
docker image ls

4) To create working container you could use 'docker run' command, but instead I encourage to learn using docker-compose command.
To do that you have to create file docker-compose.yml.
After you finished container specification run this command:
docker-compose up -d

a) You can check if container is running:
docker ps

b) Logs:
docker logs fastapi_tutorial-api-1

c) To turn off container type:
docker-compose down

docker-compose create new image
You can enforce docker-compose to rebuild the image again by adding flag --build

WOW! My container is running and you can check that with:
docker ps
Amazing is the fact that you can send GET request to localhost:8000 (port specified in docker-compose.yml) and you will get response probably!
So it is running in the background! You know the whole http server (uvicorn).

Lets create another container consists of database environment.

I had an issue. After creation of both services I couldn't interact with database. The log (docker logs fastapi_tutorial-api-1) showed that the table does not exist. I had to uncomment part responsible for creation table in postgres database.
The best way would be to initialize alembic commands on container cmd, but at this moment I have not tried to do that.

There is a way to get into container console:
docker exec -it fastapi_tutorial-api-1 bash 