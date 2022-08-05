# Introduction
The Northwind-DB-Load repository is a technical case to challenge a data engineer and test the essential requirements for a job opening. The objective of this challenge is to build a pipeline that extracts the data everyday from two sources and writes the data first to local disk, and second to a database.

# Dataset
The dataset is the same database called Northwind provided by Microsoft except for the order_details table which was removed and replaced with a csv file. Thus, the CSV file contains the order details.

# Steps
The specific objectives of this challenge are:
1. Write the data locally respecting the rules
2. Load the data from the local filesystem to the final database that you chose.
3. Write a SQL statement that queries the orders and its details. Then, export the result as a CSV file.

# Challenge requirements

- All writing steps must be isolated from each order to be able to run any step without executing all the code.
- The pipeline schedule is daily
- Extract all the tables from the source database.
- Provide clear instructions on how to run the whole pipeline.
- Provide a CSV or JSON file with the result of the final query.
- You don’t have to actually schedule the pipeline, but you should assume that it will run for different days.
- You should be able to pass an argument to the pipeline with a day from the past, and it should reprocess the data for that day.

# Repository organization
This section presents the repository's folders and files. The list of folders or files and its details are:

- **data** folder contains the two sources, northwind.sql and order_details.csv.
- **local_data** folder represents the local filesystem.
- **dags** folder gathers the airflow dags and tasks. These folders hold the following python codes:
  - step1_extract_from_pg extracts data from the Postgres database source.
  - step1_extract_from_csv extracts data from the CSV source.
  - step2_load_to_finaldb Load the data from the local system to another Postgres database
  - step3_query_orders queries the orders and their details and exports them as a csv file.
  - pipeline_dag sets the dependencies and the scheduled time.
- **docker-compose.yml** contains the images and setting necessary to run the code. The images are:
  - Postgres:12 - It's an object-relational database system. It's used as one of the sources and as the final database.
  - adminer - Database management. It was used as the DB interface to support the pipeline development
  - apache/airflow:2.3.3 - The platform to schedule, and monitor workflows.

# Resolution

## 1 - Write the data locally

It was instructed to write data to the local disk respecting the rule: one file for each table and one file for the CSV input per day. The step1_extract_from_pg.py and step1_extract_from_csv.py are the codes that write locally. 

The step1_extract_from_pg.py executes commands to: 
1. connect to Postgres; 
2. query the database's table names;
3. create a directory;
4. export data as a CSV file.

The step1_extract_from_csv.py it's similar to the code above. It executes commands to:
1. create the directory 
2. copy CSV into the local disk.

The directory pattern used to store the CSV files are:

```
/local_data/Postgres/{table}/{date}/{table}.csv
/local_data/csv/{date}/order_details.csv
```

## 2 - Load the data

After writing the data locally, it’s necessary to load the data from the local filesystem to the final database. The same Postgres was chosen as the final database.

The step2_load_to_finaldb.py executes the following commands to load the data into the Postgres final database:
1. connect to Postgres final database;
2. get the name of the tables;
3. initialize the database;
4. import CSVs into Postgres.

## 3 - Query orders and their details
Finally, the code must run a query that shows the orders and their details. 

The step3_query_orders.py executes the following commands do it.
1. connect to Postgres final database;
2. retrieve data;
3. print the query;
4. export it as a CSV file.

## 4 - Schedule and dependencies
It was used the Apache Airflow 2.3.3 to schedule and set dependencies of the pipeline. 
The graph below represents the pipeline dependencies and cuncurrencies

![pipeline-dag](https://user-images.githubusercontent.com/41583726/182637032-5df1e52d-5dea-42da-8995-2817366b6362.png)

The step 1 tasks depends on the step 2. Also, step 3 depends on step 2.

Finally, the schedule interval was set as @daily.



# How to run
Pre-requisites: 
- Docker 20.10.17
- Docker Compose 2.3.3

```
# clone repository
git clone https://github.com/leomakino/northwind-db-load

# Change directory to northwind-db-load
cd northwind-db-load

# Make directories
mkdir -p ./logs ./plugins

# Create .env if you are a linux user
echo -e "AIRFLOW_UID=$(id -u)" > .env

# Docker build
docker build . --tag extending_airflow:latest

# Initialize the database
docker compose up airflow-init

# Start all the services
docker compose up
```

# How to check the results
After setting up the containers, the next step is to get the results.
The first step is to trigger the airflow dag to run the code. 
Next, check if the data has been loaded into the final database and if the CSV file has been generated correctly.

## Airflow
Using the following bash code it is possible to check if:
- the DAG is sucessfully created;
- the dependencies between the tasks;
- the tasks executions;
- the schedule interval.

```
# Start a bash session on the airflow container
docker exec -it northwind-db-load-airflow-triggerer-1 bash

# List DAGs
airflow dags list

# Displays DAG's tasks with their dependencies
airflow dags show pipeline-dag

# If the pipeline-dag paused attribution is false
# Then Unpause the DAG
airflow dags unpause pipeline-dag

# Trigger the DAG
airflow dags trigger pipeline-dag

# List DAG runs given a DAG id
# Copy the execution_date
airflow dags list-runs -d pipeline-dag

# Get the status of a dag run
airflow dags state pipeline-dag {execution_date}

# Check the next execution
airflow dags next-execution pipeline-dag

# Exit the bash session
exit
```

## Postgres final database
Using the following bash code it is possible to check if:
- the database is created;
- the relations of the tables;
- the data in any table.

```
# Start a bash session on the postgres container
docker exec -ti northwind-db-load-final_db-1 bash

# Login
psql -U admin -d northwind_data_analysis

# List of databases
\l

# List of relations
\dt

# Query data
SELECT * FROM {table_name};

# Exit the northwind_data_analysis database
exit

# Exit the bash session
exit
```

## Exported csv
Using the following bash code it is possible to check if:
- the csv file is created;
- the data in the CSV file.
```
# At northwind-db-load, change directory to dags
cd dags/local_data

# Check the number of line and prints the first 10 lines of the exported file
wc -l order_and_details.csv && head order_and_details.csv

# Print the content of the file
cat order_and_details.csv
```

# Author
Leonardo Villela Makino https://www.linkedin.com/in/leonardo-makino-77a559185/
