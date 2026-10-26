# STEP 5 – TESTING PHP WITH NGINX

Your LEMP stack should now be completely set up.

At this point, your LAMP stack is completely installed and fully operational.

You can test it to validate that Nginx can correctly hand .php files off to your PHP processor.

You can do this by creating a test PHP file in your document root. Open a new file called info.php within your document root in your 
text editor:

```
sudo nano /var/www/projectLEMP/info.php
```

Type or paste the following lines into the new file. This is valid PHP code that will return information about your server:


```
<?php
phpinfo();
```

You can now access this page in your web browser by visiting the domain name or public IP address you’ve set up in your Nginx 
configuration file, followed by /info.php:

```
http://`server_domain_or_IP`/info.php
```

You will see a web page containing detailed information about your server:

![projject1-step5](https://user-images.githubusercontent.com/85270361/210117729-d93d8aad-b131-40c2-b28d-ca0289327906.PNG)


After checking the relevant information about your PHP server through that page, it’s best to remove the file you created as it 
contains sensitive information about your PHP environment and your Ubuntu server. You can use rm to remove that file:

```
sudo rm /var/www/your_domain/info.php
```

You can always regenerate this file if you need it later.
