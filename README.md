Auto ria resource parser. The project uses the Selenium library as the main parsing tool. Parsing works in several threads. The number of threads is set by the BOT_NUMBERS environment variable. You also need to specify the CHROME_PROFILE_PATH variable to determine the path to create chrome browser profiles for each thread. 

The parser creates a main driver that is responsible for reading links to cars and passes a list of these links to worker threads for processing. Worker threads read information from the page and insert the data into the database. The main driver operates in open mode (headless=False), the remaining threads operate in hidden mode. My local variable example:

CHROME_PROFILE_PATH=/home/oleg

BOT_NUMBERS=4

To run the project use the following commands:

Build:
```shell
docker-compose build
```
Run:
```shell
docker-compose up
```