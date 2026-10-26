# LOAD BALANCER ROLES

We want to be able to choose which Load Balancer to use, Nginx or Apache, so we need to have two roles respectively:

1. Nginx
2. Apache


With your experience on Ansible so far you can:

- Decide if you want to develop your own roles, or find available ones from the community
- Update both static-assignment and site.yml files to refer the roles


Important Hints:

- Since you cannot use both Nginx and Apache load balancer, you need to add a condition to enable either one – this is where you 
can make use of variables.

- Declare a variable in defaults/main.yml file inside the Nginx and Apache roles. Name each variables enable_nginx_lb and 
enable_apache_lb respectively.

- Set both values to false like this enable_nginx_lb: false and enable_apache_lb: false.

- Declare another variable in both roles load_balancer_is_required and set its value to false as well

- Update both assignment and site.yml files respectively

loadbalancers.yml file

```
- hosts: lb
  roles:
    - { role: nginx, when: enable_nginx_lb and load_balancer_is_required }
    - { role: apache, when: enable_apache_lb and load_balancer_is_required }
```

site.yml file


```
 - name: Loadbalancers assignment
       hosts: lb
         - import_playbook: ../static-assignments/loadbalancers.yml
        when: load_balancer_is_required 
```

Now you can make use of env-vars\uat.yml file to define which loadbalancer to use in UAT environment by setting respective 
environmental variable to true.

You will activate load balancer, and enable nginx by setting these in the respective environment’s env-vars file.


```
enable_nginx_lb: true
load_balancer_is_required: true
```


The same must work with apache LB, so you can switch it by setting respective environmental variable to true and other to false.

To test this, you can update inventory for each environment and run Ansible against each environment.

Congratulations!
You have learned and practiced how to use Ansible configuration management tool to prepare UAT environment for Tooling web solution.


Next project
Next project is a capstone project for this part of your Project Based Learning journey – it will require all previously gained knowledge and skills, and introduce more new and exciting concepts and DevOps tools!

Get ready for new challenges ahead! Full Speed Forward!
