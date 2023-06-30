import unittest
from unittest.mock import patch
from bs4 import BeautifulSoup
from server import BaseballStatsScraper

class TestBaseballStatsScraper(unittest.TestCase):
    def setUp(self):
        # Initialize the BaseballStatsScraper instance for testing
        self.scraper = BaseballStatsScraper()

    @patch('server.MongoClient')  # Mock MongoClient for testing
    def test_connect_to_db(self, mock_mongo_client):
        # # Create an instance of BaseballStatsScraper
        # self.scraper = BaseballStatsScraper()

        # Call the connect_to_db method
        self.scraper.connect_to_db()

        # Assert that MongoClient was called with the correct arguments
        mock_mongo_client.assert_called_once_with(
            'docdb-2023-06-25-20-52-07.cluster-ctsbnohmpqnq.us-east-2.docdb.amazonaws.com',
            username='ndrishinski',
            password='VerySecurePassword123',
            ssl=True,
            tlsCAFile='global-bundle.pem'
        )
    
    def test_scrape_and_parse_html_returns_valid_html(self):
        # Test if the scrape_and_parse_html method returns valid HTML
        parsed_html = self.scraper.scrape_and_parse_html()

        # Assert that the parsed_html is not None
        self.assertIsNotNone(parsed_html)

        # Assert that the parsed_html is of type 'bs4.BeautifulSoup'
        self.assertIsInstance(parsed_html, BeautifulSoup)

    def test_scrape_player_names_returns_valid_data(self):
        # Test if the scrape_player_names method returns a valid list of player names
        player_names = self.scraper.scrape_player_names()

        # Assert that player_names is not None
        self.assertIsNotNone(player_names)

        # Assert that player_names is a list
        self.assertIsInstance(player_names, list)

        # Assert that each player in player_names is a dictionary
        for player in player_names:
            self.assertIsInstance(player, dict)

            # Assert that each player dictionary has 'name' and 'summary' keys
            self.assertIn('name', player)
            self.assertIn('summary', player)

            # Assert that 'name' and 'summary' values are not empty
            self.assertNotEqual(player['name'], '')
            self.assertNotEqual(player['summary'], '')
            
    def test_scrape_player_stats_returns_valid_data(self):
        # Call the scrape_player_stats method
        player_names = self.scraper.scrape_player_names()
        player_stats = self.scraper.scrape_player_stats(player_names)

        # Assert that player_stats is not None
        self.assertIsNotNone(player_stats)

        # Assert that player_stats is a list
        self.assertIsInstance(player_stats, list)

        # Assert that each player in player_stats is a dictionary
        for player in player_stats:
            print(f'Player: {player}')
            self.assertIsInstance(player, dict)

            # Assert that 'rank', 'date', and 'stat_categories' keys exist
            self.assertIn('rank', player)
            self.assertIn('date', player)

            # Assert that 'rank' and 'date' values are not empty
            self.assertNotEqual(player['rank'], '')
            self.assertNotEqual(player['date'], '')

    

if __name__ == '__main__':
    unittest.main()