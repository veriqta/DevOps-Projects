# CREATE A COMMON PLAYBOOK

Step 5 – Create a Common Playbook
It is time to start giving Ansible the instructions on what you needs to be performed on all servers listed in inventory/dev.

In common.yml playbook you will write configuration for repeatable, re-usable, and multi-machine tasks that is common to systems 
within the infrastructure.

Update your playbooks/common.yml file with following code:

```
---
- name: update web, nfs and db servers
  hosts: webservers, nfs, db
  remote_user: ec2-user
  become: yes
  become_user: root
  tasks:
    - name: ensure wireshark is at the latest version
      yum:
        name: wireshark
        state: latest

- name: update LB server
  hosts: lb
  remote_user: ubuntu
  become: yes
  become_user: root
  tasks:
    - name: Update apt repo
      apt: 
        update_cache: yes

    - name: ensure wireshark is at the latest version
      apt:
        name: wireshark
        state: latest
```



Examine the code above and try to make sense out of it. This playbook is divided into two parts, each of them is intended to 
perform the same task: install wireshark utility (or make sure it is updated to the latest version) on your RHEL 8 and Ubuntu 
servers. It uses root user to perform this task and respective package manager: yum for RHEL 8 and apt for Ubuntu.

Feel free to update this playbook with following tasks:

Feel free to update this playbook with following tasks:

- Create a directory and a file inside it
- Change timezone on all servers
- Run some shell script


For a better understanding of Ansible playbooks – watch this video from RedHat ( https://youtu.be/ZAdJ7CdN7DY ) and read this article
( https://www.redhat.com/en/topics/automation/what-is-an-ansible-playbook ).

Step 6 – Update GIT with the latest code
Now all of your directories and files live on your machine and you need to push changes made locally to GitHub.

In the real world, you will be working within a team of other DevOps engineers and developers. It is important to learn how to
collaborate with help of GIT. In many organisations there is a development rule that do not allow to deploy any code before it 
has been reviewed by an extra pair of eyes – it is also called "Four eyes principle".

Now you have a separate branch, you will need to know how to raise a Pull Request (PR), get your branch peer reviewed and merged to
the master branch.

Commit your code into GitHub:

1. use git commands to add, commit and push your branch to GitHub.

```
git status

git add <selected files>

git commit -m "commit message"
```


2. Create a Pull request (PR)

3. Wear a hat of another developer for a second, and act as a reviewer.

4. If the reviewer is happy with your new feature development, merge the code to the master branch.

5. Head back on your terminal, checkout from the feature branch into the master, and pull down the latest changes.

Once your code changes appear in master branch – Jenkins will do its job and save all the files (build artifacts) to 
/var/lib/jenkins/jobs/ansible/builds/<build_number>/archive/ directory on Jenkins-Ansible server.

