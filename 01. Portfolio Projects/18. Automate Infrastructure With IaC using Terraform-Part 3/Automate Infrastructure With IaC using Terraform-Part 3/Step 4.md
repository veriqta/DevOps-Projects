# COMPLETE THE TERRAFORM CONFIGURATION

Complete the rest of the codes yourself, the resulting configuration structure in your working directory may look like this:

```
└── PBL
    ├── modules
    |   ├── ALB
    |     ├── ... (module .tf files, e.g., main.tf, outputs.tf, variables.tf)     
    |   ├── EFS
    |     ├── ... (module .tf files) 
    |   ├── RDS
    |     ├── ... (module .tf files) 
    |   ├── autoscaling
    |     ├── ... (module .tf files) 
    |   ├── compute
    |     ├── ... (module .tf files) 
    |   ├── network
    |     ├── ... (module .tf files)
    |   ├── security
    |     ├── ... (module .tf files)
    ├── main.tf
    ├── backends.tf
    ├── providers.tf
    ├── data.tf
    ├── outputs.tf
    ├── terraform.tfvars
    └── variables.tf
```

Now, the code is much more well-structured and can be easily read, edited and reused by your DevOps team members.

BLOCKERS: Your website would not be available because the userdata scripts we added to the launch template does not contain the 
latest endpoints for EFS, ALB and RDS and also our AMI is not properly configured, so how do we fix this?

In project 19, you would see how to use packer to create AMIs, Terrafrom to create the infrastructure and Ansible to configure the
infrasrtucture.

We will also see how to use terraform cloud for our backends.


**Pro-tips:**

1. You can validate your codes before running terraform plan with terraform validate command. It will check if your code is 
syntactically valid and internally consistent.
2. In order to make your configuration files more readable and follow canonical format and style – use terraform fmt command. It will 
apply Terraform language style conventions and format your .tf files in accordance to them.


**Congratulations**
You have done a great job developing and refactoring AWS Infrastructure as Code with Terraform!
