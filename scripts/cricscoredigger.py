from scorecard import ScoreCard
from scrapdates import ScrapeDates
import utils
import os

import logging
logging.basicConfig()
logging.getLogger('sqlalchemy.engine').setLevel(logging.INFO)

class CricScoreDigger():
    # Initialize the class
    def __init__(self):
        # Initialize instances of ScoreCard and ScrapeDates classes
        self.sc = ScoreCard()
        self.sd = ScrapeDates()
        # Create directories for datasets and checkpoints if they do not exist
        os.makedirs("datasets", exist_ok=True)
        os.makedirs("checkpoints", exist_ok=True)

    def scrape_keyword(self, keyword:str):
        """
        Scrape data based on a keyword search.

        Args:
        - keyword (str): The keyword to search for.

        Returns:
        - dfs_tuple_list (list): List of tuples containing scraped data.
        """
        # Initialize an empty list to store tuples of dataframes
        dfs_tuple_list = []
        # Search for links related to the given keyword
        all_links = utils.search_links(keyword)
        # Iterate through the links
        for link in all_links:
            # Check if the keyword is in the link
            if keyword in link:
                # Append the scraped data to the list
                dfs_tuple_list.append(self.scraping_url(link))

        return dfs_tuple_list
    
    def scrape_date(self, start_date, end_date):
        """
        Scrape data within a specific date range.

        Args:
        - start_date (str): Start date of the range.
        - end_date (str): End date of the range.

        Returns:
        - Tuple containing scraped data.
        """
        return self.sd.scrape_date(start_date, end_date)
    
    def start_scrap_daily(self):
        """
        Start scraping data for the current day.

        Returns:
        - Tuple containing scraped data.
        """
        return self.sd.scrape_daily()

    def scrape_current_month(self):
        """
        Scrape data for the current month.

        Returns:
        - Tuple containing scraped data.
        """
        return self.sd.scrape_current_month()

    def scrape_month(self, start_month, end_month):
        """
        Scrape data within a specific month range.

        Args:
        - start_month (int): Start month of the range.
        - end_month (int): End month of the range.

        Returns:
        - Tuple containing scraped data.
        """
        return self.sd.scrape_month(start_month, end_month)

    def scrape_current_year(self):
        """
        Scrape data for the current year.

        Returns:
        - Tuple containing scraped data.
        """
        return self.sd.scrape_current_year()

    def scrape_year(self, start_year, end_year):
        """
        Scrape data within a specific year range.

        Args:
        - start_year (int): Start year of the range.
        - end_year (int): End year of the range.

        Returns:
        - Tuple containing scraped data.
        """
        return self.sd.scrape_year(start_year, end_year)

    def scrape_url(self, url):
        """
        Scrape data from a specific URL.

        Args:
        - url (str): The URL to scrape data from.

        Returns:
        - Scraped data.
        """
        return self.scrape_url(url)
    
    def save_scorecard_checked(self, url_list: list, dfs_tuple_list: list, method: str, fnames: dict = None, conn=None):
        """
        Save the scraped scorecard to files with checks last url saved.it will stop if that url matches current url else saves the data

        Args:
        - url_list (list): List of URLs.
        - dfs_tuple_list (list): List of tuples containing scraped data.
        - method (str): Method to save the data (e.g., 'csv', 'json', 'sql').
        - fnames (dict): Dictionary containing file names for different types of data.
        - conn: Database connection object.

        Returns:
        - None
        """
        # Check if the method is 'csv'
        if method == 'csv':
            # Check if the URL exists and save the data accordingly
            if not utils.check_url_exists(url_list[-1],'save_csv.txt'):
                for url, dfs_tuple in zip(url_list, dfs_tuple_list):
                    utils.save_scorecard(url, dfs_tuple, method, fnames, conn)
            else:
                print("Not Saving as last saved url is reached") 
        # Check if the method is 'json'
        elif method == 'json':
            # Check if the URL exists and save the data accordingly
            if not utils.check_url_exists(url_list[-1],'save_json.txt'):
                for url, dfs_tuple in zip(url_list, dfs_tuple_list):
                    utils.save_scorecard(url, dfs_tuple, method, fnames, conn)
            else:
                print("Not Saving as last saved url is reached") 
        # Check if the method is 'sql'
        elif method == 'sql':
            # Check if the URL exists and save the data accordingly
            if not utils.check_url_exists(url_list[-1],'save_sql.txt'):
                for url, dfs_tuple in zip(url_list, dfs_tuple_list):
                    utils.save_scorecard(url, dfs_tuple, method, fnames, conn)
            else:
                print("Not Saving as last saved url is reached") 
        else:
            print("required parameters not provided Not Provided")

    def save_scorecard_unchecked(self, url_list: str, dfs_tuple_list: tuple, method: str, fnames: dict = None, conn=None):
        """
        Save the scraped scorecard to files without checking what is last url.

        Args:
        - url_list (list): List of URLs.
        - dfs_tuple_list (list): List of tuples containing scraped data.
        - method (str): Method to save the data (e.g., 'csv', 'json', 'sql').
        - fnames (dict): Dictionary containing file names for different types of data.
        - conn: Database connection object.

        Returns:
        - None
        """
        for url, dfs_tuple in zip(url_list,dfs_tuple_list):
            utils.save_scorecard(url, dfs_tuple, method, fnames, conn)



    




    




                



    
