# CricScoreDigger 

This Python script allows users to scrape cricket scorecards from websites and extract various statistics including batting, bowling, total score, match details, and fall of wickets. It is designed to parse HTML content using BeautifulSoup and organize the extracted data into structured formats for analysis and display.

## Features

- **Data Scraping**: The script scrapes cricket statistics from the provided URL using BeautifulSoup, extracting information about the match, teams, venue, umpires, batting, bowling, total score, and fall of wickets.

- **Data Processing**: It processes the extracted data, converting it into structured formats such as Pandas DataFrames, making it suitable for analysis and visualization.

- **Flexibility**: Users can retrieve specific sets of statistics or display comprehensive information about the match based on their preferences. The script offers flexibility in retrieving and displaying data.

- **Error Handling**: Robust error handling ensures smooth execution even in the face of unexpected situations, providing informative error messages for invalid URLs or unexpected conditions.

## Steps

### 1. Web Scraping from ESPNCricinfo Website

The project utilizes the Python urllib package to scrape cricket data from the ESPNCricinfo website. By accessing specific web pages and parsing HTML content, the script extracts valuable cricket statistics and match details.

### 2. Data Transformation and Cleaning

Once the data is scraped, the project performs data transformation by extracting the required information and removing any unwanted data. This involves parsing HTML content, extracting relevant fields such as match scores, player statistics, match dates, and other pertinent details.

Data cleaning and preprocessing techniques are applied to ensure the accuracy and consistency of the extracted information. This may involve handling missing values, standardizing data formats, and removing duplicates or irrelevant data entries.

### 3. Storing Data to Different Data Sources

The transformed cricket data is stored in different data sources for further analysis and visualization. The project supports storing data in MySQL databases and CSV files, providing flexibility in data storage and retrieval.

- **MySQL Database**: The cleaned and processed cricket data is stored in MySQL databases, allowing for efficient querying and retrieval of data for analytical purposes.

- **CSV Files**: Additionally, the project offers the option to export the cleaned data to CSV files, enabling easy sharing and integration with other data analysis tools and platforms.

## Class Structure:

### ScoreCard class

The code is organized using a Python class called ScoreCard. Here's a brief overview of its structure:

#### Constructor (__init__):

- Initializes various data structures to store cricket statistics such as batting data, bowling data, match details, etc.

#### collect_stats Method:

- Scrapes cricket statistics from the provided URL using BeautifulSoup.
- Extracts information about the match, including teams, match date, venue, umpires, etc.
- Retrieves batting, bowling, total score, and fall of wickets data.

#### Data Extraction Methods:

- get_country_mapping: Extracts the country names from the scorecard.
- scores: Extracts batting and bowling statistics from the scorecard.
- match_details: Extracts match details such as venue, umpires, match format, etc.
- get_match_name_from_url: Extracts the match name from the URL.
- get_match_count_type: Parses a string to extract match count and match type information.

#### Data Processing Methods:

- batting_stats_to_dataframe: Converts batting statistics into a Pandas DataFrame.
- bowling_stats_to_dataframe: Converts bowling statistics into a Pandas DataFrame.
- match_details_to_df: Converts match details into a Pandas DataFrame.
- total_score_to_df: Converts total score data into a Pandas DataFrame.
- fall_of_wickets_to_df: Converts fall of wickets data into a Pandas DataFrame.

#### Data Retrieval Methods:

- get_batting_stats: Retrieves batting statistics as a DataFrame.
- get_bowling_stats: Retrieves bowling statistics as a DataFrame.
- get_match_details: Retrieves match details as a DataFrame.
- get_total_score: Retrieves total score data as a DataFrame.
- get_fall_of_wickets: Retrieves fall of wickets data as a DataFrame.
- get_playing_xii: Retrieves playing XI data as a dictionary or list.

#### Utility Methods:

- display_all_stats: Displays all collected statistics.
- get_stats: Retrieves statistics based on user preferences.
- get_player_of_the_match: Retrieves the player of the match.

#### Error Handling:

- Implements error handling to manage exceptions during the scraping process.
- Provides informative error messages for invalid URLs or unexpected situations.

### ScrapeDates Class

The `ScrapeDates` class is responsible for scraping cricket match statistics from ESPN Cricinfo for various date ranges.

#### Constructor (__init__)

The constructor initializes the class.

#### scrape_url Method

- This method initiates the scraping process by creating a `ScoreCard` object and calling its `collect_stats` method to scrape statistics from a given URL.
- It returns all the statistics obtained from the scraping process.

#### get_scraped_list Method

- Retrieves cricket match statistics for a list of dates provided as input.
- Iterates over each date and scrapes match statistics for that date.
- Returns a tuple containing a list of URLs scraped and a list of corresponding statistics dataframes.

#### scrape_daily Method

- Scrapes cricket match statistics for the current day.
- Fetches the current date and retrieves match statistics for that date.
- Calls `get_scraped_list` method to perform scraping and returns the obtained data.

#### scrape_date Method

- Scrapes cricket match statistics for a specified date range.
- Accepts start and end dates as input and retrieves match statistics for each date within the specified range.
- Calls `get_scraped_list` method to perform scraping and returns the obtained data.

#### scrape_current_month Method

