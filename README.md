# Crawling School Webpage

This project consists of three Python files: `main.py`, `args.py`, and `crawler.py`. Below are the descriptions of their functionalities.

## main.py

`main.py` is the main program file responsible for executing the logic of the entire program. Its functionalities include:

- Reading input parameters
- Calling `args.py` to parse the input parameters
- Calling `crawler.py` to crawl the announcements from the NTU website
- Writing the crawled announcement information to a file

## args.py

`args.py` is the file used to parse input parameters. Its functionalities include:

- Parsing the command-line arguments provided by the user
- Providing the parsed arguments for use by other modules

## crawler.py

`crawler.py` is the file used to crawl announcements from the NTU website. Its functionalities include:

- Using the LXML library to parse webpage content
- Crawling announcements from the NTU website
- Returning the crawled announcement information for use by `main.py`
