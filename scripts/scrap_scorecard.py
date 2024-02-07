from bs4 import BeautifulSoup
import urllib.request
import re
import pandas as pd

def get_html_response(url:str):
    #checking whether domain is available in url based on that we fetch theresponse
    try: 
        if "www.espncricinfo.com" not in url:
            return urllib.request.urlopen('https://www.espncricinfo.com'+url).read()
        else:
            return urllib.request.urlopen(url).read()
    except Exception as err:
        print("Error getting html response",err)


def get_match_name_from_url(link):
    if ("africa" in link) and ("lanka" in link):
        return "_".join( link.split("/")[-2].split("-")[5:-1])

    elif ("africa" in link) and ("zealand" in link):
        return "_".join( link.split("/")[-2].split("-")[5:-1])

    elif ("lanka" in link) and ("zealand" in link):
        return "_".join( link.split("/")[-2].split("-")[5:-1])

    elif ("africa" in link) or ("lanka" in link) or ("zealand" in link):
        return "_".join( link.split("/")[-2].split("-")[4:-1])
    else:
        return "_".join(link.split("/")[-2].split("-")[3:-1])
                    
 
# function to get batting_stats of match from html respomse and returns list of list contins headers and data [[header],[data]]
def get_batting_stats(url):
    batting_data = []
    batting_header = []
    country_data = []

    source = get_html_response(url)

    #using Beautifulsoup to read the response and do scaping
    score_card = BeautifulSoup(source,'lxml')
    
    #getting country name 
    for country in score_card.find_all('span',class_='ds-text-title-xs ds-font-bold ds-capitalize'):
        country_data.append(country.text)

    #setting index value to add the country name  for batting : for batting we go asc order and for bowling we go desc order 
    batting_country_index = 0
   
    #getting the table related to bating 
    for sc in score_card.find_all('table',class_="ds-w-full ds-table ds-table-md ds-table-auto ci-scorecard-table"):
        # fetching table headers
        for headers in sc.find("thead"):
            header_list =[]
            for header in headers.find_all('th'):
                if header.text == '\xa0':
                    header_list.append('WICKET')
                else:
                    header_list.append(header.text)
            batting_header = header_list
            batting_header.extend(["country","match_name"])
        # fetching table data
        for bb in sc.find_all('tbody'):
            for batting in bb.find_all('tr',class_ = ""):
                batter_row = []
                for batter in batting.find_all("td"):
                    batter_row.append(batter.text.replace("\xa0", " ").replace("†","").replace("(c)","").replace("-","0").strip())
                # filtering only batter data from all data
                if ('TOTAL' not in batter_row) and not bool(re.search('Fall of wickets', " ".join(batter_row))) :
                    batter_row.extend([country_data[batting_country_index],get_match_name_from_url(url)])
                    batting_data.append(batter_row)
            
       
        batting_country_index = batting_country_index + 1

    return (batting_header,batting_data)
        
# function to get batting_stats of match from html respomse and returns list of list contins headers and data [[header],[data]]
def get_bowling_stats(url):

    bowling_data = []
    bowling_header = []
    country_data = []
    
    #getting html response
    source = get_html_response(url)
    #using Beautifulsoup to read the response and do scaping
    score_card = BeautifulSoup(source,'lxml')
    
    #getting country name
    for country in score_card.find_all('span',class_='ds-text-title-xs ds-font-bold ds-capitalize'):
        country_data.append(country.text)

    #setting index value to add the country name  for bowling : for batting we go asc order and for bowling we go desc order
    bowling_country_index = len(country_data) - 1
    
    #getting the table related to bowling 
    for sc in score_card.find_all('table',class_="ds-w-full ds-table ds-table-md ds-table-auto"):
        # fetching table headers
        for headers in sc.find("thead"):
            header_list =[]
            for header in headers.find_all('th'):
                if header.text == '\xa0':
                    header_list.append('WICKET')
                else:
                    header_list.append(header.text)
            bowling_header = header_list
            bowling_header.extend(["country","match_name"])
        # fetching table data
        for bb in sc.find_all('tbody'):
            for bowling in bb.find_all('tr',class_ = ""):
                bowler_row = []
                for bowler in bowling.find_all("td"):
                    bowler_row.append(bowler.text.replace("\xa0", " ").replace("†","").replace("(c)","").replace("-","0").strip())
                # filtering only bowler data from all data
                if ('TOTAL' not in bowler_row) and not bool(re.search('Fall of wickets', " ".join(bowler_row))) :
                    bowler_row.extend([country_data[bowling_country_index],get_match_name_from_url(url)])
                    bowling_data.append(bowler_row)

        bowling_country_index = bowling_country_index - 1
    return(bowling_header,bowling_data)

# function function that takes url and gives dataframe as output for batting_details
def get_batting_stats_as_dataframe(url):
    data = get_batting_stats(url)
    batting_df = pd.DataFrame(data= data[1],columns=data[0])
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
    batting_df = batting_df.rename(columns={"BATTING": "batsmen","R":"runs_scored",
                                            "B":"balls_faced","4s":"fours","6s":"sixes","SR":"strike_rate",
                                            "M":"matches_played",'WICKET':"wicket"})
    #batting_df = batting_df.drop(columns='wicket')

    return batting_df



def get_bowling_stats_as_dataframe(url):
    data = get_bowling_stats(url)
    bowling_df = pd.DataFrame(data= data[1],columns=data[0])
    bowling_df = bowling_df.astype({"BOWLING": str,
                                    "O":  float,
                                    "M":  int, 
                                    "R":  int,
                                    "W":  int,
                                    "ECON":  float,
                                    "0s": int,
                                    "4s": int,
                                    "6s": int,
                                    "WD": int,
                                    "NB":  int,  
                                    "country": str,
                                    "match_name":str
                                })
    
    bowling_df = bowling_df.rename(columns = {"BOWLING": "bowler",
                                    "O":  "overs",
                                    "M":  "maidens", 
                                    "R":  "runs",
                                    "W":  "wickets",
                                    "ECON":  "economy",
                                    "0s": "zeros",
                                    "4s": "fours",
                                    "6s": "sixes",
                                    "WD": "wides",
                                    "NB":  "noballs",  
                                })
    return bowling_df
    
    #print(bowling_df)




#print(get_batting_stats(url='/series/icc-cricket-world-cup-2023-24-1367856/england-vs-south-africa-20th-match-1384411/full-scorecard')) 
#print(get_bowling_stats(url='/series/icc-under-19-world-cup-2023-24-1399722/south-africa-under-19s-vs-india-under-19s-1st-semi-final-1399762/full-scorecard'))
#print(get_batting_stats_as_dataframe('/series/icc-cricket-world-cup-2023-24-1367856/england-vs-south-africa-20th-match-1384411/full-scorecard'))
#print(get_bowling_stats_as_dataframe('/series/icc-cricket-world-cup-2023-24-1367856/england-vs-south-africa-20th-match-1384411/full-scorecard'))



