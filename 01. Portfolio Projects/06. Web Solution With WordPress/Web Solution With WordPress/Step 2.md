# UPDATE THE `/ETC/FSTAB` FILE

The UUID of the device will be used to update the /etc/fstab file;

```
sudo blkid
```

![5030](https://user-images.githubusercontent.com/85270361/210138145-4da8745a-86be-4110-8abd-ee7d6363ba33.PNG)

```
sudo vi /etc/fstab
```

Update /etc/fstab in this format using your own UUID and rememeber to remove the leading and ending quotes.

![5031](https://user-images.githubusercontent.com/85270361/210138190-36d404db-1ad5-4dbb-ad02-c1adfa865e0a.PNG)


1. Test the configuration and reload the daemon

```
sudo mount -a
sudo systemctl daemon-reload
```

2. Verify your setup by running df -h, output must look like this:

![5032](https://user-images.githubusercontent.com/85270361/210138253-28ab8647-88be-4b59-9bad-c981014cdc4b.PNG)


Step 2 — Prepare the Database Server
Launch a second RedHat EC2 instance that will have a role – ‘DB Server’
Repeat the same steps as for the Web Server, but instead of apps-lv create db-lv and mount it to /db directory instead of
/var/www/html/.

Step 3 — Install WordPress on your Web Server EC2


1. Update the repository

```
sudo yum -y update
```


2. Install wget, Apache and it’s dependencies

```
sudo yum -y install wget httpd php php-mysqlnd php-fpm php-json
```


3. Start Apache

```
sudo systemctl enable httpd
sudo systemctl start httpd
```


4. To install PHP and it’s depemdencies

```
sudo yum install https://dl.fedoraproject.org/pub/epel/epel-release-latest-8.noarch.rpm
sudo yum install yum-utils http://rpms.remirepo.net/enterprise/remi-release-8.rpm
sudo yum module list php
sudo yum module reset php
sudo yum module enable php:remi-7.4
sudo yum install php php-opcache php-gd php-curl php-mysqlnd
sudo systemctl start php-fpm
sudo systemctl enable php-fpm
setsebool -P httpd_execmem 1
```

5. Restart Apache

```
sudo systemctl restart httpd
```

6. Download wordpress and copy wordpress to var/www/html

```
  mkdir wordpress
  cd   wordpress
  sudo wget http://wordpress.org/latest.tar.gz
  sudo tar xzvf latest.tar.gz
  sudo rm -rf latest.tar.gz
  cp wordpress/wp-config-sample.php wordpress/wp-config.php
  cp -R wordpress /var/www/html/
```


7. Configure SELinux Policies

```
sudo chown -R apache:apache /var/www/html/wordpress
sudo chcon -t httpd_sys_rw_content_t /var/www/html/wordpress -R
sudo setsebool -P httpd_can_network_connect=1
```

Step 4 — Install MySQL on your DB Server EC2

```
sudo yum update
sudo yum install mysql-server
```

Verify that the service is up and running by using sudo systemctl status mysqld, if it is not running, restart the service and 
enable it so it will be running even after reboot:

```
sudo systemctl restart mysqld
sudo systemctl enable mysqld
```

Step 5 — Configure DB to work with WordPress

```
sudo mysql
CREATE DATABASE wordpress;
CREATE USER `myuser`@`<Web-Server-Private-IP-Address>` IDENTIFIED BY 'mypass';
GRANT ALL ON wordpress.* TO 'myuser'@'<Web-Server-Private-IP-Address>';
FLUSH PRIVILEGES;
SHOW DATABASES;
exit
```

Step 6 — Configure WordPress to connect to remote database.
Hint: Do not forget to open MySQL port 3306 on DB Server EC2. For extra security, you shall allow access to the DB server ONLY 
from your Web Server’s IP address, so in the Inbound Rule configuration specify source as /32

![5034](https://user-images.githubusercontent.com/85270361/210138507-0b3b6372-958b-406a-9672-82f729d26b85.PNG)


1. Install MySQL client and test that you can connect from your Web Server to your DB server by using mysql-client

```
sudo yum install mysql
sudo mysql -u admin -p -h <DB-Server-Private-IP-address>
```

2. Verify if you can successfully execute SHOW DATABASES; command and see a list of existing databases.

3. Change permissions and configuration so Apache could use WordPress:

4. Enable TCP port 80 in Inbound Rules configuration for your Web Server EC2 (enable from everywhere 0.0.0.0/0 or from your 
workstation’s IP)

5. Try to access from your browser the link to your WordPress 

http://<Web-Server-Public-IP-Address>/wordpress/
  
![5040](https://user-images.githubusercontent.com/85270361/210138663-27322aaf-f020-4261-a695-a98dc5f2387c.PNG)

  
Fill out your DB credentials:
  
![5050](https://user-images.githubusercontent.com/85270361/210138669-88078473-e459-4864-856f-4e6cb3d457d6.PNG)


If you see this message – it means your WordPress has successfully connected to your remote MySQL database
  

![5060](https://user-images.githubusercontent.com/85270361/210138718-d9c15bc9-f5b0-45f8-b613-11882374bf63.PNG)

  
Important: Do not forget to STOP your EC2 instances after completion of the project to avoid extra costs.

CONGRATULATIONS!
You have learned how to configure Linux storage susbystem and have also deployed a full-scale Web Solution using WordPress CMS and
MySQL RDBMS!
  

![5070](https://user-images.githubusercontent.com/85270361/210138753-775e4c79-c634-473a-9330-254b209347d1.PNG)
