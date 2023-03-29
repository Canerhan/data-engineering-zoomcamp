



# Problem description


# Execution of the Project

This folling parts will explain,   
how you can reproduce this project on your environment.  


## Prerequisites
---
### Local
---
1. **Terraform**  
Follow Instruction based on your local operating system.  
[Terraform install instruction](https://developer.hashicorp.com/terraform/downloads)  

<br>

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
Rename the file to "service_account_dc_project_2023.json" and  
save it to your home folder in  `$HOME/.google/`

<br>

#### Credentials Env Var  
Wenn have to set the path to the credentials json file and save it in a variable. 
export GOOGLE_APPLICATION_CREDENTIALS="<path/to/your/service-account-authkeys>.json".  
We will save it in the .bashrc file in the home folder.
1. Edit `.bashrc`:
    
---
### Cloud Environment
---
### VM Preparing

