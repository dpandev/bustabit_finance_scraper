"""
Web Scraper
"""

import random
import time
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from bs4 import BeautifulSoup
import pandas as pd
# Imports modules that check for fully-loaded webpage
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import os.path
import options

# options for CSV EXPORT
# TODO read input from options.txt and assign values to these variables (instead of T/F values)
# TODO create different customized version of CVS export way below to accomodate these options
option1 = options.dates
option2 = options.times
option3 = options.games
option4 = options.bustaNums
option5 = options.bets
option6 = options.users
option7 = options.cashedOut
option8 = options.profits
option9 = options.betIDs
opList = [option1, option2, option3, option4, option5, option6, option7, option8, option9]

def main():

    # Identifying which games to scrap
    starting_game = options.starting_game  # NOTE: Enter manually which game to start scraping first
    number_of_games = options.number_of_games  # NOTE: Enter manually how many games to scrap in total
    counter = 1  # For loop tracking purposes

    # Declaring arrays to hold info (for csv export)
    gameID = starting_game
    games = []
    dates = []
    times = []
    bustaNums = []
    users = []
    bets = []
    cashedOut = []
    profits = []
    betNums = []

    # Looping through each requested game
    for game_id in range(starting_game, starting_game + number_of_games):
        # updates for for csv export and printouts
        gameID = game_id

        # Anti-ban guard for delaying loop cycle
        time_delay = random.random() * 24  # Aiming for an average of 12 seconds
        time.sleep(time_delay)
        print("Time Delay: " + str(time_delay))

        # Anti-ban guard for randomizing polling frequency (default is 0.5 seconds)
        time_delay_polling = random.random() * 16 + 1.6  # Aiming for an average of 8 seconds
        print("Time Delay Polling: " + str(time_delay_polling))

        # Identifying website address to target
        url = "https://www.bustabit.com/game/" + str(game_id)

        dr_options = Options()
        options.headless = True
        driver = webdriver.Firefox(firefox_options=dr_options,
                                   executable_path="./geckodriver.exe")  # Point to geckodriver.exe
        driver.get(url)

        try:
            # Waits until the page is fully loaded
            WebDriverWait(driver, timeout=300, poll_frequency=time_delay_polling).until(
                EC.presence_of_element_located((By.CLASS_NAME, "history-table")))
        finally:
            # Verify that page sources are valid:
            if "Hash:" in driver.page_source:
                print("File is Good.")
                status = 'good'

            else:
                print("File is Corrupt.")
                status = 'corrupt'

        if status == 'good':
            print("Beginning data extraction... --> (file " + str(counter) + " of " + str(
                number_of_games) + ")")
            # DATA EXTRACTION
            # Loads page content into a string to be read
            content = driver.page_source
            soup = BeautifulSoup(content, "lxml")
            bust = str(soup.find('div', attrs={'class': 'modal-content'}))
            table = str(soup.find('table', attrs={'class': 'history-table'}))

            # grabs busted at number
            pos = bust.find('Busted at:', 0) + 38
            posEnd = bust.find('</span></h5><h5>')
            bustedAt = bust[pos:posEnd]
            bustaNums.append(bustedAt)

            # grabs date
            pos = bust.find('GMT', 0) - 26
            posEnd = pos + 16
            date = bust[pos:posEnd]
            dates.append(date)

            # grabs time
            pos = posEnd + 1
            posEnd = pos + 9
            timer = bust[pos:posEnd]
            times.append(timer)

            # adds game to array
            games.append(gameID)

            if options.specific_user:
                # Finds specific user
                user = options.user_name + '">'
                pos = table.find(user, 0) - user.length
                posEnd = table.find('">', pos)
            else:
                # Adds all users found to the list
                pos = table.find('href="/user/', 0) + 13
                posEnd = table.find('">',pos)
                user = table[pos:posEnd]
                users.append(user)

            # Finds bets and adds to array
            pos = table.find('<td>', posEnd) + 4
            posEnd = table.find('</td>', pos)
            bet = table[pos:posEnd]
            bets.append(bet)

            # Finds cashed out and adds to array
            pos = table.find('<td>', posEnd) + 4
            posEnd = table.find('</td>', pos)
            cashOut = table[pos:posEnd]
            cashedOut.append(cashOut)

            # Finds profit and adds to array
            pos = table.find('<td>', posEnd) + 4
            posEnd = table.find('</td>', pos)
            profit = table[pos:posEnd]
            profits.append(profit)

            # Finds bet number
            pos = table.find('/bet/', posEnd) + 5
            posEnd = table.find('">Bet', pos)
            betNum = table[pos:posEnd]
            betNums.append(betNum)
            counter += 1
        else:
            print("Skipping corrupted file...")
            print("Corrupted GameID: " + str(gameID))
            counter += 1

        # Closing Selenium driver
        driver.quit()

    # Export to csv
    # TODO fix formatting, variable names, make everything match up cleaner
    frameString = '{'
    for x in opList:
        if x:
            # add option to dataframe
            frameString += "'Date': dates, "

    df = pd.DataFrame(
        {'Date': dates, 'Time': times, 'Game ID': games, 'Busted At': bustaNums, 'Bets': bets,
            'Cashed Out': cashedOut, 'Profits': profits, 'Bet #': betNums})
    df.to_csv('bustabit-history-' + str(starting_game) + '_' + str(
        starting_game + number_of_games) + '.csv', index=False, encoding='utf-8')

    # Indicate completion
    print("All requested data has been downloaded and saved.")


if __name__ == "__main__":
    print("Executing main...")
    main()