from datetime import datetime,timedelta
from cricscoredigger import CricScoreDigger


if __name__ == "__main__":
    csd = CricScoreDigger()
     # Get the current date
    current_date = datetime.now()

    # Format the date as "DD-MM-YYYY"
    date = current_date.strftime("%d-%m-%Y")

    #dates_list = csd.get_dates(start_date="08-02-2024", end_date=date)
    #print("date_list : ",dates_list)

    print("current_month:",date)
    print(f'{"*"*10} SCRAPING DATA{"*"*10}')
    print(csd.scrape_date(start_date='08-02-2024', end_date=date))
    url_list,dfs_list = csd.scrape_date(start_date='08-02-2024', end_date=date)

    for index,df_tuple in enumerate(dfs_list):
        if df_tuple:
            csd.save_scorecard(url_list[index],df_tuple,method = 'csv')