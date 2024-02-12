import sys
from datetime import datetime,timedelta
from scorecard import ScoreCard
import utils


class ScrapeDates:
    def __init__(self):
        pass

    def scrape_url(self, url):
        all_stats  = ()
        sc = ScoreCard()
        result = sc.collect_stats(url)
        if result:
            all_stats =  sc.get_stats()
        
        return all_stats
        
    def get_scraped_list(self, dates_list):
        dfs_list = []
        url_list = []
        if dates_list:
            for current_date in dates_list:
                if current_date:
                    main_url = "https://www.espncricinfo.com/live-cricket-match-results?date=" + current_date
                    
                    url_dict = utils.get_urls_on_date(main_url, current_date)
                    for score_url in url_dict[current_date]:
                        if score_url:
                            print(f"Scraping data using '{score_url}' for date: '{current_date}'")
                            dfs_tuple = self.scrape_url(score_url)
                            if dfs_tuple:
                                dfs_list.append(dfs_tuple)
                                url_list.append(score_url)
                            
        else:
            print("Provided Dates list is empty")

        return (url_list,dfs_list)
    
    def scrape_daily(self):
        current_date = datetime.now()

        # Format the date as "DD-MM-YYYY"
        date = current_date.strftime("%d-%m-%Y")
        dates_list = utils.get_dates(start_date=date)
        return self.get_scraped_list(dates_list)

    def scrape_date(self,start_date,end_date):
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
        

        
        

            

    
   