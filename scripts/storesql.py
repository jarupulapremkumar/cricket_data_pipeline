import mysql.connector
import utils

def save_with_python_connector(url,df,table_name,conn):

    #print(url,table_name)
    # Create a cursor object
    cursor = conn.cursor()
    # Iterate over each row in the DataFrame and insert it into the MySQL table
    if df is not None:
        for index,row in df.iterrows():
            #print("list",list(row.index))
            
            # Define your insert query
            # Define your insert query dynamically based on column names
            insert_query = f"INSERT INTO {table_name} ("
            insert_query += ", ".join(list(row.index))
            insert_query += ") VALUES ("
            insert_query += ",".join([f'"{value}" ' if value is not None else "null" for value in row.values])
            insert_query += ")"

            #print(insert_query)

            
            # Execute the insert query
            #cursor.execute(insert_query, tuple(row.values))
            cursor.execute(insert_query)

        # Commit the changes
        conn.commit()

        # Close the cursor and connection
        cursor.close()

        with open('checkpoints/save_sql.txt', 'w') as file:
            # Write the URL to the file
            file.write(url)

        print("SAVING DONE")
    else:
        print("df is none unable to save")
    

def save_scorecard_checked(url_list: list, dfs_tuple_list: list, config:dict,fnames: dict = None):
    """
    Save the scraped scorecard to files with checks last url saved.it will stop if that url matches current url else saves the data

    Args:
    - url_list (list): List of URLs.
    - dfs_tuple_list (list): List of tuples containing scraped data.
    - method (str): Method to save the data (e.g., 'csv', 'json', 'sql').
    - fnames (dict): Dictionary containing file names for different types of data.
    - conn: Database connection object.

    Returns:
    - None
    """
    
    if not fnames:
            fnames = {}

    # Check if the URL exists and save the data accordingly
    if not utils.check_url_exists(url_list[-1],'save_sql.txt'):
        # Connect to MySQL server
        cnx = mysql.connector.connect(**config)

        for url, dfs_tuple in zip(url_list, dfs_tuple_list):
            #print(dfs_tuple)

            match_df, total_df, batting_df, bowling_df,fall_of_wickets_df = dfs_tuple
            if cnx.is_connected():
                print("Saving Files for",url,"...........")
                if not fnames or not any(value == False for value in [True if key in fnames else False for key in ['batting', 'bowling', 'match_details', 'total','fall_of_wickets']]):
                    print("Saving with default table names as file names are not provided")
                    fnames['batting'] = 'batting_scorecard'
                    fnames['bowling'] = 'bowling_scorecard'
                    fnames['match_details'] = "match_scorecard"
                    fnames['total'] = 'total_scorecard'
                    fnames['fall_of_wickets'] = 'fall_of_wickets'

                    if match_df is not None :
                        save_with_python_connector(url,match_df,fnames['match_details'],cnx)
                    if total_df is not None :
                        save_with_python_connector(url,total_df,fnames['total'],cnx)
                    if batting_df is not None :
                        save_with_python_connector(url,batting_df,fnames['batting'],cnx)
                    if bowling_df is not None :
                        save_with_python_connector(url,bowling_df,fnames['bowling'],cnx)
                    if fall_of_wickets_df is not None :
                        save_with_python_connector(url,fall_of_wickets_df,fnames['fall_of_wickets'],cnx)
        cnx.close()

                
    else:
        print("Not Saving as last saved url is reached") 
    

def save_scorecard_unchecked(url_list: str, dfs_tuple_list: tuple, config:dict,fnames: dict = None, ):
    """
    Save the scraped scorecard to files without checking what is last url.

    Args:
    - url_list (list): List of URLs.
    - dfs_tuple_list (list): List of tuples containing scraped data.
    - method (str): Method to save the data (e.g., 'csv', 'json', 'sql').
    - fnames (dict): Dictionary containing file names for different types of data.
    - conn: Database connection object.

    Returns:
    - None
    """
    if not fnames:
        fnames = {}
    # Connect to MySQL server
    cnx = mysql.connector.connect(**config)
    for url, dfs_tuple in zip(url_list, dfs_tuple_list):
            match_df, total_df, batting_df, bowling_df,fall_of_wickets_df = dfs_tuple
            if cnx.is_connected():
                print("Saving Files for",url,"...........")
                if not fnames or not any(value == False for value in [True if key in fnames else False for key in ['batting', 'bowling', 'match_details', 'total','fall_of_wickets']]):
                    print("Saving with default table names as file names are not provided")
                    fnames['batting'] = 'batting_scorecard'
                    fnames['bowling'] = 'bowling_scorecard'
                    fnames['match_details'] = "match_scorecard"
                    fnames['total'] = 'total_scorecard'
                    fnames['fall_of_wickets'] = 'fall_of_wickets'

                    if match_df is None :
                        save_with_python_connector(url,match_df,fnames['match_details'],cnx)
                    if total_df is None :
                        save_with_python_connector(url,total_df,fnames['total'],cnx)
                    if batting_df is None :
                        save_with_python_connector(url,batting_df,fnames['batting'],cnx)
                    if bowling_df is None :
                        save_with_python_connector(url,bowling_df,fnames['bowling'],cnx)
                    if fall_of_wickets_df is None :
                        save_with_python_connector(url,fall_of_wickets_df,fnames['fall_of_wickets'],cnx)
    cnx.close()
