from bs4 import BeautifulSoup
import urllib.request
import pandas as pd
import numpy as np
from scrap_scorecard import get_batting_stats,get_bowling_stats
from tqdm import tqdm
from sqlalchemy import create_engine,text
import os
from scrap_scorecard import get_match_name_from_url,get_batting_stats_as_dataframe,get_bowling_stats_as_dataframe,get_html_response


def run_sql_file(engine):
    with engine.connect() as con:
        with open("SQL/query.sql") as file:
            query = text(file.read())
            con.execute(query)
#getting match table of world cup  ODI 2023
def get_match_details(url):
    match_table_header = []
    match_table_data = []

    #getting html response
    source = get_html_response(url)

    soup = BeautifulSoup(source,'lxml') 
    
    for div in soup.find_all('thead'):#, class_='body'):
        match_table_header = [td.text for td in div.find_all('td')]

    
    for div in soup.find_all('tbody'):
        for tr in div.find_all('tr'):
            #print([td.text for td in tr.find_all('td')])
            match_table_data.append([td.text for td in tr.find_all('td')])

    return (match_table_header,match_table_data)

def get_match_details_as_df(url):
    data = get_match_details(url)
    match_table_df = pd.DataFrame(data= data[1],columns=data[0])
    match_table_df = match_table_df.drop(columns="Scorecard")
    match_table_df = match_table_df.rename(columns={"Team 1": "team_a",
                                                    "Team 2":"team_b",
                                                    'Match Date':'match_date',
                                                    "Winner":"winner",
                                                    "Margin":"margin",
                                                    "Ground":"stadium"})
    return match_table_df
    
#function to save match table to csv
def save_match_table_csv(url):
    try : 
        df = get_match_details_as_df(url)
        os.makedirs("datasets", exist_ok=True)
        df.to_csv("datasets/match_table.csv",index=False)
    except Exception as err:
        print("Error saving",err)
    
#function to save match table to sql
def save_match_table_sql(url,engine):
    try:
        get_match_details_as_df(url).to_sql('match_table', con=engine, if_exists='append', index=False) # table_name = match_table
    except Exception as err:
        print("Error saving",err)

def save_batting_data_csv(url):
    try:
        df = get_batting_stats_as_dataframe(url)
        match_name = get_match_name_from_url(url)
        os.makedirs("datasets", exist_ok=True)
        df.to_csv("datasets/batting_"+match_name+".csv",index=False)
    except Exception as err:
        print("Error saving",err)


def save_bowling_data_csv(url):
    try:
        df = get_bowling_stats_as_dataframe(url)
        match_name = get_match_name_from_url(url)
        os.makedirs("datasets", exist_ok=True)
        df.to_csv("datasets/bowling_"+match_name+".csv",index=False)
    except Exception as err:
        print("Error saving",err)
    

def save_batting_data_sql(url,engine):
    try:
        get_batting_stats_as_dataframe(url).to_sql('batting_details', con=engine, if_exists='append', index=False)
    except Exception as err:
        print("Error saving",err)

def save_bowling_data_sql(url,engine):
    try:
        get_bowling_stats_as_dataframe(url).to_sql('bowling_details', con=engine, if_exists='append', index=False)
    except Exception as err:
        print("Error saving",err)



def save_all_match_scorecard_csv(url):
    try:
        #saving match_table
        save_match_table_csv(url)

        source = get_html_response(url)

        #looping over every match and fetching scorecards and storing them
        soup = BeautifulSoup(source,'lxml') 
        for div in soup.find_all('tbody'):
            for tr in tqdm(div.find_all('tr')):
                for link in tr.find_all('a',title=[td.text for td in tr.find_all('td')][-1]):
                    save_batting_data_csv(link.get('href'))
                    save_bowling_data_csv(link.get('href'))
    except Exception as err:
        print("Error saving",err)

def save_all_match_scorecard_sql(url,engine):
    try:
        #saving match_table
        save_match_table_sql(url,engine)

        source = get_html_response(url)

        #looping over every match and fetching scorecards and storing them
        soup = BeautifulSoup(source,'lxml') 
        for div in soup.find_all('tbody'):
            for tr in tqdm(div.find_all('tr')):
                for link in tr.find_all('a',title=[td.text for td in tr.find_all('td')][-1]):
                    save_batting_data_sql(link.get('href'),engine)
                    save_bowling_data_sql(link.get('href'),engine)
    except Exception as err:
        print("Error saving",err)

def get_sql_engine():
    #  Create a SQLAlchemy engine to connect to the MySQL database
    return create_engine("mysql+mysqlconnector://root:root@localhost/sports")
    #mysql+mysqlconnector://username:password@localhost/db_name


if __name__ == "__main__":
    #url to scrap world cup 2023 url
    url = 'https://www.espncricinfo.com/records/tournament/team-match-results/icc-cricket-world-cup-2023-24-15338'

    # for csv
    #save_all_match_scorecard_csv(url)

    #for sql
    engine = get_sql_engine()
    #run_sql_file(engine=engine)
    save_all_match_scorecard_sql(url=url,engine=engine)




                



    
