Welcome to your very first PBL Project
You must be really excited to start getting your hands dirty. There is a lot of projects ahead, so without any delay, lest get started.

As you kick off your career in DevOps, you will soon realise that everything you will be doing as a DevOps engineer is around software,
websites, applications etc. And, there are different stack of technologies that make different solutions possible. These stack of
technologies are regarded as WEB STACKS. Examples of Web Stacks include LAMP, LEMP, MEAN, and MERN stacks. As you proceed in your
journey, you will be required to understand and implement all of these technology stacks. Lets have a short close up on what a 
Technology stack is.

What is a Technology stack?
A technology stack is a set of frameworks and tools used to develop a software product. This set of frameworks and tools are very 
specifically chosen to work together in creating a well-functioning software. They are acronymns for individual technologies used
together for a specific technology product. some examples are…

- LAMP (Linux, Apache, MySQL, PHP or Python, or Perl)
- LEMP (Linux, Nginx, MySQL, PHP or Python, or Perl)
- MERN (MongoDB, ExpressJS, ReactJS, NodeJS)
- MEAN (MongoDB, ExpressJS, AngularJS, NodeJS

WARNING: Most of the things you will be doing at the early days may not mean a lot to you. Sometimes it may seem like you are just 
copying and pasting. That is absolutely fine. We want some concepts to begin to register in your sub-conscious mind, and without you 
realising it, you are building up skills. although, there are certain traps that will require you to troubleshoot along the way. 
So watch out for them in all your project implementations.

After successful completion of PBL projects 1 to 4, you will be able to achieve the following.

1. Become very confident on the Linux Terminal

2. Deepen your understanding of Web Stacks and familiarity between the differences between the different Web Technology stacks such 
as LAMP, LEMP, MEAN, and MERN stacks

3. Solid Linux administration skills in Storage management, NFS, troubleshooting, and basic networking.

4. Basic knowledge of AWS platform and components used to host a Website of various Web stacks.

Being able to work with Linux requires the ability to work outside the level of your present knowledge. It means that in the 
real world, you will be faced with tasks that you have never worked on before, and with Google search and its results, you can 
achieve a lot. Thanks to “Google!!!”. 

It is one of the essential skills you will need to develop – constructing a correct search query for Google to process and having
the ability to comb through resources that interpretes into a potential solution for you is a great skill to have as well.



Side Self Study
- Conduct a Google search on what software development life cycle (SDLC) is and document your finding in a Google word file.
- Conduct another Google search, understand what LAMP stack means.
- Read about ‘chmod’ and ‘chown’ commands in Linux and understand how access and ownership of files and directories work.
- Learn what TCP and UPD terms mean and how they are different. List down ports most commonly used in Web (http, https, ssh, telnet,
 ftp, sftp, telnet)
- Get yourself familiar with basic text editing in [Vi (Vim)](https://www.vim.org/) editor.[Practice Here](https://www.openvim.com/)

- Instructions On How To Submit Your Work For Review And Feedback
To submit your work for review and feedback – follow this instruction.

As a beginner it would be nice that you also set up your workspace for learning, you can take a look at these video series to learn
how to do that.


# Step 0 – Preparing prerequisites
In order to complete this project you will need an AWS account and a virtual server with Ubuntu Server OS.

[AWS](https://aws.amazon.com/) is the biggest Cloud Service Provider and it offers a free tier account that we are going to leverage for our projects.

Do not focus too much on AWS itself right now, there will be a proper Cloud introduction and configuration projects later in our course.

Right now, all we need to know is that AWS can provide us with a free virtual server called EC2 (Elastic Compute Cloud) for our needs.

Spinning up a new EC2 instance (an instance of a virtual server) is only a matter of a few clicks.

You can either Watch the videos below to get yourself set up.

1. AWS account setup and Provisioning an Ubuntu Server
2. Connecting to your EC2 Instance

Or follow the instructions below.

1. Register a new AWS account following this instruction.
2. Select your preferred region (the closest to you) and launch a new EC2 instance of t2.micro family with Ubuntu Server 20.04 LTS (HVM)
launch EC2

IMPORTANT – save your private key (.pem file) securely and do not share it with anyone! If you lose it, you will not be able to
connect to your server ever again!

For Windows users, you will need a tool called putty to connect to your EC2 Instance. Download Putty Here.
For Mac users, you can simply open up Terminal and use the ssh command to get into the server.

IMPORTANT NOTICE
Both Putty and ssh use the SSH protocol to establish connectivity between computers. It is the most secure protocol because it uses
crypto algorithms to encrypt the data that is transmitted – it uses TCP port 22 which is open for all newly created EC2 intances in
AWS by default. Most of these terminologies will make more sense to you as you proceed. So for now, if nothing makes sense, just 
ignore. But be assured that the information is already registered in your sub-conscious mind. So it will become useful to you soon.

The process to connect to the virtual server is different between Windows and Mac. So lets take a quick tour.

# Connecting to EC2 terminal

## Using the terminal on MAC/Linux

- The terminal is already installed by default. You just need to open it up.
- You do not need to convert to a .ppk file. Just use the same key as downloaded from AWS.
- Change directory into the loacation where your PEM file is. Most likely will be in the Downloads folder

```
cd ~/Downloads
```


IMPORTANT - Anywhere you see these anchor tags < > , going forward, it means you will need to replace the content in there with values 
specific to your situation. For example, if we need you to replace the name you have saved the private key on your machine, we will 
write something like < private-key-name >.

If the private key you downloaded was named my-private-key.pem simply remove the anchor tags and insert my-private-key.pem in the
command you are required to execute. Lets try this and follow the instructions below to get some work done.

- Change premissions for the private key file (.pem), otherwise you can get an error "Bad permissions"

```
sudo chmod 0400 <private-key-name>.pem
```


- Connect to the instance by running

```
ssh -i <private-key-name>.pem ubuntu@<Public-IP-address>
``` 
  
  
  
# Using Windows Terminal

Remember the private key your downloaded from AWS while provisioning the server? It is a PEM file format. You can open it up to see
the content and have a glimpse of what a PEM file looks like.

Now, we are going to use that PEM key to connect to our EC2 Instnace via ssh.

On, windows the windows terminal tool is not installed by default, you can install it from here

cd Downloads

IMPORTANT - Anywhere you see these anchor tags < > , going forward, it means you will need to replace the content in there with values
specific to your situation. For example, if we need you to replace the name you have saved the private key on your machine, we will 
write something like < private-key-name >.

If the private key you downloaded was named my-private-key.pem simply remove the anchor tags and insert my-private-key.pem in the 
command you are required to execute. Lets try this and follow the instructions below to get some work done.

Connect to the instance by 

```
ssh -i <private-key-name>.pem ubuntu@<Public-IP-address>
``` 
 
 
 Congratulations! You have just created your very first Linux Server in the Cloud and our set up looks like this now:
  (You are the client)



![projject1-step0](https://user-images.githubusercontent.com/85270361/210112007-5cd14a18-8aaa-4c7a-857e-b18400535bdd.PNG)


Please read information about AWS free tier limits and make sure that you STOP your EC2 instance when you are not using it.

Stop EC2

All we need to know right now is that we can use 750 hours (31.25 days) of t2.micro server per month for the first 12 months FOR FREE.

You can launch and stop new instances when you need to, but by default there is a soft-limit of maximum 5 running instances at the same time. In our first projects we will be using only 1 running instance at a time. When you stop an instance – it stops consuming available hours.

Note that every time you stop and start your EC2 instance – you will have a new IP address, it is normal behavior, so do not forget to update your SSH credentials when you try to connect to your EC2 server.

Let us move on and configure our EC2 machine to serve a Web server!
