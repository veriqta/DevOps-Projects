# CONNECTING TO THE MYSQL DOCKER CONTAINER

Step 3: Connecting to the MySQL Docker Container
We can either connect directly to the container running the MySQL server or use a second container as a MySQL client. Let us see 
what the first option looks like.

Approach 1

Connecting directly to the container running the MySQL server:

```
$ docker exec -it mysql bash

or

$ docker exec -it mysql mysql -uroot -p
```

Provide the root password when prompted. With that, you’ve connected the MySQL client to the server.

Finally, change the server root password to protect your database. Exit the the shell with exit command

Flags used

- exec used to execute a command from bash itself
- -it makes the execution interactive and allocate a pseudo-TTY
- bash this is a unix shell and its used as an entry-point to interact with our container
- mysql The second mysql in the command "docker exec -it mysql mysql -uroot -p" serves as the entry point to interact with mysql
 container just like bash or sh
- -u mysql username
- -p mysql password


Approach 2

At this stage you are now able to create a docker container but we will need to add a network. So, stop and remove the previous
mysql docker container.

```
docker ps -a
docker stop mysql 
docker rm mysql or <container ID> 04a34f46fb98
```

verify that the container is deleted

```
docker ps -a

CONTAINER ID   IMAGE                                COMMAND                  CREATED          STATUS                             PORTS                       NAMES
```


First, create a network:
 $ docker network create --subnet=172.18.0.0/24 tooling_app_network 

Creating a custom network is not necessary because even if we do not create a network, Docker will use the default network for all 
the containers you run. By default, the network we created above is of DRIVER Bridge. So, also, it is the default network. You can
verify this by running the docker network ls command.

But there are use cases where this is necessary. For example, if there is a requirement to control the cidr range of the containers
running the entire application stack. This will be an ideal situation to create a network and specify the --subnet

For clarity’s sake, we will create a network with a subnet dedicated for our project and use it for both MySQL and the application 
so that they can connect.

Run the MySQL Server container using the created network.

First, let us create an environment variable to store the root password:

 $ export MYSQL_PW= 
verify the environment variable is created

```
echo $MYSQL_PW
```

Then, pull the image and run the container, all in one command like below:

 $ docker run --network tooling_app_network -h mysqlserverhost --name=mysql-server -e MYSQL_ROOT_PASSWORD=$MYSQL_PW  -d mysql/mysql-server:latest 

Flags used

- -d runs the container in detached mode
- --network connects a container to a network
- -h specifies a hostname

If the image is not found locally, it will be downloaded from the registry.

Verify the container is running:

 $ docker ps -a 
 
 
 ```
 CONTAINER ID   IMAGE                                COMMAND                  CREATED          STATUS                             PORTS                       NAMES
7141da183562   mysql/mysql-server:latest            "/entrypoint.sh mysq…"   12 seconds ago   Up 11 seconds (health: starting)   3306/tcp, 33060-33061/tcp   mysql-server
 ```
 
 
 
As you already know, it is best practice not to connect to the MySQL server remotely using the root user. Therefore, we will create
an SQL script that will create a user we can use to connect remotely.

Create a file and name it create_user.sql and add the below code in the file:

 $ CREATE USER ''@'%' IDENTIFIED BY ''; GRANT ALL PRIVILEGES ON * . * TO ''@'%'; 

Run the script:
Ensure you are in the directory create_user.sql file is located or declare a path

 $ docker exec -i mysql-server mysql -uroot -p$MYSQL_PW < create_user.sql 

If you see a warning like below, it is acceptable to ignore:


```
mysql: [Warning] Using a password on the command line interface can be insecure.
```


Connecting to the MySQL server from a second container running the MySQL client utility
The good thing about this approach is that you do not have to install any client tool on your laptop, and you do not need to connect
directly to the container running the MySQL server.

Run the MySQL Client Container:

 $ docker run --network tooling_app_network --name mysql-client -it --rm mysql mysql -h mysqlserverhost -u  -p 

Flags used:


- --name gives the container a name
- -it runs in interactive mode and Allocate a pseudo-TTY
- --rm automatically removes the container when it exits
- --network connects a container to a network
- -h a MySQL flag specifying the MySQL server Container hostname
- -u user created from the SQL script
- admin username-for-user-created-from-the-SQL-script-create_user.sql
- -p password specified for the user created from the SQL script


