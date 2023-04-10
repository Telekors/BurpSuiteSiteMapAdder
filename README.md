# BurpSuiteSiteMapAdder

The following is a simple python script to take an input list of websites and generate the site map in Burpsuite quickly and efficently. 

## Install
`pip install -r requirements.txt`

## Usage

```
Usage:
  web_request.py <input_file> [--proxy=<proxy>] [--retries=<retries>] [--timeout=<timeout>] [--threads=<threads>]
Options:
  --proxy=<proxy>          Proxy to use for requests in the format 'http://<host>:<port>' [default: http://localhost:8080]
  --retries=<retries>      Number of retries for failed requests [default: 3]
  --timeout=<timeout>      Timeout for each request in seconds [default: 10]
  --threads=<threads>      The number of threads to use [default: 4]
  ```
