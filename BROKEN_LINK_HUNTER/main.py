import requests
from bs4 import BeautifulSoup
from datetime import datetime
import argparse
import logging
import signal
from colorama import Fore, Style

TITLE_LABEL = '''


██████╗░░█████╗░██╗░░██╗███████╗███╗░░██╗░░░░░░██╗░░██╗██╗░░░██╗███╗░░██╗████████╗
██╔══██╗██╔══██╗██║░██╔╝██╔════╝████╗░██║░░░░░░██║░░██║██║░░░██║████╗░██║╚══██╔══╝
██████╦╝██║░░██║█████═╝░█████╗░░██╔██╗██║█████╗███████║██║░░░██║██╔██╗██║░░░██║░░░
██╔══██╗██║░░██║██╔═██╗░██╔══╝░░██║╚████║╚════╝██╔══██║██║░░░██║██║╚████║░░░██║░░░
██████╦╝╚█████╔╝██║░╚██╗███████╗██║░╚███║░░░░░░██║░░██║╚██████╔╝██║░╚███║░░░██║░░░
╚═════╝░░╚════╝░╚═╝░░╚═╝╚══════╝╚═╝░░╚══╝░░░░░░╚═╝░░╚═╝░╚═════╝░╚═╝░░╚══╝░░░╚═╝░░░

'''

print(TITLE_LABEL)
# Configure logging
log_filename = None
stop_requested = False

def setup_logging(url):
    global log_filename
    domain = url.split('//')[1].split('/')[0].replace('.', '_')
    timestamp = datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
    log_filename = f'broken_links_{domain}_{timestamp}.log'
    logging.basicConfig(filename=log_filename, level=logging.INFO, format='%(asctime)s - %(message)s')

def check_links(url):
    try:
        response = requests.get(url)
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        print(f"Failed to retrieve the page: {e}")
        return

    soup = BeautifulSoup(response.text, 'html.parser')

    links = soup.find_all('a', href=True)

    for link in links:
        if stop_requested:
            break

        link_url = link['href']
        if not link_url.startswith('http'):
            link_url = f"{url.rstrip('/')}/{link_url.lstrip('/')}"

        request_time = datetime.now()

        try:
            link_response = requests.head(link_url)
            response_time = datetime.now()
            if link_response.status_code == 200:
                message = f'Link OK: {Fore.LIGHTBLUE_EX + link_url + Style.RESET_ALL} | Status Code: 200 | Request Time: {request_time} | Response Time: {response_time}'
                print(Fore.GREEN + message + Style.RESET_ALL)
                logging.info(message)
            else:
                message = f'Broken link: {Fore.LIGHTBLUE_EX + link_url + Style.RESET_ALL} | Status Code: {link_response.status_code} | Request Time: {request_time} | Response Time: {response_time}'
                print(Fore.RED + message + Style.RESET_ALL)
                logging.warning(message)
        except requests.exceptions.RequestException as e:
            response_time = datetime.now()
            message = f"Failed to check link {Fore.LIGHTBLUE_EX + link_url + Style.RESET_ALL}: {e} | Request Time: {request_time} | Response Time: {response_time}"
            print(Fore.RED + message + Style.RESET_ALL)
            logging.error(message)

def signal_handler(signum, frame):
    global stop_requested
    stop_requested = True
    print(Fore.YELLOW + "Testing Stopped" + Style.RESET_ALL)
    exit(0)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Broken Link Checker")
    parser.add_argument("url", help="The URL to check for broken links")

    args = parser.parse_args()
    url = args.url

    setup_logging(url)
    signal.signal(signal.SIGINT, signal_handler)  # Handle Ctrl+C to gracefully stop

    check_links(url)
    
    print(f"Results are logged to {log_filename}")
