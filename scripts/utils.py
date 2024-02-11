from bs4 import BeautifulSoup
import urllib.request
from sqlalchemy.types import *
import os
import sys
import requests
import re
from datetime import datetime,timedelta


schema_mappings = {
    'batting' : {
                "batsmen":String(100),
                "dismissed":String(100),
                "runs_scored":Integer,  
                "balls_faced":Integer,  
                "minutes_played":Integer,  
                "fours":Integer,  
                "sixes":Integer,  
                "strike_rate":DECIMAL(5,2), 
                "country": String(64), 
                "ininngs": String(64), 
                "scorecard_id": String(64)
                },

    'bowling' : {
                "bowler":String(100),  
                "overs":DECIMAL(5,2),  
                "maidens":Integer,  
                "runs":Integer,  
                "wickets":Integer,  
                "economy":DECIMAL(5,2),  
                "zeros":Integer,
                "fours":Integer,  
                "sixes":Integer,  
                "wides":Integer,  
                "noballs":Integer, 
                "country":String(64),  
                "match_name":String(64), 
                "innings":String(64),
                "scorecard_id":String(64)
                },

    'match_details' : {
                "team_a":String(64),                                                       
                "team_b":String(64),                                                         
                "scorecard_id":String(64),                                                    
                "description":String(500),           
                "match_result":String(64),         
                "stadium":String(64),                
                "series":String(64),                                                    
                "series_result":String(64),                                                      
                "season":String(64),                                                          
                "player_of_the_match":String(64),                                         
                "player_of_the_series":String(64),                                               
                "match_number":String(64),                                                       
                "tv_umpire":String(64),                                                         
                "reserve_umpire":String(64),                                               
                "match_referee":String(64),                                             
                "standing_umpire1":String(64),                                          
                "standing_umpire2":String(64),                                          
                "match_date":String(64),                                                   
                "match_format":String(64),                                                       
                "toss_won":String(64),                                                     
                "toss_decision":String(64),                                      
                "winner":String(64),                                                         
                "match_count":String(64),                                                        
                "match_type":String(64),
                },

    'total' : {
                "over_played":DECIMAL(5,2), 
                "run_rate":DECIMAL(5,2), 
                "total_score":Integer, 
                "wickets_fallen":Integer,
                "country":String(64), 
                "innings":String(64), 
                "scorecard_id":String(64)
                }

}

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

def get_bs_object(url:str):
    return BeautifulSoup(get_html_response(url), 'lxml')

def save_df_to_csv(df,file_name):
    try:
        if os.path.exists("datasets/"+file_name+".csv"):
            header = False
        else:
            header  = True

        df.to_csv("datasets/"+file_name+".csv",index=False,mode='a',header=header)
    except Exception as err:
        print(file_name,"Error saving",err)

def save_df_to_json(df,file_name):
    try:
        if os.path.exists("datasets/"+file_name):
            header = False
        else:
            header  = True

        df.to_json("datasets/"+file_name,index=False,mode='a',header=header)
    except Exception as err:
        print(file_name,"Error saving",err)

def save_df_to_sql(df,table_name,conn,df_schema):
    try:
        
        # Write the DataFrame to the database
        df.to_sql(name=table_name, con=conn, if_exists='append', index=False, dtype=df_schema)
        
    except Exception as err:
        print("Error saving in sql : ",err)

def search_links(keyword, num_links=25):
    links =[]
    search_url = f"https://www.google.com/search?q={keyword}&num={num_links}"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.61 Safari/537.36"
    }

    response = requests.get(search_url, headers=headers)
    soup = BeautifulSoup(response.text, 'lxml')

    # Find all <a> tags
    links = soup.find_all('a')

    # Define a regular expression pattern to match the desired href format
    pattern = r'href="([^"]*)/full-scorecard"'

    # Extract and print the text between href and /full-scorecard for each link
    for link in links:
        # Search for the pattern in the href attribute of the link
        match = re.search(pattern, str(link))
        if match:
            extracted_text = match.group(1)
            links.append(extracted_text+"/full-scorecard")

    return links

