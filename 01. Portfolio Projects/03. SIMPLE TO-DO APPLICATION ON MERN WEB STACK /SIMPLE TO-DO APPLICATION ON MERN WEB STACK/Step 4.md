# MONGODB DATABASE

We need a database where we will store our data. For this we will make use of mLab. mLab provides MongoDB database as a service 
solution [(DBaaS)]https://en.wikipedia.org/wiki/Cloud_database(), so to make life easy, you will need to sign up for a shared clusters free account, which is ideal 
for our use case.
Sign up [here](https://www.mongodb.com/atlas-signup-from-mlab). Follow the sign up process, select AWS as the cloud provider, and choose a region near you.

Complete a get started checklist as shown on the image below

![5003](https://user-images.githubusercontent.com/85270361/210130940-3d8a93d0-d7e1-46d6-87bc-57deaa5ac417.PNG)


Allow access to the MongoDB database from anywhere (Not secure, but it is ideal for testing)

IMPORTANT NOTE
In the image below, make sure you change the time of deleting the entry from 6 Hours to 1 Week


![5004](https://user-images.githubusercontent.com/85270361/210130965-09bfdbb5-8ca1-46ad-bc10-37d0a8ac54db.PNG)


Create a MongoDB database and collection inside mLab


![5005](https://user-images.githubusercontent.com/85270361/210130999-ae626111-3e54-4273-a194-e447662f19e0.PNG)


In the index.js file, we specified process.env to access environment variables, but we have not yet created this file. So we need 
to do that now.

Create a file in your Todo directory and name it .env.

```
touch .env
vi .env
```

Add the connection string to access the database in it, just as below:

```
DB = 'mongodb+srv://<username>:<password>@<network-address>/<dbname>?retryWrites=true&w=majority'
```

Ensure to update <username>, <password>, <network-address> and <database> according to your setup

Here is how to get your connection string
  
![5006](https://user-images.githubusercontent.com/85270361/210131129-c22696a1-76bb-41cf-a6cf-5028c7ab6845.PNG)

  
![50007](https://user-images.githubusercontent.com/85270361/210131217-788a794c-8e51-49fa-8a00-35e7b8982e16.PNG)

  
 Now we need to update the index.js to reflect the use of .env so that Node.js can connect to the database.

Simply delete existing content in the file, and update it with the entire code below.

To do that using vim, follow below steps

1. Open the file with vim index.js
2. Press esc
3. Type :
4. Type %d
5. Hit ‘Enter’
  
The entire content will be deleted, then,

6. Press i to enter the insert mode in vim
7. Now, paste the entire code below in the file.
  

```
const express = require('express');
const bodyParser = require('body-parser');
const mongoose = require('mongoose');
const routes = require('./routes/api');
const path = require('path');
require('dotenv').config();

const app = express();

const port = process.env.PORT || 5000;

//connect to the database
mongoose.connect(process.env.DB, { useNewUrlParser: true, useUnifiedTopology: true })
.then(() => console.log(`Database connected successfully`))
.catch(err => console.log(err));

//since mongoose promise is depreciated, we overide it with node's promise
mongoose.Promise = global.Promise;

app.use((req, res, next) => {
res.header("Access-Control-Allow-Origin", "\*");
res.header("Access-Control-Allow-Headers", "Origin, X-Requested-With, Content-Type, Accept");
next();
});

app.use(bodyParser.json());

app.use('/api', routes);

app.use((err, req, res, next) => {
console.log(err);
next();
});

app.listen(port, () => {
console.log(`Server running on port ${port}`)
});
```

Using environment variables to store information is considered more secure and best practice to separate configuration and secret
data from the application, instead of writing connection strings directly inside the index.js application file.

Start your server using the command:
  
```
node index.js
```
  
 
You shall see a message ‘Database connected successfully’, if so – we have our backend configured. Now we are going to test it.

Testing Backend Code without Frontend using RESTful API
So far we have written backend part of our To-Do application, and configured a database, but we do not have a frontend UI yet. We 
need ReactJS code to achieve that. But during development, we will need a way to test our code using RESTfulL API. Therefore, we will
need to make use of some API development client to test our code.

In this project, we will use Postman to test our API.
Click Install Postman to download and install postman on your machine.

Click HERE to learn how perform CRUD operartions on Postman

You should test all the API endpoints and make sure they are working. For the endpoints that require body, you should send JSON 
back with the necessary fields since it’s what we setup in our code.

Now open your Postman, create a POST request to the API http://<PublicIP-or-PublicDNS>:5000/api/todos. This request sends a new task
to our To-Do list so the application could store it in the database.

Note: make sure your set header key Content-Type as application/json
 
 
![5008](https://user-images.githubusercontent.com/85270361/210131561-9316f8f5-2112-4f09-846a-544677328817.PNG)

Check the image below:
  
  
![5009](https://user-images.githubusercontent.com/85270361/210131585-627646c4-a59e-48c3-8edd-0354e4ac2431.PNG)


Create a GET request to your API on http://<PublicIP-or-PublicDNS>:5000/api/todos. This request retrieves all existing records from
out To-do application (backend requests these records from the database and sends it us back as a response to GET request).
  
  
![5010](https://user-images.githubusercontent.com/85270361/210131610-9c7c4544-1e2b-40f3-b2b6-bcd389857b0d.PNG)

  
Optional task: Try to figure out how to send a DELETE request to delete a task from out To-Do list.

Hint: To delete a task – you need to send its ID as a part of DELETE request.

By now you have tested backend part of our To-Do application and have made sure that it supports all three operations we wanted:

- Display a list of tasks – HTTP GET request
- Add a new task to the list – HTTP POST request
- Delete an existing task from the list – HTTP DELETE request
  
  
We have successfully created our Backend, now let go create the Frontend.
  
