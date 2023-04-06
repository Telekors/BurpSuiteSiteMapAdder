"""
Usage:
  web_request.py <input_file> [--proxy=<proxy>] [--retries=<retries>] [--timeout=<timeout>] [--threads=<threads>]

Options:
  --proxy=<proxy>          Proxy to use for requests in the format 'http://<host>:<port>' [default: http://localhost:8080]
  --retries=<retries>      Number of retries for failed requests [default: 3]
  --timeout=<timeout>      Timeout for each request in seconds [default: 10]
  --threads=<threads>      The number of threads to use [default: 4]
"""

import requests
import threading
import urllib3
from docopt import docopt
from termcolor import colored

# Disable SSL verification
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
session = requests.Session()
session.verify = False

# Function to make web request and handle errors
def make_request(websites, retries, timeout, proxy):
    for website in websites:
        try:
            # Send a request with a timeout
            response = session.get(website, timeout=timeout, proxies=proxy)
            if response.status_code == 200 or response.status_code == 302:
                print(colored(f"Response from {website}: {response.status_code}", 'green'))
            elif response.status_code == 404 or response.status_code == 403 or response.status_code == 400:
                print(colored(f"Response from {website}: {response.status_code}", 'yellow'))
            else:
                print(colored(f"Response from {website}: {response.status_code}", 'red'))
        except requests.exceptions.RequestException as e:
            print(colored(f"Failed to make request to {website}: {e}", 'red'))
            if retries > 0:
                print(f"Retrying {retries} more times...")
                make_request([website], retries-1, timeout, proxy)

def main():
    # Parse command line arguments
    args = docopt(__doc__)

    # Extract input file, proxy, retries, and timeout from command line arguments
    input_file = args['<input_file>']
    proxy_str = args['--proxy']
    retries = int(args['--retries'])
    timeout = float(args['--timeout'])
    input_threads = int(args['--threads'])

    # Read websites from input file
    with open(input_file, 'r') as file:
        websites = file.read().splitlines()

    # Divide the websites into 4 separate arrays
    #num_threads = 4
    num_threads = input_threads - 1
    websites_per_thread = len(websites) // num_threads
    website_chunks = [websites[i:i + websites_per_thread] for i in range(0, len(websites), websites_per_thread)]

    # Create proxy dictionary if proxy is provided
    proxy = None
    if proxy_str:
        proxy = {
            'http': proxy_str,
            'https': proxy_str
        }

    # Create and start threads for each website chunk
    threads = []
    for chunk in website_chunks:
        print(chunk)
        t = threading.Thread(target=make_request, args=(chunk, retries, timeout, proxy))
        threads.append(t)
        t.start()

    # Wait for all threads to finish
    for t in threads:
        t.join()

    print("All requests completed.")


if __name__ == '__main__':
    main()

