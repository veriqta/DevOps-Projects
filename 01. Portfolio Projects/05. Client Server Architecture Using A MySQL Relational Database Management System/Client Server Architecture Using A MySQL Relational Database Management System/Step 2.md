# IMPLEMENT A CLIENT SERVER ARCHITECTURE USING MYSQL DATABASE MANAGEMENT SYSTEM (DBMS).

TASK – Implement a Client Server Architecture using MySQL Database Management System (DBMS).
To demonstrate a basic client-server using MySQL Relational Database Management System (RDBMS), follow the below instructions

1. Create and configure two Linux-based virtual servers (EC2 instances in AWS).

```
Server A name - `mysql server`
Server B name - `mysql client`
```

2. On mysql server Linux Server install MySQL Server software.

Interesting fact: MySQL is an open-source relational database management system. Its name is a combination of "My", the name of
co-founder Michael Widenius’s daughter, and "SQL", the abbreviation for Structured Query Language.

3. On mysql client Linux Server install MySQL Client software.

4. By default, both of your EC2 virtual servers are located in the same local virtual network, so they can communicate to each other
using local IP addresses. Use mysql server's local IP address to connect from mysql client. MySQL server uses TCP port 3306 by 
default, so you will have to open it by creating a new entry in ‘Inbound rules’ in ‘mysql server’ Security Groups. 
For extra security, do not allow all IP addresses to reach your ‘mysql server’ – allow access only to the specific local
IP address of your ‘mysql client’.

5. You might need to configure MySQL server to allow connections from remote hosts.

```
sudo vi /etc/mysql/mysql.conf.d/mysqld.cnf
```

Replace ‘127.0.0.1’ to ‘0.0.0.0’ like this:




![5018](https://user-images.githubusercontent.com/85270361/210136418-f4832b77-89d4-4e65-8287-6e73a338a65a.PNG)


6. From mysql client Linux Server connect remotely to mysql server Database Engine without using SSH. You must use the mysql 
utility to perform this action.

7. Check that you have successfully connected to a remote MySQL server and can perform SQL queries:

```
Show databases;
```

If you see an output similar to the below image, then you have successfully completed this project – you have deloyed a fully 
functional MySQL Client-Server set up.
Well Done! You are getting there gradually. You can further play around with this set up and practice in creating/dropping databases 
& tables and inserting/selecting records to and from them.

Congratulations!


![5020](https://user-images.githubusercontent.com/85270361/210136618-f3738310-258f-4848-ab6d-710a06cce2e8.PNG)


