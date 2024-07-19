import unittest
from unittest.mock import patch, mock_open
from src.utils.api_key_management import load_api_key, save_api_key

class TestUtils(unittest.TestCase):
    @patch('src.utils.api_key_management.load_dotenv')
    @patch('src.utils.api_key_management.os.getenv', return_value='test_key')
    def test_load_api_key(self, mock_getenv, mock_load_dotenv):
        api_key = load_api_key()
        mock_load_dotenv.assert_called_once()
        mock_getenv.assert_called_once_with('OPENAI_API_KEY')
        self.assertEqual(api_key, 'test_key')

    @patch('builtins.open', new_callable=mock_open)
    def test_save_api_key(self, mock_file):
        save_api_key('test_key')
        mock_file.assert_called_once_with('api_key.txt', 'w')
        mock_file().write.assert_called_once_with('test_key')

if __name__ == '__main__':
    unittest.main()