def get_dates_between(start_date,end_date):

    # Create a list to store the dates between start and end dates
    dates_between = []

    # Generate dates between start and end dates
    current_date = start_date
    while current_date <= end_date:
        dates_between.append(current_date.strftime("%d-%m-%Y"))
        current_date += timedelta(days=1)

    return dates_between[::-1]

    #print("dates_between : ",dates_between)
        
def get_urls_on_date(url:str,current_date:str):
    try:
        soup = get_bs_object(url)
        
        url_dict = {}

        for child_div in soup.find_all("div",class_= "ds-mb-6")[1:]:
            if child_div:
                if child_div.findChild().findChild().get('id') == current_date:
                    # Find all <a> tags
                    links = child_div.find_all('a')

                    # Define a regular expression pattern to match the desired href format
                    pattern = r'href="([^"]*)/full-scorecard"'

                    # Extract and print the text between href and /full-scorecard for each link
                    for link in links:
                        # Search for the pattern in the href attribute of the link
                        match = re.search(pattern, str(link))
                        if match:
                            extracted_text = match.group(1)
                            
                            if current_date in url_dict:
                                url_dict[current_date].append(extracted_text+"/full-scorecard")
                            else:
                                url_dict[current_date] = [extracted_text+"/full-scorecard"]
                            
    except Exception as err:
        print("No Data Found or Error : ",err)

    finally:
        return url_dict
    
def check_url_exists(url, cname):
    try:
        result = False
        with open("/checkpoints/" + cname, 'r') as file:
            txt_url = file.readline().strip()  # Read the first line which contains the URL
            if url.strip().lower() == txt_url.lower():
                result = True
    except FileNotFoundError:
        print(f"The file '{cname}' was not found.")
    except Exception as e:
        print(f"An error occurred while reading the file: {e}")
    finally:
        return result

def save_scorecard(url: str, dfs_tuple: tuple, method: str, fnames: dict = None, conn=None):
    try:
        if not fnames:
            fnames = {}

        match_df, total_df, batting_df, bowling_df = dfs_tuple
        print("Saving Files for",url,"...........")
        if method == "csv":
            if not fnames or not any(value == False for value in [True if key in fnames else False for key in ['batting', 'bowling', 'match_details', 'total']]):
                print("Saving with default file names as file names are not provided")
                fnames['batting'] = 'batting_scorecard.csv'
                fnames['bowling'] = 'bowling_scorecard.csv'
                fnames['match_details'] = "match_scorecard.csv"
                fnames['total'] = 'total_scorecard.csv'

            if not check_url_exists(url, 'save_csv.txt'):
                save_df_to_csv(match_df, fnames['match_details'])
                save_df_to_csv(total_df, fnames['total'])
                save_df_to_csv(batting_df, fnames['batting'])
                save_df_to_csv(bowling_df, fnames['bowling'])

                with open('checkpoints/save_csv.txt', 'w') as file:
                    # Write the URL to the file
                    file.write(url)

                print("SAVING DONE")
            else:
                print("stopping saving as last saved url reached")
                sys.exit(0)

        elif method == "json":
            if not fnames or not any(value == False for value in [True if key in fnames else False for key in ['batting', 'bowling', 'match_details', 'total']]):
                print("Saving with default file names as file names are not provided")
                fnames['batting'] = 'batting_scorecard.json'
                fnames['bowling'] = 'bowling_scorecard.json'
                fnames['match_details'] = "match_scorecard.json"
                fnames['total'] = 'total_scorecard.json'

            if not check_url_exists(url, 'save_json.txt'):
                save_df_to_json(match_df, fnames['match_details'])
                save_df_to_json(total_df, fnames['total'])
                save_df_to_json(batting_df, fnames['batting'])
                save_df_to_json(bowling_df, fnames['bowling'])

                with open('checkpoints/save_json.txt', 'w') as file:
                    # Write the URL to the file
                    file.write(url)

                print("SAVING DONE")
            else:
                print("stopping saving as last saved url reached")
                sys.exit(0)
            
        elif method == 'sql':
            if conn:
                if not fnames or not any(value == False for value in [True if key in fnames else False for key in ['batting', 'bowling', 'match_details', 'total']]):
                    print("Saving with default table names as file names are not provided")
                    fnames['batting'] = 'batting_scorecard'
                    fnames['bowling'] = 'bowling_scorecard'
                    fnames['match_details'] = "match_scorecard"
                    fnames['total'] = 'total_scorecard'

                if not check_url_exists(url, 'save_sql.txt'):
                    save_df_to_sql(match_df, fnames['match_details'], conn, schema_mappings['match_details'])
                    save_df_to_sql(total_df, fnames['total'], conn, schema_mappings['total'])
                    save_df_to_sql(batting_df, fnames['batting'], conn, schema_mappings['batting'])
                    save_df_to_sql(bowling_df, fnames['bowling'], conn, schema_mappings['bowling'])

                    with open('checkpoints/save_sql.txt', 'w') as file:
                        # Write the URL to the file
                        file.write(url)

                    print("SAVING DONE")
                else:
                    print("stopping saving as last saved url reached")
                    sys.exit(0)
            else:
                print("for sql conn ins not provided SAVING FAILED . TRY AGAIN")
        else:
            print("SAVE ERROR : required Parameters are not provided")
    
    except Exception as err:
        print("Error saving :", err)

