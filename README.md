# Cricket Data Pipeline

This project is designed to scrape cricket data from the ESPNCricinfo website using Python's urllib package, perform data cleaning and preprocessing, and store the transformed data into different data sources such as MySQL databases and CSV files.

## Steps

### 1. Web Scraping from ESPNCricinfo Website

The project utilizes the Python urllib package to scrape cricket data from the ESPNCricinfo website. By accessing specific web pages and parsing HTML content, the script extracts valuable cricket statistics and match details.

### 2. Data Transformation and Cleaning

Once the data is scraped, the project performs data transformation by extracting the required information and removing any unwanted data. This involves parsing HTML content, extracting relevant fields such as match scores, player statistics, match dates, and other pertinent details.

Data cleaning and preprocessing techniques are applied to ensure the accuracy and consistency of the extracted information. This may involve handling missing values, standardizing data formats, and removing duplicates or irrelevant data entries.

### 3. Storing Data to Different Data Sources

The transformed cricket data is stored in different data sources for further analysis and visualization. The project supports storing data in MySQL databases and CSV files, providing flexibility in data storage and retrieval.

- **SQL Database**: The cleaned and processed cricket data is stored in MySQL databases, allowing for efficient querying and retrieval of data for analytical purposes.

- **CSV Files**: Additionally, the project offers the option to export the cleaned data to CSV files, enabling easy sharing and integration with other data analysis tools and platforms.

## SQLAlchemy URL Formats for SQL Databases

This details the URL formats used to connect to various SQL databases using SQLAlchemy. Each section describes the specific format, provides additional context, and explains how to replace placeholders with your actual credentials.

### Introduction

SQLAlchemy is a versatile object-relational mapper (ORM) that simplifies interacting with SQL databases in Python. One key step in using SQLAlchemy is establishing a connection to your database. This document serves as a reference for the different URL formats you can use based on the specific type of SQL database you're working with.

### Connecting to Different Databases

Remember to replace the placeholders in each URL format with your actual credentials and connection information.

#### MySQL

**URL Format:**

Use code with caution. Learn more
`mysql://username:password@hostname:port/database`


**Description:**

* `username`: Your MySQL username.
* `password`: Your MySQL password.
* `hostname`: The hostname or IP address of your MySQL server.
* `port`: The port number of your MySQL server (default: 3306).
* `database`: The name of the MySQL database you want to connect to.

#### PostgreSQL

**URL Format:**

`postgresql://username:password@hostname:port/database`


**Description:**

* `username`: Your PostgreSQL username.
* `password`: Your PostgreSQL password.
* `hostname`: The hostname or IP address of your PostgreSQL server.
* `port`: The port number of your PostgreSQL server (default: 5432).
* `database`: The name of the PostgreSQL database you want to connect to.

#### SQLite

**URL Format:**

`sqlite:///absolute/path/to/database/file.db`

Description:

/absolute/path/to/database/file.db: Replace with the actual path to your SQLite database file.
Context:

SQLite databases are stored as individual files, so the URL format simply points to the location of that file on your system.

SQL Server
URL Format:

`mssql+pyodbc://username:password@hostname:port/database?driver=SQL+Server`


**Description:**

* `username`: Your SQL Server username.
* `password`: Your SQL Server password.
* `hostname`: The hostname or IP address of your SQL Server.
* `port`: The port number of your SQL Server (default: 1433).
* `database`: The name of the SQL Server database you want to connect to.

**Note:** This format requires the `pyodbc` driver to be installed.

#### Oracle

**URL Format:**

`oracle+cx_oracle://username:password@hostname:port/?service_name=database`


**Description:**

* `username`: Your Oracle username.
* `password`: Your Oracle password.
* `hostname`: The hostname or IP address of your Oracle server.
* `port`: The port number of your Oracle listener (default: 1521).
* `database`: The service name of the Oracle database you want to connect to.

**Note:** This format requires the `cx_oracle` driver to be installed.

#### ClickHouse

**URL Format:**

`clickhouse://username:password@hostname:port/database`

Description:

username: Your ClickHouse username (optional).
password: Your ClickHouse password (optional).
hostname: The hostname or IP address of your ClickHouse server.
port: The port number of your ClickHouse server (default: 9000).
database: The name of the ClickHouse database you want to connect to.


## Code Flow for scorecard class 
#### Score Scrapper class `Scorecard`

`Initialization`: The class initializes various lists and dictionaries to store cricket statistics such as batting data, bowling data, match details, player of the match, etc.

`collect_stats`: This method is the main function responsible for scraping data from the provided URL. It uses Beautiful Soup to parse the HTML content of the scorecard webpage. It collects information about the match, batting scores, bowling scores, etc., and stores them in the respective lists and dictionaries.

`get_country_mapping`: This method extracts the mapping of countries from the scorecard.

`scores`: This method extracts batting and bowling statistics from the scorecard.

`get_match_name_from_url`: This method extracts the match name from the URL.

`batting_stats_to_dataframe`: Converts batting stats into a DataFrame.

`bowling_stats_to_dataframe`: Converts bowling stats into a DataFrame.

`get_batting_stats`: Returns batting stats as a DataFrame.

`get_bowling_stats`: Returns bowling stats as a DataFrame.

`match_details`: Extracts match details from the scorecard HTML.

`get_match_count_type`: Parses a string to extract match count and match type information.

`match_details_to_df`: Converts match details dictionary to a DataFrame.

`total_score_to_df`: Converts total score data into a DataFrame.

`fall_of_wickets_to_df`: Converts fall of wickets data into a DataFrame.

`get_fall_of_wickets`: Returns fall of wickets data as a DataFrame.

`get_playing_xii`: Returns the playing XI for a given country.

`display_all_stats`: Displays all the collected statistics.

`get_stats`: Returns all the collected statistics.

`get_player_of_the_match`: Returns the player of the match.


## Usage

To use the Cricket Data Pipeline:

1. Clone the repository to your local machine.
2. Install the required Python dependencies.
3. Run the provided Python scripts to scrape cricket data from ESPNCricinfo, perform data transformation and cleaning, and store the data in MySQL databases or CSV files.

Feel free to explore and modify the project according to your specific requirements and use cases. Happy analyzing!
