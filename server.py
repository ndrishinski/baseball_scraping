import requests
from bs4 import BeautifulSoup
import wikipedia as wk
from pymongo import MongoClient
import datetime
import logging
from dotenv import dotenv_values

env_vars = dotenv_values('.env')
class BaseballStatsScraper:
    def __init__(self):
        # Define DB connection details
        self.username = env_vars['USERNAME']
        self.password = env_vars['PASS']
        self.cluster_endpoint = env_vars['MONGODB']
        self.ssl_cert_file = 'global-bundle.pem'  # Path to the SSL certificate file
        self.database_name = 'baseball'
        self.collection_name = 'hitting_leaders'
        self.scraper_url = 'https://www.espn.com/mlb/stats/player'
        self.parsed_html = None
        self.collection = None
        # Configure error logging to file
        logging.basicConfig(filename='error.log', level=logging.ERROR)

    def connect_to_db(self):
        try:
            client = MongoClient(self.cluster_endpoint, username=self.username, password=self.password, ssl=True, tlsCAFile=self.ssl_cert_file)
            db = client[self.database_name]
            collection = db[self.collection_name]
            self.collection = collection
            print("Connected to MongoDB successfully!")
            return collection
        except Exception as e:
            print(f"Error connecting to MongoDB: {str(e)}")
            logging.error('Error connecting to DB', exc_info=True)
            return None
            
    def scrape_and_parse_html(self):
        # Step 1: Scrape player names from ESPN MLB stats website
        try:
            response = requests.get(self.scraper_url)
            self.parsed_html = BeautifulSoup(response.content, "html.parser")
            return self.parsed_html
        except Exception as e:
            print(f"Error connecting to MongoDB: {str(e)}")
            logging.error('Error connecting to DB', exc_info=True)
            return None

    def scrape_player_names(self):
        # ensure the parsed html exists and declare list that will hold all players names
        self.scrape_and_parse_html()
        player_names = []

        # Extract player names and summaries
        name_rows = self.parsed_html.select("#fittPageContainer > div:nth-child(3) > div > div > section > div > div:nth-child(4) > div.ResponsiveTable.ResponsiveTable--fixed-left.mt4.Table2__title--remove-capitalization > div > table > tbody > tr")
        stat_categories = self.parsed_html.select("#fittPageContainer > div:nth-child(3) > div > div > section > div > div:nth-child(4) > div.ResponsiveTable.ResponsiveTable--fixed-left.mt4.Table2__title--remove-capitalization > div > div > div.Table__Scroller > table > thead > tr > th.Table__TH")

        for row in name_rows:
            name = row.select('a.AnchorLink')[0].text
            team = row.select('span.athleteCell__teamAbbrev')[0].text

            try:
                summary = wk.summary(f"{name}, baseball player")  # Search Summary
                player_names.append({
                    "name": name,
                    "summary": summary
                })
            except Exception as e:
                player_names.append({
                    "name": name,
                    "summary": 'Sorry - no summary is available.'
                })
                print(f"Unable to retrieve summary for {name}: {e}")
                continue

        return player_names
        
    def scrape_player_stats(self, player_names):
      current_date = datetime.datetime.now()

      stat_categories = self.parsed_html.select("#fittPageContainer > div:nth-child(3) > div > div > section > div > div:nth-child(4) > div.ResponsiveTable.ResponsiveTable--fixed-left.mt4.Table2__title--remove-capitalization > div > div > div.Table__Scroller > table > thead > tr > th.Table__TH")
        # first looping thru the player names 
      for index, player in enumerate(player_names):
          # then looping thru the row of stats and adding each one to the player's object, along with a rank and date.
          for stat, num in enumerate(stat_categories):
              try:
                  # temp_stats_for_player is each cell
                  temp_stats_for_player = self.parsed_html.select(f"#fittPageContainer > div:nth-child(3) > div > div > section > div > div:nth-child(4) > div.ResponsiveTable.ResponsiveTable--fixed-left.mt4.Table2__title--remove-capitalization > div > div > div.Table__Scroller > table > tbody > tr:nth-child({index + 1}) > td")
                  player_names[index][num.text] = temp_stats_for_player[stat].text
                  player_names[index]['date'] = current_date.strftime('%Y-%m-%d %H:%M:%S')
                  player_names[index]['rank'] = index + 1
              except Exception as e:
                  print(f"Error scraping player stats: {str(e)}")
                  logging.error('Error scraping player stats', exc_info=True)
                  continue
          try:
              # adding the dict to the DB
            result = self.collection.insert_one(player_names[index])
            print(f"{index}. RESULT: {result} end \n")
          except Exception as e:
            print(f'{index}. Failure adding result to database: {e}. See player: {player}')
            continue

      return player_names
      
if __name__ == "__main__":
    # Create an instance of the BaseballStatsScraper class
    scraper = BaseballStatsScraper()

    # Call the methods of the scraper instance
    scraper.connect_to_db()
    names = scraper.scrape_player_names()
    scraper.scrape_player_stats(names)