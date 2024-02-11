import sys
from datetime import datetime,timedelta
from scorecard import ScoreCard
import utils


class ScrapeDates:
    def __init__(self):
        self.dfs_list = []
        self.url_list = []

    def scrape_url(self, url):
        sc = ScoreCard()
        result = sc.collect_stats(url)
        if result:
            return sc.get_all_stats()
        else:
            return None

    def get_scraped_list(self, dates_list):
        if dates_list:
            for current_date in dates_list:
                if current_date:
                    main_url = "https://www.espncricinfo.com/live-cricket-match-results?date=" + current_date
                    
                    url_dict = utils.get_urls_on_date(main_url, current_date)
                    for score_url in url_dict[current_date]:
                        if score_url:
                            print(f"Scraping data using '{score_url}' for date: '{current_date}'")
                            dfs_tuple = self.scrape_url(score_url)
                            print(dfs_tuple)
                            if dfs_tuple:
                                self.dfs_list.append(dfs_tuple)
                                self.url_list.append(score_url)
                            
        else:
            print("Provided Dates list is empty")

        return self.url_list, self.dfs_list
    
    def scrape_daily(self):
        current_date = datetime.now()

        # Format the date as "DD-MM-YYYY"
        date = current_date.strftime("%d-%m-%Y")
        dates_list = utils.get_dates(start_date=date)
        return self.get_scraped_list(dates_list)

    def scrape_date(self,start_date,end_date):
        print("s",start_date,end_date)
        dates_list = utils.get_dates(start_date=start_date, end_date=end_date)
        return self.get_scraped_list(dates_list)

    def scrape_current_month(self):
        current_month = datetime.now().month
        dates_list = utils.get_dates(start_month=current_month)
        return self.get_scraped_list(dates_list)

    def scrape_month(self, start_month, end_month):
        dates_list = utils.get_dates(start_month=start_month, end_month=end_month)
        return self.get_scraped_list(dates_list)

    def scrape_current_year(self):
        current_year = datetime.now().year
        dates_list = utils.get_dates(start_year=current_year)
        return self.get_scraped_list(dates_list)

    def scrape_year(self, start_year, end_year):
        dates_list = utils.get_dates(start_year=start_year, end_year=end_year)
        return self.get_scraped_list(dates_list)
        


'''   
if __name__ == "__main__":
    
    sc = ScrapeDates()
    # Get the current date
    current_date = datetime.now()

    # Format the date as "DD-MM-YYYY"
    date = current_date.strftime("%d-%m-%Y")

    dates_list = utils.get_dates(start_date="08-02-2024", end_date=date)
    #print("date_list : ",dates_list)

    print("current_month:",datetime.now().month)
    print(f'{"*"*10} SCRAPING DATA{"*"*10}')
    url_list,dfs_list = sc.scrape_date(start_date='08-02-2024',end_date=date)

    for index,df_tuple in enumerate(dfs_list):
        if df_tuple:
            utils.save_scorecard(url_list[index],df_tuple,method = 'csv')
'''

        
        

            

    
   