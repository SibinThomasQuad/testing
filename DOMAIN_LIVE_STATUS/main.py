import argparse
import requests
import time
from colorama import Fore, Style
from datetime import datetime
import logging
import urllib.parse
TITLE_LABEL = '''
        

  _      _             _____ _             
 | |    (_)           |  __ (_)            
 | |     ___   _____  | |__) | _ __   __ _ 
 | |    | \ \ / / _ \ |  ___/ | '_ \ / _` |
 | |____| |\ V /  __/_| |   | | | | | (_| |
 |______|_| \_/ \___(_)_|   |_|_| |_|\__, |
                                      __/ |
                                     |___/ 


'''
print(TITLE_LABEL)

# Configure logging
log_filename = None

def setup_logging(url):
    global log_filename
    domain = urllib.parse.urlparse(url).netloc
    timestamp = datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
    log_filename = f'live_{domain}_{timestamp}.log'
    logging.basicConfig(filename=log_filename, level=logging.INFO, format='%(asctime)s - %(message)s')

# Create a command line argument parser
parser = argparse.ArgumentParser(description="Continuous URL status checker")
parser.add_argument("url", help="The URL to check")

args = parser.parse_args()
url = args.url

# Record the timestamp when the script starts
start_timestamp = datetime.now()
print(f"Pinging started at {start_timestamp}")

# Setup logging
setup_logging(url)

try:
    while True:
        request_datetime = datetime.now()  # Record the current date and time for sending the request
        start_time = time.time()  # Record the start time for sending the request
        try:
            response = requests.get(url)
            response.raise_for_status()  # Raise an exception if the response is not successful
        except requests.exceptions.RequestException as e:
            end_time = time.time()
            response_time = -1  # Set a negative value to indicate an error
            message = f'Request Error: {e}'
            print(Fore.RED + message + Style.RESET_ALL)
            logging.error(message)
        else:
            end_time = time.time()  # Record the end time after receiving the response
            response_datetime = datetime.now()  # Record the current date and time for receiving the response
            http_code = response.status_code
            response_time = round((end_time - start_time) * 1000)  # Convert to milliseconds

            if http_code == 200:
                message = f'HTTP Status: {http_code} | Request Time: {request_datetime} | Response Time: {response_datetime} | Response Time: {response_time} ms'
                print(Fore.GREEN + message + Style.RESET_ALL)
                logging.info(message)
            else:
                message = f'HTTP Status: {http_code} | Request Time: {request_datetime} | Response Time: {response_datetime} | Response Time: {response_time} ms'
                print(Fore.RED + message + Style.RESET_ALL)
                logging.warning(message)

        time.sleep(1)  # Wait for 1 second before pinging the domain again
except KeyboardInterrupt:
    if log_filename:
        print(Fore.YELLOW + f"Testing Closed. Output logged to {log_filename}" + Style.RESET_ALL)
