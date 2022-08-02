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



# How to run

## Pre-requisites