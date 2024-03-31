# API-Users
API REST developed with Django to manage users

## Installation proccess
1) Clone this repository in your PC
2) Go to the root folder of the project (/API-Users)
3) Execute docker compose up (you will need to have Docker installed)
4) At this point, the API will be listen at port 8001 and the PostgreDB server at port 5432.

## Restoring database
1) Go to the root folder of the project (/API-Users)
2) Execute docker exec -i -t postgreDb_users /bin/bash in order to open database server terminal.
3) Inside this terminal execute:
   
   -  psql -U admin -d db -f ./dump-files/dump.sql
   -  exit

## Use
Go to http://localhost:8001/api/ in order to see the different endpoints of the API
