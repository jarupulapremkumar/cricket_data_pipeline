from bs4 import BeautifulSoup
import urllib.request
import pandas as pd
import re
import sys

class ScoreCard:
    #constructor call collect_stats when class object is created using url which us input to class object
    def __init__(self, url):
        self.batting_data = []
        self.batting_header = []
        self.bowling_data = []
        self.bowling_header = []
        self.country_data = []
        self.player_of_the_match = ""
        self.total_score = [["over_played", "run_rate", "total_score", "wickets_fallen", "country", "match_name", "scorecard_id"]]
        self.playing_xii = {}
        self.fall_of_wickets_header = [["wicket_number", "score", "over", "country", "match_name", "scorecard_id"]]
        self.fall_of_wickets_data = []
        self.match_details_dict={ key:None for key in ['team_a','team_b','scorecard_id','description','match_result','stadium','series','season','player_of_the_match','match_number',
               'tv_umpire','reserve_umpire','match_referee','standing_umpire1','standing_umpire2','match_date','match_format','toss_won','toss_decision','winner','match_count','match_type',
               'player_of_the_series',"series_result",]}

        self.collect_stats(url)

    #this function fetches the html content from provided url and throws error is url is not valid
    def get_html_response(self, url):
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

    #this fonction return bs object of html content
    def get_bs_object(self, url):
        return BeautifulSoup(self.get_html_response(url), 'lxml')

    # this is main function this collects all the stats and stores them where is required
    def collect_stats(self, url):
        try:
            scorecard = self.get_bs_object(url)
            self.player_of_the_match = scorecard.find("span", class_="ds-text-tight-m ds-font-medium ds-text-typo ds-underline ds-decoration-ui-stroke hover:ds-text-typo-primary hover:ds-decoration-ui-stroke-primary ds-block ds-cursor-pointer").text

            for country in scorecard.find_all('span', class_='ds-text-title-xs ds-font-bold ds-capitalize'):
                self.country_data.append(country.text)

            scorecard_id = url.split("/")[-2].split("-")[-1]
        
            self.match_details_dict['team_a'] = self.country_data[0]
            self.match_details_dict['team_b'] = self.country_data[1]
            self.match_details_dict['scorecard_id'] = scorecard_id
            self.match_details(scorecard, scorecard_id)
            self.batting_stats(scorecard, scorecard_id)
            self.bowling_stats(scorecard, scorecard_id)
            
        except Exception as err:
            print("Error : ",err)
            print("provided url is not valid to scrap the data , provide espninfo scorecard url")
            print("Exiting.......")
            sys.exit(0)

    # this function scraps batting stats from bs object 
    def batting_stats(self,scorecard,scorecard_id):
        batting_country_index = 0
        match_name_here = self.get_match_name_from_url()
        for sc in scorecard.find_all('table', class_="ds-w-full ds-table ds-table-md ds-table-auto ci-scorecard-table"):
            for headers in sc.find("thead"):
                header_list =[]
                for header in headers.find_all('th'):
                    if header.text == '\xa0':
                        header_list.append('WICKET')
                    else:
                        header_list.append(header.text)
                self.batting_header = header_list
                self.batting_header.extend(["country", "match_name", "scorecard_id"])

            for bb in sc.find_all('tbody'):
                for batting in bb.find_all('tr', class_ = ""):
                    batter_row = []
                    for batter in batting.find_all("td"):
                        text_value = batter.text.replace("\xa0", " ").replace("†", "").replace("(c)", "").strip()
                        text_value = '0' if text_value == '-' else text_value
                        batter_row.append(text_value)

                    if 'TOTAL' not in batter_row and not bool(re.search('Fall of wickets', " ".join(batter_row))):
                        batter_row.extend([self.country_data[batting_country_index],match_name_here, scorecard_id])
                        self.batting_data.append(batter_row)
                    elif 'TOTAL' in batter_row and not bool(re.search('Fall of wickets', " ".join(batter_row))):
                        self.total_score.append([
                            batter_row[1].split(" ")[0].strip(),
                            batter_row[1].split(" ")[-1][:-1].strip(),
                            batter_row[2].split("/")[0],
                            batter_row[2].split("/")[1] if len(batter_row[2].split("/")) > 1 else '10',
                            self.country_data[batting_country_index],
                            match_name_here,
                            scorecard_id
                        ])
                    else:
                        for s in batter_row[0].split("),"):
                            if "Fall of wickets" in s:
                                lis = s.strip().split(" ")[3].split("-")
                                lis.extend([s.split()[-2], self.country_data[batting_country_index],match_name_here, scorecard_id])
                            elif "• DRS" in s:
                                lis = s.strip().split(" ")[0].split("-")
                                lis.extend([s.split()[-4], self.country_data[batting_country_index],match_name_here, scorecard_id])
                            else:
                                lis = s.strip().split(" ")[0].split("-")
                                lis.extend([s.split()[-2], self.country_data[batting_country_index],match_name_here, scorecard_id])

                            self.fall_of_wickets_data.append(lis)

            batting_country_index += 1

    #this function scraps bowling stats fron bs object
    def bowling_stats(self, scorecard, scorecard_id):
        bowling_country_index = len(self.country_data) - 1
        match_name_here = self.get_match_name_from_url()
        for sc in scorecard.find_all('table', class_="ds-w-full ds-table ds-table-md ds-table-auto"):
            for headers in sc.find("thead"):
                header_list =[]
                for header in headers.find_all('th'):
                    if header.text == '\xa0':
                        header_list.append('WICKET')
                    else:
                        header_list.append(header.text)
                self.bowling_header = header_list
                self.bowling_header.extend(["country", "match_name", "scorecard_id"])

            for bb in sc.find_all('tbody'):
                for bowling in bb.find_all('tr', class_ = ""):
                    bowler_row = []
                    for bowler in bowling.find_all("td"):
                        text_value = bowler.text.replace("\xa0", " ").replace("†", "").replace("(c)", "").strip()
                        text_value = '0' if text_value == '-' else text_value
                        bowler_row.append(text_value)

                    if 'TOTAL' not in bowler_row and not bool(re.search('Fall of wickets', " ".join(bowler_row))):
                        bowler_row.extend([self.country_data[bowling_country_index],match_name_here, scorecard_id])
                        self.bowling_data.append(bowler_row)

            bowling_country_index -= 1

    # this function returjs match name from url
    def get_match_name_from_url(self):
        '''
        if ("africa" in link and "lanka" in link) or ("africa" in link and "zealand" in link) or ("lanka" in link and "zealand" in link):
            return "_".join(link.split("/")[-2].split("-")[5:-1])
        elif "africa" in link or "lanka" in link or "zealand" in link:
            return "_".join(link.split("/")[-2].split("-")[4:-1])
        else:
            return "_".join(link.split("/")[-2].split("-")[3:-1])
        '''
        match_count_here = self.get_match_count_type(re.search(r'scorecard of (.*?),', self.match_details_dict['description']).group(1))[0]
        match_type_here = self.get_match_count_type(re.search(r'scorecard of (.*?),', self.match_details_dict['description']).group(1))[1]
        
        return match_count_here+"-"+match_type_here

    # this function return batting stats as df taking batting scrapped data list as input
    def batting_stats_to_dataframe(self, header, data):
        batting_df = pd.DataFrame(data=data, columns=header)
        batting_df = batting_df.astype({
            'BATTING': str,
            'WICKET': str,
            'R': int,
            'B': int,
            'M': int,
            '4s': int,
            '6s': int,
            'SR': float,
            'country': str,
            'match_name': str
        })
        batting_df = batting_df.rename(columns={"BATTING": "batsmen", "R": "runs_scored",
                                                "B": "balls_faced", "4s": "fours", "6s": "sixes", "SR": "strike_rate",
                                                "M": "minutes_played", 'WICKET': "wicket"})

        return batting_df
    
    # this function return bowling stats as df taking bowlingscrapped data list as input
    def bowling_stats_to_dataframe(self, header, data):
        bowling_df = pd.DataFrame(data=data, columns=header)
        bowling_df = bowling_df.astype({"BOWLING": str,
                                        "O": float,
                                        "M": int,
                                        "R": int,
                                        "W": int,
                                        "ECON": float,
                                        "0s": int,
                                        "4s": int,
                                        "6s": int,
                                        "WD": int,
                                        "NB": int,
                                        "country": str,
                                        "match_name": str
                                        })

        bowling_df = bowling_df.rename(columns={"BOWLING": "bowler",
                                                "O": "overs",
                                                "M": "maidens",
                                                "R": "runs",
                                                "W": "wickets",
                                                "ECON": "economy",
                                                "0s": "zeros",
                                                "4s": "fours",
                                                "6s": "sixes",
                                                "WD": "wides",
                                                "NB": "noballs",
                                                })
        return bowling_df
    
    
    # getting bowling data as df getter function
    def get_batting_stats(self):
        if len(self.batting_header) > 0 and len(self.batting_data) > 0:
            batting_df = self.batting_stats_to_dataframe(self.batting_header, self.batting_data)
        else:
            batting_df = None

        return batting_df
    
    # getting bowling data as df getter function
    def get_bowling_stats(self):
        if len(self.bowling_header) > 0 and len(self.bowling_data) > 0:
            bowling_df = self.bowling_stats_to_dataframe(self.bowling_header, self.bowling_data)
        else:
            bowling_df = None

        return bowling_df
    
    #this function scraps match_detail fron bs object
    def match_details(self,scorecard, scorecard_id):
        # Find the table containing match details
        des =  [d.get('content') for d in scorecard.find_all('meta',itemprop="description")][0].strip()
        self.match_details_dict['description'] = des
        self.match_details_dict['match_result']  = scorecard.find("p",class_ = 'ds-text-tight-m ds-font-regular ds-truncate ds-text-typo').text.strip()
        match_details_table = scorecard.find('table', class_='ds-w-full ds-table ds-table-sm ds-table-auto')
        tbody_table = match_details_table.find('tbody')
        
        
        if tbody_table:
            # Extract and print the match details
            #for match_details in tbody_table:
            rows = tbody_table.find_all('tr')
            for row in rows:
                cols = row.find_all('td')
                cols = [[div.text.strip() for div in col.find_all('div')]  # Get text content of each div within the column
                            if col.find('div') else [col.text.strip()]        # Check if the column contains a div tag
                            for col in cols                                   # Iterate over each column in the table row
                        ]
                
                if(len(cols)==1):
                    self.match_details_dict['stadium']  = cols[0][0].strip()
                else:
                    self.match_details_dict[cols[0][0].replace(" ","_").lower()]  = ",".join([col for col in cols[1] if col.strip()]).strip(",")
                    #umpires_without_empty_strings = [umpire for umpire in umpires if umpire.strip()]
                        

            #print(self.match_details_dict)
        else:
            print("Match details table not found on the page.")
    
    def get_match_count_type(self,s:str):
        # Split the string
        parts = s.split()
        
        # Initialize match_count and match_type
        match_count = '1st'
        match_type = parts[0]

        # Update match_count and match_type if more than one part
        if len(parts) > 1:
            match_count = next(part for part in parts if any(char.isdigit() for char in part.strip()))
            match_type = next(part for part in parts if not any(char.isdigit() for char in part.strip()))

        return (match_count, match_type)
                
    #this function returns match_details df 
    def match_details_to_df(self,match_details:dict):
        # Convert the dictionary to a DataFrame
        df = pd.DataFrame([match_details])
        # Split the 'Umpires' column into two new columns
        # standing_umpire1 and standing_umpire2 columns
        if 'umpires' in df.columns:
            df["standing_umpire1"] = df['umpires'].apply(lambda x: x.split(",")[0].strip())
            df["standing_umpire2"] = df['umpires'].apply(lambda x: x.split(",")[1].strip())
        else:
            df["standing_umpire1"] = None
            df["standing_umpire2"] = None

        # match_date column
        if 'match_days' in df.columns:
            df['match_date'] = df['match_days'].apply(lambda x: x.split("-")[0].strip())
        else:
            df['match_date'] = None

        # Other columns
        if 'match_number' in df.columns:
            df['match_format'] = df['match_number'].apply(lambda x: x.split()[0].strip())
        else:
            df['match_format'] = None

        if 'toss' in df.columns:
            df['toss_won'] = df['toss'].apply(lambda x: x.split(",")[0].strip())
            df['toss_decision'] = df['toss'].apply(lambda x: x.split(",")[1].strip())
        else:
            df['toss_won'] = None
            df['toss_decision'] = None

        if 'match_result' in df.columns:
            df['winner'] = df['match_result'].apply(lambda x: x[:x.lower().find("won")].strip())
        else:
            df['winner'] = None
        if 'description' in df.columns:
            df['match_count'] = df['description'].apply(lambda x: self.get_match_count_type(re.search(r'scorecard of (.*?),', x).group(1))[0])
            #df['match_type'] = df['description'].apply(lambda x: re.search(r'scorecard of (.*?),', x).group(1).split()[1] if len(re.search(r'scorecard of (.*?),', x).group(1).split()) > 1 else re.search(r'scorecard of (.*?),', x).group(1).split()[0])
            df['match_type'] = df['description'].apply(lambda x: self.get_match_count_type(re.search(r'scorecard of (.*?),', x).group(1))[1])
        else:
            df['match_count'] =  None
            df['match_type'] = None


        columns_to_drop=["toss","hours_of_play_(local_time)","match_days","umpires","points"]
        # Check if columns exist in the DataFrame and drop them if they exist
        for col in columns_to_drop:
            if col in df.columns:
                df.drop(columns=[col], inplace=True)
                
        cols= ['team_a','team_b','scorecard_id','description','match_result','stadium','series','season','player_of_the_match','match_number',
               'tv_umpire','reserve_umpire','match_referee','standing_umpire1','standing_umpire2','match_date','match_format','toss_won','toss_decision','winner','match_count','match_type']

        return df[cols]

    # getting match_details data as df getter function
    def get_match_details(self):
         
        return self.match_details_to_df(self.match_details_dict)
    
    #this function returns total_score df 
    def total_score_to_df(self,totals:list):
        df = pd.DataFrame(data = totals[1:],columns=totals[0])
        return df
    
    # getting total_score data as df getter function
    def get_total_score(self):
        return  self.total_score_to_df(self.total_score)
    
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
    def get_all_stats(self):
        print(self.get_match_details())
        print(self.get_total_score())
        print(self.get_batting_stats())
        print(self.get_bowling_stats())

    #getting the player of the match 
    def get_player_of_the_match(self):
        if not self.match_details_dict:
            return None
        else:
            return self.match_details_dict['player_of_the_match']
        

    

# Example usage:
#url = 'https://www.espncricinfo.com/series/icc-cricket-world-cup-2023-24-1367856/australia-vs-south-africa-2nd-semi-final-1384438/full-scorecard'
#score_card = ScoreCard(url)
#print(score_card.get_player_of_the_match())
