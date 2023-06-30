# MLB Data Scraping & Pipeline

## Task
Select two related data sources that you find interesting. One should be a public API, and the other can be any data source of your choice, such as another public API, web scraping target, or static file. Ensure that the chosen data sources provide relevant information for solving a problem.

## Idea
Use ESPN scraping to get batting leaders. Use wikipedia API to get bio/summary (&more) of a player. Join data together in a single data source.

## Tech Stack
Python, DocumentDB, MongoDB, AWS Cloud9

Overall, Python is used for implementing the data scraping and processing logic, AWS DocumentDB is used for database operations and storage, and AWS Cloud9 is used as the development environment for hosting/running the code. This combination of technologies enables efficient development, data storage, and execution of the code in a cloud-based environment.

AWS DocumentDB: AWS DocumentDB is a fully managed NoSQL database service provided by Amazon Web Services (AWS). It is compatible with MongoDB, which means you can use existing MongoDB applications and tools with DocumentDB. In the code, AWS DocumentDB is used for connecting to the MongoDB cluster, performing database operations, and storing player data.

AWS Cloud9: AWS Cloud9 is an integrated development environment (IDE) provided by AWS. It allows you to write, run, and debug code directly in your web browser. Cloud9 provides a complete development environment with features like code editing, terminal access, and collaboration tools. In the code, AWS Cloud9 is used as the development environment for writing and running the Python code.

![Screen Shot 2023-06-30 at 1 11 30 PM](https://github.com/ndrishinski/baseball_scraping/assets/24279724/a761dad3-8883-47a5-96dc-576f25aefc89)

## Installation

Use the package manager [pip](https://pip.pypa.io/en/stable/) to install bs4, wikipedia and datetime

```bash
pip install beautifulsoup4 wikipedia datetime
```


## License

[MIT](https://choosealicense.com/licenses/mit/)