Prepare database schema
Now you need to prepare a database schema so that the Tooling application can connect to it.

1. Clone the Tooling-app repository from here
 $ git clone https://github.com/darey-devops/tooling.git 

2. On your terminal, export the location of the SQL file
 $ export tooling_db_schema=/tooling_db_schema.sql 

You can find the tooling_db_schema.sql in the tooling/html/tooling_db_schema.sql folder of cloned repo.

Verify that the path is exported


```
echo $tooling_db_schema
```

3. Use the SQL script to create the database and prepare the schema. With the docker exec command, you can execute a command in a 
running container.

 $ docker exec -i mysql-server mysql -uroot -p$MYSQL_PW < $tooling_db_schema 

4. Update the .env file with connection details to the database
The .env file is located in the html tooling/html/.env folder but not visible in terminal. you can use vi or nano


```
sudo vi .env

MYSQL_IP=mysqlserverhost
MYSQL_USER=username
MYSQL_PASS=client-secrete-password
MYSQL_DBNAME=toolingdb
```

Flags used:

- MYSQL_IP mysql ip address "leave as mysqlserverhost"
- MYSQL_USER mysql username for user export as environment variable
- MYSQL_PASS mysql password for the user exported as environment varaible
- MYSQL_DBNAME mysql databse name "toolingdb"


5. Run the Tooling App
Containerization of an application starts with creation of a file with a special name - 'Dockerfile' (without any extensions). 
This can be considered as a 'recipe' or 'instruction' that tells Docker how to pack your application into a container. In this
project, you will build your container from a pre-created Dockerfile, but as a DevOps, you must also be able to write Dockerfiles.

You can [watch this video](https://youtu.be/hnxI-K10auY) to get an idea how to create your Dockerfile and build a container from it.

And on this [page](https://docs.docker.com/develop/develop-images/dockerfile_best-practices/), you can find official Docker best 
practices for writing Dockerfiles.

So, let us containerize our Tooling application; here is the plan:


- Make sure you have checked out your Tooling repo to your machine with Docker engine
- First, we need to build the Docker image the tooling app will use. The Tooling repo you cloned above has a Dockerfile for this purpose. 
Explore it and make sure you understand the code inside it.
- Run docker build command
- Launch the container with docker run
- Try to access your application via port exposed from a container


Let us begin:

Ensure you are inside the directory "tooling" that has the file Dockerfile and build your container :

$ docker build -t tooling:0.0.1 . 
In the above command, we specify a parameter -t, so that the image can be tagged tooling"0.0.1 - Also, you have to notice the . at 
the end. This is important as that tells Docker to locate the Dockerfile in the current directory you are running the command. 
Otherwise, you would need to specify the absolute path to the Dockerfile.

6. Run the container:
 $ docker run --network tooling_app_network -p 8085:80 -it tooling:0.0.1 

Let us observe those flags in the command.


We need to specify the --network flag so that both the Tooling app and the database can easily connect on the same virtual network
we created earlier.
The -p flag is used to map the container port with the host port. Within the container, apache is the webserver running and, by default,
it listens on port 80. You can confirm this with the CMD ["start-apache"] section of the Dockerfile. But we cannot directly use 
port 80 on our host machine because it is already in use. The workaround is to use another port that is not used by the host machine.
In our case, port 8085 is free, so we can map that to port 80 running in the container.

**Note:** You will get an error. But you must troubleshoot this error and fix it. Below is your error message.


```
AH00558: apache2: Could not reliably determine the server's fully qualified domain name, using 172.18.0.3. Set the 'ServerName' directive globally to suppress this message
```


Hint: You must have faced this error in some of the past projects. It is time to begin to put your skills to good use. Simply do a
google search of the error message, and figure out where to update the configuration file to get the error out of your way.

If everything works, you can open the browser and type http://localhost:8085

You will see the login page.


![7001](https://user-images.githubusercontent.com/85270361/210183773-80aa420f-b277-4da8-9921-2ae12db646b1.PNG)


The default email is test@gmail.com, the password is 12345 or you can check users' credentials stored in the toolingdb.user table.
