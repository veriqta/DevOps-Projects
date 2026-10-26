Now, when you have already learned how to deploy LAMP, LEMP and MERN Web stacks – it is time to get yourself familiar with MEAN stack
and deploy it to Ubuntu server.

# MEAN Stack is a combination of following components:
- MongoDB (Document database) – Stores and allows to retrieve data.
- Express (Back-end application framework) – Makes requests to Database for Reads and Writes.
- Angular (Front-end application framework) – Handles Client and Server Requests
- Node.js (JavaScript runtime environment) – Accepts requests and displays results to end user


Side Self Study
1. Refresh your knowledge of OSI model
2. Read about Load Balancing, get yourself familiar with different types and techniques of traffic load balancing.
3. Practice in editing simple web forms with HTML + CSS + JS


Instructions On How To Submit Your Work For Review And Feedback
To submit your work for review and feedback – follow this instruction.

## Step 0 – Preparing prerequisites
In order to complete this project you will need an AWS account and a virtual server with Ubuntu Server OS.

If you do not have an AWS account – go back to Project 1 Step 0 to sign in to AWS free tier account ans create a new EC2 Instance of
t2.nano family with Ubuntu Server 20.04 LTS (HVM) image. Remember, you can have multiple EC2 instances, but make sure you STOP 
the ones you are not working with at the moment to save available free hours.

Hint: In previous projects we used different tools to connect to an EC2 instance, but if you do not want to install or launch
anything outside of AWS, you can open youc CLI straight from Web Console in AWS, like this:


![5013](https://user-images.githubusercontent.com/85270361/210133716-47e26536-6479-440d-9c15-981cab3bbaac.PNG)

Task
In this assignment you are going to implement a simple Book Register web form using MEAN stack.

Step 1: Install NodeJs
Node.js is a JavaScript runtime built on Chrome’s V8 JavaScript engine. Node.js is used in this tutorial to set up the Express
routes and AngularJS controllers.

Update ubuntu

```
sudo apt update
```

Upgrade ubuntu

```
sudo apt upgrade
```

Add certificates

```
sudo apt -y install curl dirmngr apt-transport-https lsb-release ca-certificates

curl -sL https://deb.nodesource.com/setup_12.x | sudo -E bash -
```

Install NodeJS

```
sudo apt install -y nodejs
```

Step 2: Install MongoDB
MongoDB stores data in flexible, JSON-like documents. Fields in a database can vary from document to document and data structure can
be changed over time. For our example application, we are adding book records to MongoDB that contain book name, isbn number, author,
and number of pages.

mages/WebConsole.gif

```
sudo apt-key adv --keyserver hkp://keyserver.ubuntu.com:80 --recv 0C49F3730359A14518585931BC711F9BA15703C6
```

```
echo "deb [ arch=amd64 ] https://repo.mongodb.org/apt/ubuntu trusty/mongodb-org/3.4 multiverse" |
sudo tee /etc/apt/sources.list.d/mongodb-org-3.4.list
```

Install MongoDB

```
sudo apt install -y mongodb
```

Start The server

```
sudo service mongodb start
```

Verify that the service is up and running

```
sudo systemctl status mongodb
```

Install npm – Node package manager.

```
sudo apt install -y npm
```

Install body-parser package

We need ‘body-parser’ package to help us process JSON files passed in requests to the server.


```
sudo npm install body-parser
```

Create a folder named ‘Books’

```
mkdir Books && cd Books
```

In the Books directory, Initialize npm project

```
npm init
```

Add a file to it named server.js

```
vi server.js
```

Copy and paste the web server code below into the server.js file.

```
var express = require('express');
var bodyParser = require('body-parser');
var app = express();
app.use(express.static(__dirname + '/public'));
app.use(bodyParser.json());
require('./apps/routes')(app);
app.set('port', 3300);
app.listen(app.get('port'), function() {
    console.log('Server up: http://localhost:' + app.get('port'));
});
```

