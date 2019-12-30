from kijiji import run
from config import directory


# this script is intended to scrape Kijiji webpages and create a .csv file showing all listings within your criteria
# this is an optional script that is not required to be used on your server, although it is pretty handy

search = input("Enter your search ==>  ")
floor = float(input("Enter your floor price ==>  "))
ceiling = float(input("Enter your ceiling price ==>  "))
pages = int(input("Enter number of pages to scrape ==>  "))

dataframe = run(search, pages, floor, ceiling)
dataframe.to_csv(directory + search + ".csv", index=False)
