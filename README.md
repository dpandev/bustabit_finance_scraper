# Bustabit Finance Scraper (with Python)
Scrapes historical game data from the [bustabit](https://www.bustabit.com/) site and exports data into a CSV.

This project utilizes the python libraries [Selenium](https://github.com/SeleniumHQ/Selenium), [BeautifulSoup](https://www.crummy.com/software/BeautifulSoup/), and [Pandas](https://pandas.pydata.org/). The script scrapes data from each game listed on the site with a user-defined starting game number and number of games (to scrape). There is a random delay which prevents the scripts from sending too many requests to the site.

The [Mozilla GeckoDriver](https://github.com/mozilla/geckodriver) is also used in pair with Selenium.

----------

## Running the Script

First, install the requirements. (Also make sure to download the correct version of GeckoDriver for your specific OS and place it in the project directory).

```
$ pip install -r requirements.txt
```

Edit the following variables in options.txt to scrape specific games in a chronologically increasing order.

```
starting_game = 2351255
number_of_games = 2
```

Run the script.

```
$ python bustabit_scraper.py  (for Mac OS)

$ python.exe bustabit_scraper.py  (for Windows)
```

That's it.

The script will export the data to a CSV in the project directory.

-------
## Additional Exporting Options

If you want to export specific user data from the site, edit the options.txt based on the instructions below:

To export game history data of a specific user:

```
specific_user = True  (set value to True)
user_name = username_example  (replace with username)
```

You can also choose which data to extract and export to CSV:
(Each value represents a specific column of data)

```
games  = true   //specific game id
dates = true    //date of the specific game
times = true    //time of the specific game
bustaNums = true //number at which game busted
users = false   //to list all users that participated in game
bets = true     //bet amount (in bits)
cashedOut = true //cash out multiplier
profits = true  //profit amount (in bits)
betNums = true  //specific bet id
```

Make sure to save the changes made to options.txt before running the script!