from bs4 import BeautifulSoup
import urllib.request
import pandas as pd
import numpy as np
from tqdm import tqdm
from sqlalchemy import create_engine,text
import os
from scorecard import ScoreCard
import sys

def get_html_response(url):
    try:
        if "www.espncricinfo.com" not in url:
            return urllib.request.urlopen('https://www.espncricinfo.com' + url).read()
        else:
            return urllib.request.urlopen(url).read()
    except Exception as err:
        print("Error getting html response", err)
        print("provided url is not valid to scrap the data , provide espninfo scorecard url")
        print("Exiting.......")
        sys.exit(0)

#run sql quries from quires.sql file 
def run_sql_file(engine):
    with engine.connect() as con:
        with open("SQL/query.sql") as file:
            query = text(file.read())
            con.execute(query)
            
#function to save all stats of world cup 2023 to csv 
def save_all_match_scorecard_csv(url):
    try:
        source = get_html_response(url)

        #looping over every match and fetching scorecards and storing them
        soup = BeautifulSoup(source,'lxml') 
        for div in soup.find_all('tbody'):
            for tr in tqdm(div.find_all('tr')):
                for link in tr.find_all('a',title=[td.text for td in tr.find_all('td')][-1]):
                    sc = ScoreCard(url = link.get('href'))
                    batting_df = sc.get_batting_stats()
                    bowling_df = sc.get_bowling_stats()
                    match_details_df = sc.get_match_details()
                    total_score_df = sc.get_total_score()
                    save_df_to_csv(batting_df,'batting')
                    save_df_to_csv(bowling_df,"bowling")
                    save_df_to_csv(match_details_df,'match_details')
                    save_df_to_csv(total_score_df,'total_score')
    except Exception as err:
        print("Error saving",err)

#function to save all stats of world cup 2023 to sql
def save_all_match_scorecard_sql(url,engine):
    try:
        source = get_html_response(url)

        #looping over every match and fetching scorecards and storing them
        soup = BeautifulSoup(source,'lxml') 
        for div in soup.find_all('tbody'):
            for tr in tqdm(div.find_all('tr')):
                for link in tr.find_all('a',title=[td.text for td in tr.find_all('td')][-1]):
                    sc = ScoreCard(url = link.get('href'))
                    batting_df = sc.get_batting_stats()
                    bowling_df = sc.get_bowling_stats()
                    match_details_df = sc.get_match_details()
                    total_score_df = sc.get_total_score()
                    save_df_to_sql(batting_df,'batting',engine)
                    save_df_to_sql(bowling_df,"bowling",engine)
                    save_df_to_sql(match_details_df,'match_details',engine)
                    save_df_to_sql(total_score_df,'total_score',engine)
    except Exception as err:
        print("Error saving",err)
        
#  Create a SQLAlchemy engine to connect to the MySQL database
def get_sql_engine():
    return create_engine("mysql+mysqlconnector://root:root@localhost/sports")
    #mysql+mysqlconnector://username:password@localhost/db_name


def save_df_to_csv(df,file_name):
    try:
        os.makedirs("datasets", exist_ok=True)
        df.to_csv("datasets/"+file_name+".csv",index=False,mode='a')
    except Exception as err:
        print(file_name,"Error saving",err)

def save_df_to_sql(df,table_name,engine):
    try:
        df.to_sql(table_name, con=engine, if_exists='append', index=False)
    except Exception as err:
        print(table_name,"Error saving",err)
    

    
    

if __name__ == "__main__":
    #url to scrap world cup 2023 url
    url = 'https://www.espncricinfo.com/records/tournament/team-match-results/icc-cricket-world-cup-2023-24-15338'

    # for csv
    #save_all_match_scorecard_csv(url)
    
    #for sql
    engine = get_sql_engine()
    #run_sql_file(engine=engine)
    save_all_match_scorecard_sql(url=url,engine=engine)


    




                



    
