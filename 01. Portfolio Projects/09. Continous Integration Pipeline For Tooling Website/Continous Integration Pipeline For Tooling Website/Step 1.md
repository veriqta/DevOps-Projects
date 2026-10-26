# INSTALL AND CONFIGURE JENKINS SERVER

Step 1 – Install Jenkins server

1. Create an AWS EC2 server based on Ubuntu Server 20.04 LTS and name it "Jenkins"

2. Install JDK (since Jenkins is a Java-based application)

```
sudo apt update
sudo apt install default-jdk-headless
```

3. Install Jenkins

```
wget -q -O - https://pkg.jenkins.io/debian-stable/jenkins.io.key | sudo apt-key add -
sudo sh -c 'echo deb https://pkg.jenkins.io/debian-stable binary/ > \
    /etc/apt/sources.list.d/jenkins.list'
sudo apt update
sudo apt-get install jenkins
```

Make sure Jenkins is up and running

```
sudo systemctl status jenkins
```

4. By default Jenkins server uses TCP port 8080 – open it by creating a new Inbound Rule in your EC2 Security Group

![6012](https://user-images.githubusercontent.com/85270361/210151779-4467072e-8a07-46e6-951b-5176e067c110.PNG)


5. Perform initial Jenkins setup.
From your browser access http://<Jenkins-Server-Public-IP-Address-or-Public-DNS-Name>:8080

You will be prompted to provide a default admin password

  
![6013](https://user-images.githubusercontent.com/85270361/210151821-9b9baaf6-e89c-4a9b-b06a-c2c1d6e01930.PNG)

  
Retrieve it from your server:
  
```
sudo cat /var/lib/jenkins/secrets/initialAdminPassword
```
  
Then you will be asked which plugings to install – choose suggested plugins.
 

![6014](https://user-images.githubusercontent.com/85270361/210151862-fee4be20-f6b3-4c3b-9830-78ce4a28253b.PNG)

  
Once plugins installation is done – create an admin user and you will get your Jenkins server address.

The installation is completed!
  

![6015](https://user-images.githubusercontent.com/85270361/210151901-28354c74-518a-49d6-85bd-ab7b98c7f419.PNG)
  

Step 2 – Configure Jenkins to retrieve source codes from GitHub using Webhooks
In this part, you will learn how to configure a simple Jenkins job/project (these two terms can be used interchangeably). This job 
will will be triggered by GitHub webhooks and will execute a ‘build’ task to retrieve codes from GitHub and store it locally on 
Jenkins server.

1. Enable webhooks in your GitHub repository settings
  
  
![6017](https://user-images.githubusercontent.com/85270361/210151970-d0f50b34-4da2-45cb-a028-9848ba197ebc.PNG)

  
![6016](https://user-images.githubusercontent.com/85270361/210151978-adbff3ba-d11a-4a41-8b67-a3e40bf18095.PNG)

  
2. Go to Jenkins web console, click "New Item" and create a "Freestyle project"
  

![6018](https://user-images.githubusercontent.com/85270361/210152007-3464d147-0ac9-4c44-a9f6-a81d6612d887.PNG)

  
To connect your GitHub repository, you will need to provide its URL, you can copy from the repository itself
  
  
![6019](https://user-images.githubusercontent.com/85270361/210152055-41f70f37-ec2d-477a-a3f2-456b15474459.PNG)

  
In configuration of your Jenkins freestyle project choose Git repository, provide there the link to your Tooling GitHub repository 
and credentials (user/password) so Jenkins could access files in the repository.


![6020](https://user-images.githubusercontent.com/85270361/210152098-dbee8c5f-66e9-4d67-9366-09bddc8b2ed8.PNG)

  
  
Save the configuration and let us try to run the build. For now we can only do it manually.
Click "Build Now" button, if you have configured everything correctly, the build will be successfull and you will see it under #1
  
  
![6021](https://user-images.githubusercontent.com/85270361/210152125-9b0ea377-b751-4f3c-a671-bcc957d2ee37.PNG)

  
You can open the build and check in "Console Output" if it has run successfully.

If so – congratulations! You have just made your very first Jenkins build!

But this build does not produce anything and it runs only when we trigger it manually. Let us fix it.

3. Click "Configure" your job/project and add these two configurations
Configure triggering the job from GitHub webhook:

  
![6022](https://user-images.githubusercontent.com/85270361/210152165-d652ba1d-cbc0-4d4b-ae87-03109268de38.PNG)

Configure "Post-build Actions" to archive all the files – files resulted from a build are called "artifacts".
  

![6023](https://user-images.githubusercontent.com/85270361/210152199-9432da9f-2eb0-4369-bc2a-45e8c7838985.PNG)

  
Now, go ahead and make some change in any file in your GitHub repository (e.g. README.MD file) and push the changes to the master branch.

You will see that a new build has been launched automatically (by webhook) and you can see its results – artifacts, saved on Jenkins
server.


![6024](https://user-images.githubusercontent.com/85270361/210152236-8ee1b372-25cf-4848-b8d0-e3413972abeb.PNG)

  
You have now configured an automated Jenkins job that receives files from GitHub by webhook trigger (this method is considered as
‘push’ because the changes are being ‘pushed’ and files transfer is initiated by GitHub). There are also other methods: trigger one 
job (downstreadm) from another (upstream), poll GitHub periodically and others.

By default, the artifacts are stored on Jenkins server locally

  
```
ls /var/lib/jenkins/jobs/tooling_github/builds/<build_number>/archive/
```
  
  
