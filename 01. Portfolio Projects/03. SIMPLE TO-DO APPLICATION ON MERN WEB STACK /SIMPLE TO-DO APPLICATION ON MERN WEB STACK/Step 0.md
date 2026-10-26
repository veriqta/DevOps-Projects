# In this project, you are tasked to implement a web solution based on MERN stack in AWS Cloud.

## MERN Web stack consists of following components:

- MongoDB: A document-based, No-SQL database used to store application data in a form of documents.

- ExpressJS: A server side Web Application framework for Node.js.

- ReactJS: A frontend framework developed by Facebook. It is based on JavaScript, used to build User Interface (UI) components.

- Node.js: A JavaScript runtime environment. It is used to run JavaScript on a machine rather than in a browser.


![proj3](https://user-images.githubusercontent.com/85270361/210118416-5abdf8d5-5fb8-4caf-b315-3d98d45a9e3d.PNG)


As shown on the illustration above, a user interacts with the ReactJS UI components at the application front-end residing in the
browser. This frontend is served by the application backend residing in a server, through ExpressJS running on top of NodeJS.

Any interaction that causes a data change request is sent to the NodeJS based Express server, which grabs data from the MongoDB 
database if required, and returns the data to the frontend of the application, which is then presented to the user.



Side Self Study

1. Make a research what types of Database Management Systems (DBMS) exist and what each type is more suitable for. Be able to 
explain the difference between Relational DBMS and NoSQL (of a different kind).
2. Get yourself familiar with a concept of Web Application Frameworks. Get to know what server-side (backend) and client-side
(forntend) frameworks exist and what they are used for.
3. Practice basic JavaScript syntax just for fun.
4. Explore what RESTful API is and what it is used for in Web development.
5. Read what Cascading Style Sheets (CSS) is used for and browse basic syntax and properties.


Instructions On How To Submit Your Work For Review And Feedback
To submit your work for review and feedback – follow this instruction.

# Step 0 – Preparing prerequisites
In order to complete this project you will need an AWS account and a virtual server with Ubuntu Server OS.

If you do not have an AWS account – go back to Project 1 Step 0 to sign in to AWS free tier account and create a new EC2 Instance 
of t2.nano family with Ubuntu Server 20.04 LTS (HVM) image. Remember, you can have multiple EC2 instances, but make sure you STOP 
the ones you are not working with at the moment to save available free hours.

Hint #1: When you create your EC2 Instances, you can add Tag "Name" to it with a value that corresponds to a current project you 
are working on – it will be reflected in the name of the EC2 Instance. Like this:


![pro3](https://user-images.githubusercontent.com/85270361/210118546-bead7609-5dea-4538-86f6-2e69c17408cc.PNG)


Hint #2 (for Windows users only): In previous projects we used Putty and Git Bash to connect to our EC2 Instances.

In this project and going forward, we are going to explore the usage windows terminal.

Watch this videos to learn how to set up windows terminal on your pc;

windows installatatiosn part 1

windows installatatiosn part 2

Task
To deploy a simple To-Do application that creates To-Do lists like this:


![porr3](https://user-images.githubusercontent.com/85270361/210118580-173d44bc-f848-48a3-b63d-4aed7998c638.PNG)
