# RUNNING ANSIBLE PLAYBOOK FROM JENKINS

Now that you have a broad overview of a typical Jenkins pipeline. Let us get the actual Ansible deployment to work by:

1. Installing Ansible on Jenkins
2. Installing Ansible plugin in Jenkins UI
3. Creating Jenkinsfile from scratch. (Delete all you currently have in there and start all over to get Ansible to run successfully)

You can [watch a 10 minutes video here](https://youtu.be/PRpEbFZi7nI) to guide you through the entire setup

Note: Ensure that Ansible runs against the Dev environment successfully.

Possible errors to watch out for:

1. Ensure that the git module in Jenkinsfile is checking out SCM to main branch instead of master (GitHub has discontinued the use of
Master due to Black Lives Matter. You can read more here)

2. Jenkins needs to export the ANSIBLE_CONFIG environment variable. You can put the .ansible.cfg file alongside Jenkinsfile in the
deploy directory. This way, anyone can easily identify that everything in there relates to deployment. Then, using the Pipeline
Syntax tool in Ansible, generate the syntax to create environment variables to set.

https://wiki.jenkins.io/display/JENKINS/Building+a+software+project


![6071](https://user-images.githubusercontent.com/85270361/210167751-0d654ed1-893b-4758-9c3b-3b3551661bcd.PNG)


Possible issues to watch out for when you implement this

1. Remember that ansible.cfg must be exported to environment variable so that Ansible knows where to find Roles. But because you will
possibly run Jenkins from different git branches, the location of Ansible roles will change. Therefore, you must handle this 
dynamically. You can use Linux [Stream Editor sed](https://www.gnu.org/software/sed/manual/sed.html) to update the section 
roles_path each time there is an execution. You may not have this issue if you run only from the main branch.

2. If you push new changes to Git so that Jenkins failure can be fixed. You might observe that your change may sometimes have no effect.
Even though your change is the actual fix required. This can be because Jenkins did not download the latest code from GitHub. Ensure
that you start the Jenkinsfile with a clean up step to always delete the previous workspace before running a new one. Sometimes 
you might need to login to the Jenkins Linux server to verify the files in the workspace to confirm that what you are actually 
expecting is there. Otherwise, you can spend hours trying to figure out why Jenkins is still failing, when you have pushed up 
possible changes to fix the error.

3. Another possible reason for Jenkins failure sometimes, is because you have indicated in the Jenkinsfile to check out the main git
branch, and you are running a pipeline from another branch. So, always verify by logging onto the Jenkins box to check the workspace,
and run git branch command to confirm that the branch you are expecting is there.


If everything goes well for you, it means, the Dev environment has an up-to-date configuration. But what if we need to deploy to
other environments?

- Are we going to manually update the Jenkinsfile to point inventory to those environments? such as sit, uat, pentest, etc.
- Or do we need a dedicated git branch for each environment, and have the inventory part hard coded there.

Think about those for a minute and try to work out which one sounds more like a better solution.

Manually updating the Jenkinsfile is definitely not an option. And that should be obvious to you at this point. Because we try to
automate things as much as possible.

Well, unfortunately, we will not be doing any of the highlighted options. What we will be doing is to parameterise the deployment. 
So that at the point of execution, the appropriate values are applied.


## Parameterizing Jenkinsfile For Ansible Deployment

To deploy to other environments, we will need to use parameters.

1. Update sit inventory with new servers


```
[tooling]
<SIT-Tooling-Web-Server-Private-IP-Address>

[todo]
<SIT-Todo-Web-Server-Private-IP-Address>

[nginx]
<SIT-Nginx-Private-IP-Address>

[db:vars]
ansible_user=ec2-user
ansible_python_interpreter=/usr/bin/python

[db]
<SIT-DB-Server-Private-IP-Address>
```

2. Update Jenkinsfile to introduce parameterization. Below is just one parameter. It has a default value in case if no value is 
specified at execution. It also has a description so that everyone is aware of its purpose.

```
pipeline {
    agent any

    parameters {
      string(name: 'inventory', defaultValue: 'dev',  description: 'This is the inventory file for the environment to deploy 
      configuration')
    }
...
```


3. In the Ansible execution section, remove the hardcoded inventory/dev and replace with `${inventory}
From now on, each time you hit on execute, it will expect an input.


![6072](https://user-images.githubusercontent.com/85270361/210167987-8db77bd8-2a78-4cfc-93a1-00006ab00fa7.PNG)


## Notice that the default value loads up, but we can now specify which environment we want to deploy the configuration to. Simply type
sit and hit Run

![6073](https://user-images.githubusercontent.com/85270361/210168032-0cdcb670-d96d-4d4b-937b-8341fee2ec5f.PNG)


4. Add another parameter. This time, introduce tagging in Ansible. You can limit the Ansible execution to a specific role or playbook
desired. Therefore, add an Ansible tag to run against webserver only. Test this locally first to get the experience. Once you 
understand this, update Jenkinsfile and run it from Jenkins.
