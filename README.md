# OCP12 : Epic Events

Projet OpenClassrooms - Programme développeur d'applications Python

**Objectif** : CLI based CRM app for event management.

## Functions
- Login
- CRUD management for : clients, contracts, events, employees
- JWT token authentication
- Permission management

## Installing and running

### 1. Install Software requirements
- Install Python 3.11+

### 2. Create Python project environment
1. In your terminal/IDLE, position yourself in the directory where you want
to create your project folder
```shell
$ cd //path//
```

2. Create your project folder 
```shell
$ mkdir <Project_folder_Name>
```

3. Clone the github repository to the projetct folder
```bash
git clone <git_hub_repository> <project_folder_name>
```

4. Create your project environment 
```shell
$ python -m venv env
```

5. Create .ssh folder
```shell
mkdir .ssh
```

### 3. Activate virtual environment
- From your project folder (this commande may change depending on your OS):
```shell
$ ./env/Scripts/activate
```

### 4. Install Pyhton packages
- From your terminal or IDLE, install all packages listed in requirements.txt
```shell
$ pip install -r requirements.txt
```

### 5. Create MySQL Database
#### Prerequisite
Having installed DBMS MySQL on the system

- Open MySQL Command Line Client
- Use database creation command : 
```sql
CREATE DATABASE epic_events
```
- Create database user:
```sql
CREATE USER 'new_user'@'localhost' IDENTIFIED BY 'password';
```
*new_user* is the name we’ve given to our new user account and the IDENTIFIED BY *‘password’* section sets a 
passcode for this user. You can replace these values with your own, inside the quotation marks.
- Gran privileges on the newly created database :
```sql
GRANT ALL PRIVILEGES ON * . * TO 'new_user'@'localhost';
FLUSH PRIVILEGES;
```
- create database connexion file :
  - Get into .ssh folder :
  `cd .ssh`
  - Create db_connexion.txt file : `touch db_connexion.txt`
  - Write in the file the following text :
```text
mysql+mysqlconnector://<new_user>:<password>@localhost/epic_events
```

### 6. Create encryption secret file
In the .ssh folder :
```shell
touch secret.txt
```
- Inside the file, write a secret to be used by the encrypting library

### 7.  Create sentry dsn file
In the .ssh folder :
```shell
touch sentry_dns.txt
```
- Inside the file, paste de dsn url provided by sentry services.

### 8. Launch login
- From your terminal or IDLE, from the epicevents folder :
```shell
python cli.py login
```

### 9. Launch CRM
- From your terminal or IDLE, from the epicevents folder :
```shell
python cli.py start
```

## Test Data

### Users
| username    | Password     |
|-------------|--------------|
| gestion1    | password     |
| commercial1 | password     |
| support1    | password     |
| commercial2 | password     |
| gestion2    | password     |
| support2    | password     |

### Database
Test data initialised with `tests/test_data.sql`



