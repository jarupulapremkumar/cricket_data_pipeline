from datetime import datetime,timedelta
from cricscoredigger import CricScoreDigger
import os
from scorecard import ScoreCard
from sqlalchemy import create_engine,inspect
import storesql

import pymysql


if __name__ == "__main__":

    # Example usage:
    '''

    url = '/series/ranji-trophy-plate-league-2023-24-1383415/hyderabad-india-vs-nagaland-1st-semi-final-1383838/full-scorecard'
    score_card = ScoreCard()
    score_card.collect_stats(url)
    #print(score_card.bowling_header)
    #print(score_card.bowling_data)
    #score_card.display_all_stats()
    #print(score_card.get_match_details().T)
    #print(score_card.get_batting_stats())
    
    '''
    '''
    csd = CricScoreDigger()
     # Get the current date
    current_date = datetime.now()

    # Format the date as "DD-MM-YYYY"
    date = current_date.strftime("%d-%m-%Y")

    #dates_list = csd.get_dates(start_date="08-02-2024", end_date=date)
    #print("date_list : ",dates_list)
    mysql_url = "mysql://root:root@localhost:3306/sport"
    
    conn = create_engine(mysql_url)
    print("current_month:",date)
    print(f'{"*"*10} SCRAPING DATA{"*"*10}')
    #print(csd.scrape_date(start_date='08-02-2024', end_date=date))
    url_list,dfs_list = csd.scrape_date(start_date='08-02-2024', end_date=date)

    
    csd.save_scorecard_checked(url_list,dfs_list,method = 'csv')
    '''
    #'''
    csd = CricScoreDigger()
     # Get the current date
    current_date = datetime.now()

    # Format the date as "DD-MM-YYYY"
    date = current_date.strftime("%d-%m-%Y")

    #dates_list = csd.get_dates(start_date="08-02-2024", end_date=date)
    #print("date_list : ",dates_list)
    mysql_url = "mysql+mysqlconnector://root:root@localhost:3306/sports"
    engine = create_engine(mysql_url)
    
    # Create the database engine
    #engine = conn = pymysql.connect(host='localhost',
    #                   port=3306,
    #                   user='root', 
    #                   passwd='root',  
    #                   db='sports')
    ## Create an inspector object
    inspector = inspect(engine)

    # Get the names of all tables in the database
    table_names = inspector.get_table_names()

    # Print the table names
    print("Tables in the database:")
    for table_name in table_names:
        print(table_name)
    #print("current_month:",date)
    print(f'{"*"*10} SCRAPING DATA{"*"*10}')
    #print(csd.scrape_date(start_date='08-02-2024', end_date=date))
    url_list,dfs_list = csd.scrape_date(start_date='08-02-2024', end_date=date)

    # Define MySQL connection parameters
    config = {
        'user': 'root',
        'password': 'root',
        'host': 'localhost',
        'port': '3306',  # Default MySQL port
        'database': 'sports',
    }
    #csd.save_scorecard_checked(url_list,dfs_list,method = 'csv',conn=engine)
    storesql.save_scorecard_checked(url_list,dfs_list,config)
    #'''
    
    
    
    