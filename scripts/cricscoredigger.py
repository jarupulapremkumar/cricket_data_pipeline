from scorecard import ScoreCard
from scrapdates import ScrapeDates
import utils
import os

class CricScoreDigger():
    def __init__(self):
        self.sc = ScoreCard()
        self.sd = ScrapeDates()
        os.makedirs("datasets", exist_ok=True)
        os.makedirs("checkpoints", exist_ok=True)

    def scrape_keyword(self,keyword:str):
        dfs_tuple_list =[]
        all_links = utils.search_links(keyword)
        for link in all_links:
            if keyword in link:
                 dfs_tuple_list.append(self.scraping_url(link))

        return dfs_tuple_list
    
    def scrape_date(self,start_date,end_date):
        self.sd.scrape_date(start_date,end_date)
    
    def start_scrap_daily(self):
        self.sd.scrape_daily()

    def scrape_current_month(self):
         self.sd.scrape_current_month()

    def scrape_month(self, start_month, end_month):
        self.sd.scrape_month(start_month, end_month)

    def scrape_current_year(self):
        self.sd.scrape_current_year()

    def scrape_year(self, start_year, end_year):
        self.sd.scrape_year(start_year, end_year)

    def scrape_url(self,url):
        return self.scrape_url(url)
    
    def save_scorecard(self, url: str, dfs_tuple: tuple, method: str, fnames: dict = None, conn=None):
        utils.save_scorecard(url, dfs_tuple, method, fnames, conn)


    




    




                



    
