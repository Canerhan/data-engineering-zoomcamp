



# Problem description


# Execution of the Project

This folling parts will explain,   
how you can reproduce this project on your environment.  


## Prerequisites
---

### Cloud
---
 

#### Account  
   Create a Account, [Register here]( https://console.cloud.google.com/)

<br>

#### Project  
We will create a project with the name "DC-Project-2023" on the [GCloud Site](https://console.cloud.google.com/).  
On the top left you can click on the name of name  
of the current project and select "New Project" on the top right.

<br>

#### APIs  
Enabe the following APIs. The Project-Name on the top left must be "DC-Project-2023".   
* https://console.cloud.google.com/apis/library/iam.googleapis.com
* https://console.cloud.google.com/apis/library/iamcredentials.googleapis.com

<br>

#### Service Account
We will need a account for the communication with our  
Cloud environment. In GCloud open the menu on the left top.  
Choose "IAM & Admin". On the menu left select "Service accounts",  
click on "Create Service Account" and create a new account 
with the name "service_account_dc_project_2023".  
Add the following roles:  
Viewer, Storage Admin, Storage Object Admin,  BigQuery Admin

<br>

#### Service Account Key
We need the authorization key for the created service account.  
In the Mneu "Service Accounts" klick in the list on the name of the account,    
we created in the previous step. The go to the "KEYS" Tab, "Add Key"    
"Create new key". Choose Json and save the file.  
Rename the file to 'service_account_dc_project_2023.json' and    
save it to your home folder in  `$HOME/.google/`  

<br>

### Local
---



#### Credentials Env Var  
We have to set the path to the credentials json file and save it in a variable.  
export GOOGLE_APPLICATION_CREDENTIALS="<path/to/your/service-account-authkeys>.json".  
We will save it in the .bashrc file in the home folder.  
The following command will add `GOOGLE_APPLICATION_CREDENTIALS="$HOME/.google/service_account_dc_project_2023.json"`  
at the end of the .bashrc file.  
~~~sh
echo GOOGLE_APPLICATION_CREDENTIALS="$HOME/.google/service_account_dc_project_2023.json" >>  $HOME/.bashrc
~~~


#### Terraform


Terraform is an infrastructure as code tool that lets you build, change,   
and version cloud and on-prem resources safely and efficiently.  
With the help opf terraform, we will create the create the infrastructure  
we need on GCP for this project.  

We will create
   - GC Bucket
   - Big Query Dataset

First we need to install terraform on our local machine.  
Follow Instruction based on your local operating system.  
[Terraform install instruction](https://developer.hashicorp.com/terraform/downloads)  

<br>

#### GCloud SDK
We need the Google SDK for authentication when we use terraform  
https://cloud.google.com/sdk/docs/install-sdk

<br>

#### Create GCP Infrastructure

First we need to authorize:

~~~sh
gcloud auth application-default login
~~~

Open the link in the browser and copy and paste the 
authorization code.  

After that we initialize terraform,
we need to be in the ./week_7_myproject/_1_Prerequisites folder.
In the folder are the codes for the infratsructure, we want to create.  

~~~sh
terraform init

# First we plan and check changes to new infra plan
terraform plan -var="project=<your-gcp-project-id>"
# For our exapmple it is: 
terraform plan -var="project=dc-project-2023"

# Create new infra
terraform apply -var="project=<your-gcp-project-id>

terraform apply -var="project=dc-project-2023"

~~~


---
### Cloud Environment
---

We will execute everythin on the cloud environment.  
We have to prepare the VM. The best OS for this project is Linux.  


### VM Preparing

You can find a deatiled Video about setting up the cloud VM [here](https://www.youtube.com/watch?v=ae-CV2KfoN0&list=PL3MmuxUbc_hJed7dXYoJw8DoCuVHhGEQb).  

This things will be executed:

- Generating SSH keys
- Creating a virtual machine on GCP
- Connecting to the VM with SSH
- Installing Anaconda
- Installing Docker
- Creating SSH config file
- Accessing the remote machine with VS Code and SSH remote
- Installing docker-compose
- Installing pgcli
- Port-forwarding with VS code: connecting to pgAdmin and Jupyter from the local computer
- Installing Terraform
- Using sftp for putting the credentials to the remote machine
- Shutting down and removing the instance

### Repository

If you finished all the points in the previous step,  
the VM is ready to be used.  
Now you have to clone this repository into your homefolder