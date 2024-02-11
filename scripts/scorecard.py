#from bs4 import BeautifulSoup
#import urllib.request
import pandas as pd
import re
import sys
#import requests
#import json 
from datetime import datetime
#import pprint
import utils
import os
import time

class ScoreCard:
    #constructor call collect_stats when class object is created using url which us input to class object
    def __init__(self):
        # Initialize empty lists and dictionaries to store cricket statistics
        self.batting_data = []
        self.batting_header = []
        self.bowling_data = []
        self.bowling_header = []
        self.country_dict = {}
        self.table_count = 0
        self.player_of_the_match = ""
        self.total_score = [["over_played", "run_rate", "total_score", "wickets_fallen", "country", "match_name","innings","scorecard_id"]]
        self.playing_xii = {}
        self.fall_of_wickets_header = [["wicket_number", "fallen_score", "over", "country", "match_name","innings","scorecard_id"]]
        self.fall_of_wickets_data = []
        self.match_details_dict = {key: None for key in ['team_a','team_b','scorecard_id','description','match_result','stadium','series','season','player_of_the_match','match_number',
                                                          'tv_umpire','reserve_umpire','match_referee','umpire','match_date','match_format','toss_won','toss_decision','winner','match_count','match_type',
                                                          'player_of_the_series',"series_result"]}
        
        
           
    # this is main function this collects all the stats and stores them where is required
    def collect_stats(self,url):
        """
        Collect statistics from the provided URL.
        """
        try:
            result = True
            # Scrape data from the URL using BeautifulSoup
            print(f'{"*"*50} SCRAPING DATA {"*"*50}')
            start_time = time.perf_counter()
            scorecard = utils.get_bs_object(url)
            scorecard_id = url.split("/")[-2].split("-")[-1]
            if scorecard.find_all('div', class_="ds-rounded-lg ds-mt-2"):
                self.country_dict = self.get_country_mapping(scorecard)
                self.match_details_dict['team_a'] = self.country_dict['0']
                self.match_details_dict['team_b'] = self.country_dict['1']
                self.match_details_dict['scorecard_id'] = scorecard_id
                self.match_details(scorecard, scorecard_id)
                self.scores(scorecard, scorecard_id)
                if self.table_count < 2:
                    print("Data is not available for this match")
                    result = False
                
            else:
                print("Data is not available for this match")
                result = False
            end_time = time.perf_counter()
            print("scraping took :", round(end_time - start_time, 4), "seconds")
            print(f'{"*"*50} SCRAPING DONE {"*"*50}')
        except Exception as err:
            print("Error:", err)
            print("Provided URL is not valid for scraping data.")
            print("Exiting...")
            sys.exit(0)
        finally:
            return result


    def get_country_mapping(self,scorecard):
        c_dict  = {}
        outer_div = scorecard.find('div',class_ = "ds-flex ds-flex-col ds-mt-3 md:ds-mt-0 ds-mt-0 ds-mb-1")
        for index,div in enumerate(list(outer_div.children)):
        #print(div.find('div').text)
            c_dict[str(index)] = div.find('div').text

        return c_dict

    #Score scraping Function    
    def scores(self, scorecard, scorecard_id):
        """
        Extract batting, bowling, and total score information from the scorecard.
        """
        country_index = 0
        innings = ""
        match_name_here = self.get_match_name_from_url()
        # Loop through main divs in the scorecard HTML
        
        for main_div in scorecard.find_all('div', class_="ds-rounded-lg ds-mt-2"):
            outer_span = main_div.find("span")
            for index,inner_span in enumerate(list(outer_span.children)):
                text = inner_span.text.replace('\xa0',"").strip()
                if index != 0:
                    if "innings" in text.lower():
                        innings = text.lower().split()[0]
                    else:
                        innings = "1st"
            # Extract batting data from tables
            for index,sc in enumerate(main_div.find_all('table', class_="ds-w-full ds-table ds-table-md ds-table-auto ci-scorecard-table")):
                # extracting batting header
                for tag in list(sc.find('thead').children):
                        header = [td.text.replace("\xa0", "dismissed").replace("†", "").replace("(c)", "").strip().lower() if td  else None for td in list(tag.children)]
                        header = header if len(header) == 8 else header[:-1]
                        self.batting_header = header
                        self.batting_header.extend(["country", "match_name","ininngs", "scorecard_id"])
                
                # extracting batting data and processing the data 
                for tag in list(sc.find('tbody').children):
                    if not tag.get("class") :
                        batter_row = [td.text.replace("\xa0", " ").replace("†", "").replace("(c)", "").strip() if td else None for td in list(tag.children)]
                        batter_row = ['0' if item =='-' else item for item in batter_row]
                        batter_row = batter_row if len(batter_row) ==8 else batter_row[:-1]
                        if batter_row and 'TOTAL' not in batter_row and not bool(re.search('Fall of wickets', " ".join(batter_row))):
                            batter_row.extend([self.country_dict[str(country_index)],match_name_here,innings,scorecard_id])
                            self.batting_data.append(batter_row)
                        elif batter_row and 'TOTAL' in batter_row and not bool(re.search('Fall of wickets', " ".join(batter_row))):
                            self.total_score.append([
                                batter_row[1].split(" ")[0].strip(),
                                batter_row[1].split(" ")[-1][:-1].strip(),
                                batter_row[2].split("/")[0],
                                batter_row[2].split("/")[1] if len(batter_row[2].split("/")) > 1 else '10',
                                self.country_dict[str(country_index)],
                                match_name_here,
                                innings,
                                scorecard_id
                            ])
                        else:
                            if batter_row:
                                for s in batter_row[0].split("),"):
                                    if "Fall of wickets" in s:
                                        lis = s.strip().split(" ")[3].split("-")
                                        lis.extend([s.split()[-2], self.country_dict[str(country_index)],match_name_here,innings,scorecard_id])
                                    elif "• DRS" in s:
                                        lis = s.strip().split(" ")[0].split("-")
                                        lis.extend([s.split()[-4], self.country_dict[str(country_index)],match_name_here,innings,scorecard_id])
                                    else:
                                        lis = s.strip().split(" ")[0].split("-")
                                        lis.extend([s.split()[-2], self.country_dict[str(country_index)],match_name_here,innings ,scorecard_id])

                                    self.fall_of_wickets_data.append(lis) 

            #extracting bowling data from tables
            for index,sc in enumerate(main_div.find_all('table', class_="ds-w-full ds-table ds-table-md ds-table-auto")):
                # extractng bowling headers
                for tag in list(sc.find('thead').children):
                    header = [td.text.replace("\xa0", " ").replace("†", "").replace("(c)", "").strip().lower() if td  else None for td in list(tag.children)]
                    header = header if len(header) == 11 else header[:-1]
                    self.bowling_header = header
                    self.bowling_header.extend(["country", "match_name","innings", "scorecard_id"])

                #extracting bowlers data
                for tag in list(sc.find('tbody').children):
                    if not tag.get("class") :
                        bowler_row = [td.text.replace("\xa0", " ").replace("†", "").replace("(c)", "").strip() if td else None for td in list(tag.children)]
                        bowler_row = ['0' if item =='-' else item for item in bowler_row]
                        bowler_row = bowler_row if len(bowler_row) == 11 else bowler_row[:-1]
                        if bowler_row:
                            bowler_row.extend([self.country_dict[str(int(not country_index))],match_name_here, innings,scorecard_id])
                            self.bowling_data.append(bowler_row)
                
            country_index = 0 if country_index == 1 else country_index+1
            self.table_count = self.table_count +1
        
        
     
    # this function returjs match name from url
    def get_match_name_from_url(self):
        """
        Extract the match name from the URL.
        """
        match = re.search(r'scorecard of (.*?),', self.match_details_dict['description']).group(1)
        
        if match:
            match_count_here, match_type_here = self.get_match_count_type(match)
            if match_count_here and match_type_here:
                return match_count_here + "-" + match_type_here
            else:
                return None
        else:
            return None

    # this function return batting stats as df taking batting scrapped data list as input
    def batting_stats_to_dataframe(self, header, data):
        df = pd.DataFrame(data=data, columns=header)
        df = df.astype({
            'batting': str,
            'dismissed': str,
            'r': int,
            'b': int,
            'm': int,
            '4s': int,
            '6s': int,
            'sr': float,
            

        })
        df = df.rename(columns={"batting": "batsmen", "r": "runs_scored",
                                                "b": "balls_faced", "4s": "fours", "6s": "sixes", "sr": "strike_rate",
                                                "m": "minutes_played"})
        
        #df['country'] = df['country'].apply(lambda x : self.country_dict[x])

        return df
    
    # this function return bowling stats as df taking bowlingscrapped data list as input
    def bowling_stats_to_dataframe(self, header, data):
        
        df = pd.DataFrame(data=data, columns=header)
        df = df.astype({"o": float,
                                        "m": int,
                                        "r": int,
                                        "w": int,
                                        "econ": float,
                                        "0s": int,
                                        "4s": int,
                                        "6s": int,
                                        "wd": int,
                                        "nb": int,
                                        })

        df = df.rename(columns={"bowling": "bowler",
                                                "o": "overs",
                                                "m": "maidens",
                                                "r": "runs",
                                                "w": "wickets",
                                                "econ": "economy",
                                                "0s": "zeros",
                                                "4s": "fours",
                                                "6s": "sixes",
                                                "wd": "wides",
                                                "nb": "noballs",
                                                })
        #df['country'] = df['country'].apply(lambda x : self.country_dict[x])
        return df
    
    # getting bowling data as df getter function
    def get_batting_stats(self,country:str = None):
        if len(self.batting_header) > 0 and len(self.batting_data) > 0:
            df = self.batting_stats_to_dataframe(self.batting_header, self.batting_data)
            
        else:
            df = None

        if df is not None:
            if country:
                df = df[df['country'] == country]
                df = df.drop(columns=["country"])

        return df.drop(columns=["match_name"])
    
    # getting bowling data as df getter function
    def get_bowling_stats(self,country:str = None):
        if len(self.bowling_header) > 0 and len(self.bowling_data) > 0:
            df = self.bowling_stats_to_dataframe(self.bowling_header, self.bowling_data)
            
        else:
            df = None

        if df is not None:
            if country:
                df = df[df['country'] == country]
                df = df#.drop(columns="country")

        return df#.drop(columns=["match_name"])
    
    #this function scraps match_detail fron bs object
    def match_details(self,scorecard, scorecard_id):
        """
        Extract match details from the scorecard HTML.
        """
        header = []
        data = []
        des =  [d.get('content') for d in scorecard.find_all('meta',itemprop="description")][0].strip()
        self.match_details_dict['description'] = des
        self.match_details_dict['match_result']  = scorecard.find("p",class_ = 'ds-text-tight-m ds-font-regular ds-truncate ds-text-typo').text.strip()
        match_details_table = scorecard.find('table', class_='ds-w-full ds-table ds-table-sm ds-table-auto')
        tbody = match_details_table.find('tbody')
        
        if tbody:
            for tr in list(tbody.children):
                for td in list(tr.children):
                    if  " ".join(td.get("class")) == 'ds-min-w-max':
                        header.append('stadium')
                        data.append(",".join([span.text.strip() if span else None for span in list(td.children)]))
                        
                    elif 'ds-min-w-max ds-text-typo' in " ".join(td.get("class")):
                        data.append(",".join([span.text.strip() if span else None for span in list(td.children)]))
                    else:
                        header.append(",".join([span.text.strip().replace(" ","_").lower() if span else None for span in list(td.children)]))

            dict_1 = dict(zip(header,data))
            date = dict_1['match_days'].split('-')[0].strip()
            format_date = " ".join([date.split()[0].split(",")[0],date.split()[1],date.split()[2]])
            dict_1['match_date'] = datetime.strptime(format_date, "%d %B %Y").strftime("%d-%m-%Y")
            self.match_details_dict.update(dict_1)
        else:
            print("Match details table not found on the page.")
    
    def get_match_count_type(self,s:str):
        """
        Parse a string to extract match count and match type information.
        """
        parts = s.split()
        match_count = '1st'
        match_type = parts[0]

        if len(parts) > 1:
            for part in parts:
                if any(char.isdigit() for char in part.strip()) and "t20" not in part.lower():
                    match_count = part
                else:
                    match_type = part

        return (match_count, match_type)
         
    #this function returns match_details df 
    def match_details_to_df(self,match_details:dict):
        # Convert the dictionary to a DataFrame
        """
        Convert match details dictionary to a DataFrame.
        """
        df = pd.DataFrame([match_details])
        # Split the 'Umpires' column into two new columns
        # standing_umpire1 and standing_umpire2 columns
        
        if df.count:
            if 'umpires' in df.columns:
                df["standing_umpire1"] = df['umpires'].apply(lambda x: x.split(",")[0].strip() if x else x )
                df["standing_umpire2"] = df['umpires'].apply(lambda x: x.split(",")[1].strip()  if len(x.split(",")) > 1 else None)
            else:
                df["standing_umpire1"] = None
                df["standing_umpire2"] = None

            if 'match_number' in df.columns:
                df['match_format'] = df['match_number'].apply(lambda x: x.split()[0].strip() if x else x)
            else:
                df['match_format'] = None

            if 'toss' in df.columns:
                df['toss_won'] = df['toss'].apply(lambda x: x.split(",")[0].strip() if x else x)
                df['toss_decision'] = df['toss'].apply(lambda x: x.split(",")[1].strip() if x else x )
            else:
                df['toss_won'] = None
                df['toss_decision'] = None

            if 'match_result' in df.columns:
                df['winner'] = df['match_result'].apply(lambda x: x[:x.lower().find("won") if x else x].strip())
            else:
                df['winner'] = None
            if 'description' in df.columns:
                df['match_count'] = df['description'].apply(lambda x: self.get_match_count_type(re.search(r'scorecard of (.*?),', x).group(1))[0] if x else x)
                df['match_type'] = df['description'].apply(lambda x: self.get_match_count_type(re.search(r'scorecard of (.*?),', x).group(1))[1] if x else x)
            else:
                df['match_count'] =  None
                df['match_type'] = None

            columns_to_drop=["toss","hours_of_play_(local_time)","match_days","umpires","points"]
            for col in columns_to_drop:
                if col in df.columns:
                    df.drop(columns=[col], inplace=True)
                    
        cols= ['team_a','team_b','scorecard_id','description','match_result','stadium','series',"series_result",'season','player_of_the_match','player_of_the_series','match_number',
            'tv_umpire','reserve_umpire','match_referee','standing_umpire1','standing_umpire2','match_date','match_format','toss_won','toss_decision','winner','match_count','match_type']

        #df['team_a'] = df['team_a'].apply(lambda x : self.country_dict[x])
        #df['team_b'] = df['team_b'].apply(lambda x : self.country_dict[x])
        return df[cols]

    # getting match_details data as df getter function
    def get_match_details(self,country:str = None):
        if self.match_details_dict:
            df = self.match_details_to_df(self.match_details_dict)
        else:
            df = None

        if df is not None:
            if country:
                df = df[df['country'] == country]
                df = df.drop(columns="country")

        return df
    
    #this function returns total_score df 
    def total_score_to_df(self,totals:list):
        df = pd.DataFrame(data = totals[1:],columns=totals[0])
        #df['country'] = df['country'].apply(lambda x : self.country_dict[x])
        return df
    
    # getting total_score data as df getter function
    def get_total_score(self,country:str = None):
        df =  self.total_score_to_df(self.total_score)
        
    
        if df is not None:
            if country:
                df = df[df['country'] == country]
                df = df.drop(columns="country")

        return df.drop(columns=["match_name"])
    
    def fall_of_wickets_to_df(self,header,data):
        df =  pd.DataFrame(data = data,columns=header)
        #df['country'] = df['country'].apply(lambda x : self.country_dict[x])

        return df
    
    def get_fall_of_wickets(self,country:str = None):
        if len(self.fall_of_wickets_header) > 0 and len(self.fall_of_wickets_data) > 0:
            df = self.fall_of_wickets_to_df(self.fall_of_wickets_header, self.fall_of_wickets_data)
            
        else:
            df = None

        if df is not None:
            if country:
                df = df[df['country'] == country]
                df = df.drop(columns="country")

        return df.drop(columns=["match_name"])
    
    # getting playing_xii data as dict or list getter function
    def get_playing_xii(self,country = None):
        self.playing_xii = {}
        batting_df = self.get_batting_stats()
        bowling_df = self.get_bowling_stats()
        for c in self.country_data:
            batsmen = batting_df[batting_df['country'] == c]['batsmen'].unique().tolist()
            bowlers = bowling_df[bowling_df['country'] == c]['bowler'].unique().tolist()

            team = list(set(batsmen) | set(bowlers))
            self.playing_xii[c] = team
        
        if country:
            return self.playing_xii[country]
        else:
            return self.playing_xii
    
    #prints all stats data
    def display_all_stats(self):
        print(f'\t {"#"*100}' )
        print(f'{"*"*20}  DISPLAYING ALL STATS  {"*"*20}')
        print(f'\t {"*"*10} DISPLAYING MATCH DETAILS  {"*"*10}')
        print(self.get_match_details().T)
        print(f'\t {"*"*10}  DISPLAYING TOTAL SCORE  {"*"*10}')
        print(self.get_total_score())
        print(f'\t {"*"*10}  DISPLAYING BATTING STATS  {"*"*10}')
        print(self.get_batting_stats())
        print(f'\t {"*"*10}  DISPLAYING BOWLING STATS  {"*"*10}')
        print(self.get_bowling_stats())
        print(f'\t {"#"*100}' )

    #prints all stats data
    def get_all_stats(self):
        return (self.get_match_details(),self.get_total_score(),self.get_batting_stats(),self.get_bowling_stats())

    #getting the player of the match 
    def get_player_of_the_match(self):
        if not self.match_details_dict:
            return None
        else:
            return self.match_details_dict['player_of_the_match']

    
    def clear_data(self):
        self.batting_data = []
        self.batting_header = []
        self.bowling_data = []
        self.bowling_header = []
        self.country_data = []
        self.player_of_the_match = ""
        self.total_score = []
        self.playing_xii = {}
        self.fall_of_wickets_header = []
        self.fall_of_wickets_data = []
        self.match_details_dict={}


# Example usage:
'''
if __name__ == "__main__":
    url = '/series/west-indies-championship-2023-24-1419858/guyana-vs-trinidad-tobago-4th-match-1419862/full-scorecard'
    score_card = ScoreCard()
    score_card.collect_stats(url)
    #print(score_card.bowling_header)
    #print(score_card.bowling_data)
    score_card.display_all_stats()
    #print(score_card.get_match_details().T)
    #print(score_card.get_batting_stats())
'''
