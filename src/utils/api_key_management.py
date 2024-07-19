import json
import logging
from dotenv import load_dotenv
import os

def setup_logging():
    logging.basicConfig(filename='captain.log', level=logging.INFO,
                        format='%(asctime)s - %(levelname)s - %(message)s')

def load_api_key():
    load_dotenv()
    api_key = os.getenv('OPENAI_API_KEY')
    if api_key:
        logging.info("Loaded API key from environment variable")
        return api_key
    else:
        try:
            with open('api_key.txt', 'r') as f:
                api_key = f.read().strip()
                if api_key:
                    logging.info("Loaded API key from file")
                return api_key
        except FileNotFoundError:
            logging.info("API key file not found")
            return None

def save_api_key(api_key):
    with open('api_key.txt', 'w') as f:
        f.write(api_key)
    logging.info("API key saved")
