# REFERENCE WEBSERVER ROLE

Step 4 – Reference ‘Webserver’ role

Within the static-assignments folder, create a new assignment for uat-webservers uat-webservers.yml. This is where you will reference
the role.

```
---
- hosts: uat-webservers
  roles:
     - webserver
```


Remember that the entry point to our ansible configuration is the site.yml file. Therefore, you need to refer your uat-webservers.yml 
role inside site.yml.

So, we should have this in site.yml


```
---
- hosts: all
- import_playbook: ../static-assignments/common.yml

- hosts: uat-webservers
- import_playbook: ../static-assignments/uat-webservers.yml
```

Step 5 – Commit & Test
Commit your changes, create a Pull Request and merge them to master branch, make sure webhook triggered two consequent Jenkins jobs,
they ran successfully and copied all the files to your Jenkins-Ansible server into /home/ubuntu/ansible-config-mgt/ directory.

Now run the playbook against your uat inventory and see what happens:

```
sudo ansible-playbook -i /home/ubuntu/ansible-config-mgt/inventory/uat.yml /home/ubuntu/ansible-config-mgt/playbooks/site.yaml
```


You should be able to see both of your UAT Web servers configured and you can try to reach them from your browser:

http://<Web1-UAT-Server-Public-IP-or-Public-DNS-Name>/index.php

or

http://<Web1-UAT-Server-Public-IP-or-Public-DNS-Name>/index.php

Your Ansible architecture now looks like this:
  
  
![6043](https://user-images.githubusercontent.com/85270361/210155433-92f8eac4-d31f-4cbe-af16-16dd70b2a498.PNG)

  
In Project 13, you will see the difference between Static and Dynamic assignments.

Congratulations!
You have learned how to deploy and configure UAT Web Servers using Ansible imports and roles!