def get_dates(start_date:str = None,end_date:str = None,start_month:str = None,end_month:str = None,start_year:str = None,end_year:str = None):
        
        try:
            # Create a list to store the dates between start and end dates
            dates_between = [] 
            # Get the current year
            current_year = datetime.now().year
            # Map month names (in lowercase) to their corresponding numerical representations
            month_map = {"jan": 1, "feb": 2, "mar": 3, "apr": 4, "may": 5, "jun": 6,"jul": 7, "aug": 8, "sep": 9, "oct": 10, "nov": 11, "dec": 12}

            if start_date and end_date:
                #Parse start and end dates into datetime objects
                start_date = datetime.strptime(start_date, "%d-%m-%Y")
                end_date = datetime.strptime(end_date, "%d-%m-%Y")

                if start_date < end_date : 
                    dates_between = get_dates_between(start_date,end_date)
                else:
                    print("Start date date cannot be higher than End date")
                    sys.exit(0)

            elif start_date:
                dates_between.append(start_date)

            elif start_month and end_month:
                # Get the numerical representation of start and end months
                start_month_num = month_map[start_month.lower()]
                end_month_num = month_map[end_month.lower()]

                #Define start and end dates for the specified months
                start_date = datetime(current_year, start_month_num, 1)
                end_date = datetime(current_year, end_month_num % 12 + 1, 1) - timedelta(days=1)

                dates_between =  get_dates_between(start_date,end_date)

            elif start_month:
                # Get the numerical representation of the month
                month_num = month_map[start_month.lower()]

                # Get the current year and month
                current_year = datetime.now().year
                current_month = month_num #datetime.now().month
                # Construct the start date of the month
                start_date = datetime(current_year, current_month, 1)

                # Calculate the last day of the month
                if current_month == 12:
                    next_month_year = current_year + 1
                    next_month = 1
                else:
                    next_month_year = current_year
                    next_month = current_month + 1
                end_date = datetime(next_month_year, next_month, 1) - timedelta(days=1)

                dates_between = get_dates_between(start_date=start_date,end_date=end_date)

            elif start_year and end_year:
                # Define the start and end dates
                start_date = datetime(start_year, 1, 1)
                end_date = datetime(end_year + 1, 1, 1) - timedelta(days=1)

                dates_between = get_dates_between(start_date=start_date,end_date=end_date)
            elif start_year:
                # Define the start and end dates for the year
                start_date = datetime(start_year, 1, 1)
                end_date = datetime(start_year, 12, 31)

                dates_between = get_dates_between(start_date=start_date,end_date=end_date)
            else:
                print("Either start_date or start_month or from_year need to be provided : \n exiting ...")
                sys.exit(0)
        
        except Exception  as err:
            print("""Error occured : provided input is wrong 
            if your are providing Date format is 'xx-xx-xxxx'.
            if you are providing data in mon use "JAN" or "january"
            Error: 
            """,err)
        finally:
            return dates_between