- Scrapes cricket match statistics for the current month.
- Retrieves the current month and fetches match statistics for all dates within the current month.
- Calls `get_scraped_list` method to perform scraping and returns the obtained data.

#### scrape_month Method

- Scrapes cricket match statistics for a specified month range.
- Accepts start and end months as input and retrieves match statistics for all dates within the specified month range.
- Calls `get_scraped_list` method to perform scraping and returns the obtained data.

#### scrape_current_year Method

- Scrapes cricket match statistics for the current year.
- Retrieves the current year and fetches match statistics for all dates within the current year.
- Calls `get_scraped_list` method to perform scraping and returns the obtained data.

#### scrape_year Method

- Scrapes cricket match statistics for a specified year range.
- Accepts start and end years as input and retrieves match statistics for all dates within the specified year range.
- Calls `get_scraped_list` method to perform scraping and returns the obtained data.

### Explanation of Utility Functions

This section explains the utility functions used in the cricket statistics scraping application.

#### get_html_response Function

- This function fetches the HTML response from a given URL.
- It checks if the URL belongs to espncricinfo.com and appends the base URL if necessary.
- Returns the HTML response.

#### get_bs_object Function

- This function retrieves the BeautifulSoup object from a given URL.
- It calls the `get_html_response` function to fetch the HTML response.
- Returns the BeautifulSoup object.

#### save_df_to_csv Function

- Saves a DataFrame to a CSV file.
- Appends data to an existing file if it already exists.
- Parameters:
  - df (DataFrame): DataFrame to be saved.
  - file_name (str): Name of the CSV file.

#### save_df_to_json Function

- Saves a DataFrame to a JSON file.
- Appends data to an existing file if it already exists.
- Parameters:
  - df (DataFrame): DataFrame to be saved.
  - file_name (str): Name of the JSON file.

#### save_df_to_sql Function

- Saves a DataFrame to an SQL database.
- Appends data to an existing table if it already exists.
- Parameters:
  - df (DataFrame): DataFrame to be saved.
  - table_name (str): Name of the SQL table.
  - conn: Database connection object.
  - df_schema: Schema for the DataFrame.

#### search_links Function

- Searches for links related to a keyword using Google search.
- Retrieves links from the search results and filters them based on a regular expression pattern.
- Returns a list of links.

#### get_dates_between Function

- Generates dates between two given dates.
- Parameters:
  - start_date (str): Start date.
  - end_date (str): End date.
- Returns a list of dates.

#### get_urls_on_date Function

- Retrieves URLs for a given date from a specific URL.
- Extracts URLs from HTML content based on specified criteria.
- Returns a dictionary containing URLs for the given date.

#### check_url_exists Function

- Checks if a URL exists in a given checkpoint file.
- Reads the URL from the checkpoint file and compares it with the provided URL.
- Returns True if the URL exists, False otherwise.

#### save_scorecard Function

- Saves the scraped scorecard data to different formats (CSV, JSON, SQL).
- Handles saving of match details, batting, bowling, total score, and fall of wickets.
- Provides flexibility to specify file names and database connections.
- Handles errors during the saving process.

#### get_dates Function

- Generates dates based on given parameters such as start date, end date, start month, end month, start year, and end year.
- Supports various combinations of date ranges.
- Returns a list of dates.

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


## Workflow:

The collect_stats method serves as the main entry point, orchestrating the scraping process and coordinating data extraction from different parts of the scorecard.

Data is scraped and processed iteratively, with specific methods dedicated to extracting and formatting different types of cricket statistics.

The application provides flexibility by allowing users to retrieve specific sets of statistics or display comprehensive information about the match.

Robust error handling ensures that the application gracefully handles unexpected situations, providing a smooth user experience even in the face of challenges.


## Usage

1. **Initialization**: Instantiate the `ScoreCard` class.

2. **Data Collection**: Use the `collect_stats` method to scrape cricket statistics from the provided URL. The method orchestrates the scraping process and retrieves various statistics.

3. **Data Retrieval**: Access specific sets of statistics using dedicated methods such as `get_batting_stats`, `get_bowling_stats`, `get_match_details`, `get_total_score`, and `get_fall_of_wickets`.

4. **Display and Analysis**: Display collected statistics using the `display_all_stats` method or retrieve specific statistics based on user preferences using the `get_stats` method.

5. **Error Handling**: The script handles errors gracefully, providing informative error messages for invalid URLs or unexpected conditions during the scraping process.


To use the CricScoreDigger Pipeline:

1. Clone the repository to your local machine.
2. Install the required Python dependencies.
3. Run the provided Python scripts to scrape cricket data from ESPNCricinfo, perform data transformation and cleaning, and store the data in MySQL databases or CSV files.

Feel free to explore and modify the project according to your specific requirements and use cases. Happy analyzing!

## Extensibility

The codebase is designed to be extensible, allowing developers to add new features, improve existing functionalities, or adapt the scraper to handle different types of cricket scorecards or websites. Contributions are encouraged, and developers can follow the provided guidelines to contribute to the project's growth and improvement.

## Dependencies

- Python 3.x
- BeautifulSoup
- Pandas

## Contributions

Contributions to the project are welcome! Please follow the guidelines outlined in the CONTRIBUTING.md file to contribute to the development of the Cricket Scorecard Scraper.
