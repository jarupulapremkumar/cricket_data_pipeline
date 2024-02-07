# Cricket Data Pipeline
This project is designed to scrape cricket data from the ESPNCricinfo website using Python's urllib package, perform data cleaning and preprocessing, and store the transformed data into different data sources such as MySQL databases and CSV files.

Steps
1. Web Scraping from ESPNCricinfo Website
The project utilizes the Python urllib package to scrape cricket data from the ESPNCricinfo website. By accessing specific web pages and parsing HTML content, the script extracts valuable cricket statistics and match details.

2. Data Transformation and Cleaning
Once the data is scraped, the project performs data transformation by extracting the required information and removing any unwanted data. This involves parsing HTML content, extracting relevant fields such as match scores, player statistics, match dates, and other pertinent details.

Data cleaning and preprocessing techniques are applied to ensure the accuracy and consistency of the extracted information. This may involve handling missing values, standardizing data formats, and removing duplicates or irrelevant data entries.

3. Storing Data to Different Data Sources
The transformed cricket data is stored in different data sources for further analysis and visualization. The project supports storing data in MySQL databases and CSV files, providing flexibility in data storage and retrieval.

MySQL Database: The cleaned and processed cricket data is stored in MySQL databases, allowing for efficient querying and retrieval of data for analytical purposes.

CSV Files: Additionally, the project offers the option to export the cleaned data to CSV files, enabling easy sharing and integration with other data analysis tools and platforms.

Usage
To use the Cricket Data Pipeline:

Clone the repository to your local machine.
Install the required Python dependencies.
Run the provided Python scripts main.py to scrape cricket data from ESPNCricinfo, perform data transformation and cleaning, and store the data in MySQL databases or CSV files.
Feel free to explore and modify the project according to your specific requirements and use cases. Happy analyzing!
