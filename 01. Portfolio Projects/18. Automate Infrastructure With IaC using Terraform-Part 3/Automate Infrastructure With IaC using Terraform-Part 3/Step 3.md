# REFACTOR YOUR PROJECT USING MODULES

Let us review the [repository](https://github.com/darey-devops/PBL-project-17) from project 17, you will notice that we had a single 
list of long file for creating all of our resources, but that is not the best way to go about it because it makes our code base very 
hard to read and understand therefore making future changes can be quite stressful.

QUICK TASK FOR YOU: Break down your Terraform codes to have all resources in their respective modules. Combine resources of a similar
type into directories within a ‘modules’ directory, for example, like this:

```
- modules
  - ALB: For Apllication Load balancer and similar resources
  - EFS: For Elastic file system resources
  - RDS: For Databases resources
  - Autoscaling: For Autosacling and launch template resources
  - compute: For EC2 and rlated resources
  - VPC: For VPC and netowrking resources such as subnets, roles, e.t.c.
  - security: for creating security group resources
```


Each module shall contain following files:

```
- main.tf (or %resource_name%.tf) file(s) with resources blocks
- outputs.tf (optional, if you need to refer outputs from any of these resources in your root module)
- variables.tf (as we learned before - it is a good practice not to hard code the values and use variables)
```

It is also recommended to configure providers and backends sections in separate files but should be placed in the root module.

After you have given it a try, you can check out this [repository](https://github.com/darey-devops/PBL-project-18) 
for guidiance and erors fixing.

IMPORTANT: In the configuration sample from the repository, you can observe two examples of referencing the module:

a. Import module as a source and have access to its variables via var keyword:

```
module "VPC" {
  source = "./modules/VPC"
  region = var.region
  ...
```


b. Refer to a module’s output by specifying the full path to the output variable by using module.%module_name%.%output_name% 
construction:


```
subnets-compute = module.network.public_subnets-1
```

