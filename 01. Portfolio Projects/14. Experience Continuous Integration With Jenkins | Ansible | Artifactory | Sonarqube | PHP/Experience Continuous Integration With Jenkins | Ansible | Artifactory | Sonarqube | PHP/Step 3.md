# ANSIBLE ROLES FOR CI ENVIRONMENT

Now go ahead and Add two more roles to ansible:

1. [SonarQube](https://www.sonarsource.com/products/sonarqube/) (Scroll down to the Sonarqube section to see instructions on how to 
set up and configure SonarQube manually)

2. [Artifactory](https://jfrog.com/artifactory/)

Why do we need SonarQube?
SonarQube is an open-source platform developed by SonarSource for continuous inspection of code quality, it is used to perform 
automatic reviews with static analysis of code to detect bugs, code smells, and security vulnerabilities. 
[Watch a short description here](https://youtu.be/vE39Fg8pvZg). There is a lot more hands on work ahead with SonarQube and Jenkins.
So, the purpose of SonarQube will be clearer to you very soon.


## Why do we need Artifactory?
Artifactory is a product by JFrog that serves as a binary repository manager. The binary repository is a natural extension to the
source code repository, in that the outcome of your build process is stored. It can be used for certain other automation, 
but we will it strictly to manage our build artifacts.

[Watch a short description here](https://youtu.be/upJS4R6SbgM) Focus more on the first 10.08 mins



## Configuring Ansible For Jenkins Deployment

In previous projects, you have been launching Ansible commands manually from a CLI. Now, with Jenkins, we will start running Ansible
from Jenkins UI.

To do this,

## 1. Navigate to Jenkins URL

## 2. Install & Open Blue Ocean Jenkins Plugin

## 3. Create a new pipeline


![6050](https://user-images.githubusercontent.com/85270361/210166359-afc39e9a-e5d1-4f90-887c-c7f56850a977.PNG)


## 4. Select GitHub


![6051](https://user-images.githubusercontent.com/85270361/210166383-6b87d457-5e81-4a72-a7e2-ab39d0e4b05c.PNG)


## 5. Connect Jenkins with GitHub

![6052](https://user-images.githubusercontent.com/85270361/210166800-b48df50f-ee7a-4d96-9679-402c6af0f55f.PNG)


## 6. Login to GitHub & Generate an Access Token

![6053](https://user-images.githubusercontent.com/85270361/210166867-abee93ae-73ff-409a-abef-aa3cf71b7b28.PNG)


![6054](https://user-images.githubusercontent.com/85270361/210166886-2d966818-5871-4c8a-8ff5-c54a63d3a4b1.PNG)


## 7. Copy Access Token

![6055](https://user-images.githubusercontent.com/85270361/210166915-09d3642e-7a2c-4df0-908b-6a47e25f21b3.PNG)


## 8. Paste the token and connect


![6056](https://user-images.githubusercontent.com/85270361/210166941-eb18f017-5fa8-48d0-8682-a5c7d3075720.PNG)


## 9. Create a new Pipeline

![6057](https://user-images.githubusercontent.com/85270361/210166994-35ab2b64-5c09-4e7e-a2bc-57a95e54770b.PNG)


At this point you may not have a [Jenkinsfile](https://www.jenkins.io/doc/book/pipeline/jenkinsfile/) in the Ansible repository, so 
Blue Ocean will attempt to give you some guidance to create one. But we do not need that. We will rather create one ourselves.
So, click on Administration to exit the Blue Ocean console.



![6058](https://user-images.githubusercontent.com/85270361/210167147-1f028a40-1807-439e-9801-354f0af65ad3.PNG)


## Here is our newly created pipeline. It takes the name of your GitHub repository.


![6059](https://user-images.githubusercontent.com/85270361/210167178-19245aec-9c52-4a64-ac21-2d07bccc9646.PNG)


Let us create our Jenkinsfile
Inside the Ansible project, create a new directory deploy and start a new file Jenkinsfile inside the directory.


![6060](https://user-images.githubusercontent.com/85270361/210167197-b16be56f-afcf-402e-9689-875b3be41fe9.PNG)


Add the code snippet below to start building the Jenkinsfile gradually. This pipeline currently has just one stage called Build and 
the only thing we are doing is using the shell script module to echo Building Stage


```
pipeline {
    agent any

  stages {
    stage('Build') {
      steps {
        script {
          sh 'echo "Building Stage"'
        }
      }
    }
    }
}
```


## Now go back into the Ansible pipeline in Jenkins, and select configure


![6061](https://user-images.githubusercontent.com/85270361/210167261-33892450-920b-44d2-bf88-0fabed414bd2.PNG)


## Scroll down to Build Configuration section and specify the location of the Jenkinsfile at deploy/Jenkinsfile


![6062](https://user-images.githubusercontent.com/85270361/210167304-6ad952c6-0a01-48a0-b4ea-7450575a6785.PNG)


## Back to the pipeline again, this time click "Build now"

![6063](https://user-images.githubusercontent.com/85270361/210167327-6eec0ade-d714-41bb-91a9-903da1fdf76b.PNG)


This will trigger a build and you will be able to see the effect of our basic Jenkinsfile configuration by going through the console
output of the build.

To really appreciate and feel the difference of Cloud Blue UI, it is recommended to try triggering the build again from Blue Ocean
interface.

## 1.  on Blue Ocean

![6064](https://user-images.githubusercontent.com/85270361/210167355-e6ec9846-bb2d-4247-a55f-2a2a79f0fe0a.PNG)


2. Select your project
3. Click on the play button against the branch


![6065](https://user-images.githubusercontent.com/85270361/210167364-479764ba-a92a-4f96-a1eb-a0a75bc9ecd9.PNG)


Notice that this pipeline is a multibranch one. This means, if there were more than one branch in GitHub, Jenkins would have scanned
the repository to discover them all and we would have been able to trigger a build for each branch.

Let us see this in action.

1. Create a new git branch and name it feature/jenkinspipeline-stages
2. Currently we only have the Build stage. Let us add another stage called Test. Paste the code snippet below and push the new changes 
to GitHub.


```
pipeline {
    agent any

  stages {
    stage('Build') {
      steps {
        script {
          sh 'echo "Building Stage"'
        }
      }
    }

    stage('Test') {
      steps {
        script {
          sh 'echo "Testing Stage"'
        }
      }
    }
    }
}
```


4. To make your new branch show up in Jenkins, we need to tell Jenkins to scan the repository.

## . Click on the "Administration" button


![6066](https://user-images.githubusercontent.com/85270361/210167415-a38a103d-6ece-4bb2-81db-a697d2d7985f.PNG)


## 2. Navigate to the Ansible project and click on "Scan repository now"


![6067](https://user-images.githubusercontent.com/85270361/210167461-304b5836-99f9-463d-aee8-478c15bd621a.PNG)


## 3. Refresh the page and both branches will start building automatically. You can go into Blue Ocean and see both branches there too.

![6068](https://user-images.githubusercontent.com/85270361/210167498-d43853d2-d089-4336-abc3-d28ac977c07c.PNG)


## 4. In Blue Ocean, you can now see how the Jenkinsfile has caused a new step in the pipeline launch build for the new branch.


![6069](https://user-images.githubusercontent.com/85270361/210167531-d461144a-c89b-4698-97c2-8ae1c3fe0033.PNG)


# A QUICK TASK FOR YOU!
```
1. Create a pull request to merge the latest code into the main branch
2. After merging the PR, go back into your terminal and switch into the main branch.
3. Pull the latest change.
4. Create a new branch, add more stages into the Jenkins file to simulate below phases. (Just add an echo command like we have in build
and test stages)
   1. Package 
   2. Deploy 
   3. Clean up
5. Verify in Blue Ocean that all the stages are working, then merge your feature branch to the main branch
6. Eventually, your main branch should have a successful pipeline like this in blue ocean
```

![6070](https://user-images.githubusercontent.com/85270361/210167585-4d1a0fcf-b484-432d-bf7d-81c6c519118d.PNG)
