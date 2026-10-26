PRACTICE TASK
Practice Task №1 – Implement a POC to migrate the PHP-Todo app into a containerized application.
Download php-todo repository from [here](https://github.com/darey-devops/php-todo)

The project below will challenge you a little bit, but the experience there is very valuable for future projects.

Part 1
1. Write a Dockerfile for the TODO app
2. Run both database and app on your laptop Docker Engine
3. Access the application from the browser

Part 2
1. Create an account in Docker Hub
2. Create a new Docker Hub repository
3. Push the docker images from your PC to the repository

Part 3
1. Write a Jenkinsfile that will simulate a Docker Build and a Docker Push to the registry
2. Connect your repo to Jenkins
3. Create a multi-branch pipeline
4. Simulate a CI pipeline from a feature and master branch using previously created Jenkinsfile
5. Ensure that the tagged images from your Jenkinsfile have a prefix that suggests which branch the image was pushed from. 
For example, feature-0.0.1.
6. Verify that the images pushed from the CI can be found at the registry.


Deployment with [Docker Compose](https://docs.docker.com/compose/)
All we have done until now required quite a lot of effort to create an image and launch an application inside it. We should not have
to always run Docker commands on the terminal to get our applications up and running. There are solutions that make it easy to write 
[declarative code](https://en.wikipedia.org/wiki/Declarative_programming) in [YAML](https://en.wikipedia.org/wiki/YAML), and get all
the applications and dependencies up and running with minimal effort by launching a single command.

In this section, we will refactor the Tooling app POC so that we can leverage the power of Docker Compose.

1. First, install Docker Compose on your workstation from [here](https://docs.docker.com/compose/install/)
2. Create a file, name it tooling.yaml
3. Begin to write the Docker Compose definitions with YAML syntax. The YAML file is used for defining services, networks, and volumes:

```
version: "3.9"
services:
  tooling_frontend:
    build: .
    ports:
      - "5000:80"
    volumes:
      - tooling_frontend:/var/www/html
```

The YAML file has declarative fields, and it is vital to understand what they are used for.

- version: Is used to specify the version of Docker Compose API that the Docker Compose engine will connect to. This field is optional
from docker compose version v1.27.0. You can verify your installed version with:

```
docker-compose --version
docker-compose version 1.28.5, build c4eb3a1f 
```

- service: A service definition contains a configuration that is applied to each container started for that service. In the snippet 
above, the only service listed there is tooling_frontend. So, every other field under the tooling_frontend service will execute 
some commands that relate only to that service. Therefore, all the below-listed fields relate to the tooling_frontend service.
- build
- port
- volumes
- links


You can visit the site here to find all the fields and read about each one that currently matters to you 
-> https://www.balena.io/docs/reference/supervisor/docker-compose/

You may also go directly to the official documentation site to read about each field here 
-> https://docs.docker.com/compose/compose-file/compose-file-v3/

Let us fill up the entire file and test our application:



```
version: "3.9"
services:
  tooling_frontend:
    build: .
    ports:
      - "5000:80"
    volumes:
      - tooling_frontend:/var/www/html
    links:
      - db
  db:
    image: mysql:5.7
    restart: always
    environment:
      MYSQL_DATABASE: <The database name required by Tooling app >
      MYSQL_USER: <The user required by Tooling app >
      MYSQL_PASSWORD: <The password required by Tooling app >
      MYSQL_RANDOM_ROOT_PASSWORD: '1'
    volumes:
      - db:/var/lib/mysql
volumes:
  tooling_frontend:
  db:
```

Run the command to start the containers

```
docker-compose -f tooling.yaml  up -d 
```

Verify that the compose is in the running status:

```
docker compose ls
```


Practice Task №2 – Complete Continous Integration With A Test Stage

1. Document your understanding of all the fields specified in the Docker Compose file tooling.yaml
2. Update your Jenkinsfile with a test stage before pushing the image to the registry.
3. What you will be testing here is to ensure that the tooling site http endpoint is able to return status code 200. Any other code 
will be determined a stage failure.
4. Implement a similar pipeline for the PHP-todo app.
5. Ensure that both pipelines have a clean-up stage where all the images are deleted on the Jenkins server.


**Congratulations!**


![7002](https://user-images.githubusercontent.com/85270361/210184553-603c5131-55eb-437e-9aa3-7a5d409bc644.PNG)


You have started your journey into migrating an application running on virtual machines into the Cloud with containerization.

Now you know how to prepare a Dockerfile, build an image with Docker build and deploy it with Docker Compose!

In the next project, we will expand your skills further into more advanced use cases and technologies.

Move on to the next project!
