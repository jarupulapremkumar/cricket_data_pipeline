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

- **MySQL Database**: The cleaned and processed cricket data is stored in MySQL databases, allowing for efficient querying and retrieval of data for analytical purposes.

- **CSV Files**: Additionally, the project offers the option to export the cleaned data to CSV files, enabling easy sharing and integration with other data analysis tools and platforms.

## Code Flow for scorecard class 
1. **`__init__(self, url)`**: 
   - Initializes the `ScoreCard` object with a URL.
   - Sets up attributes for storing batting and bowling data, player of the match, total score, etc.
   - Calls the `collect_stats` method to gather data from the provided URL.

2. **`get_html_response(self, url)`**:
   - Fetches the HTML response from the given URL using `urllib.request.urlopen`.
   - Handles exceptions that may occur during the HTTP request.

3. **`get_bs_object(self, url)`**:
   - Creates a BeautifulSoup object from the HTML response obtained from the URL.
   - Parses the HTML content using `BeautifulSoup`.

4. **`collect_stats(self, url)`**:
   - Gathers statistics from the cricket scorecard webpage.
   - Extracts the player of the match, country names, and calls other methods to fetch batting and bowling statistics.

5. **`batting_stats(self, url, scorecard, scorecard_id)`**:
   - Extracts batting statistics from the scorecard.
   - Iterates through the batting table, retrieves headers and data, and appends them to the `batting_data` attribute.
   - Collects fall of wickets data.

6. **`bowling_stats(self, url, scorecard, scorecard_id)`**:
   - Extracts bowling statistics from the scorecard.
   - Iterates through the bowling table, retrieves headers and data, and appends them to the `bowling_data` attribute.

7. **`get_match_name_from_url(self, link)`**:
   - Extracts the match name from the URL.
   - Parses the URL to determine the match name based on certain patterns.

8. **`batting_stats_to_dataframe(self, header, data)`**:
   - Converts batting statistics data into a pandas DataFrame.
   - Ensures proper data types for each column.

9. **`bowling_stats_to_dataframe(self, header, data)`**:
   - Converts bowling statistics data into a pandas DataFrame.
   - Ensures proper data types for each column.

10. **`get_batting_stats(self)`**:
    - Retrieves the batting statistics as a DataFrame.
    - Calls `batting_stats_to_dataframe` if there are header and data available.


## Usage

To use the Cricket Data Pipeline:

1. Clone the repository to your local machine.
2. Install the required Python dependencies.
3. Run the provided Python scripts to scrape cricket data from ESPNCricinfo, perform data transformation and cleaning, and store the data in MySQL databases or CSV files.

Feel free to explore and modify the project according to your specific requirements and use cases. Happy analyzing!
