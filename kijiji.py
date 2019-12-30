import pandas as pd
import requests
from bs4 import BeautifulSoup
from config import *
from pytz import timezone
from datetime import datetime
from smtplib import SMTP
from os import makedirs


def format_link(search):
    return kijiji + link_part_1 + search.replace(" ", "-") + link_part_2


def get_next_link(link):
    response = requests.get(link)
    soup = BeautifulSoup(response.text, "html.parser")
    next_link = soup.find(class_="pagination").find(title="Next")
    if next_link is None:
        return None
    return kijiji + next_link["href"]


def check_ad(link):
    return 'c' in link.split("/")[-1]


def scraper(url, floor, ceiling):
    array = []

    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")
    soup = soup.find_all(class_="regular-ad")

    for listing in soup:
        price = listing.find(class_="price").get_text().replace(",", "").replace("$", "").strip()
        link = kijiji + listing.find("a", href=True)["href"]
        title = listing.find("a", href=True)["href"].split("/")[-2].replace("-", " ")

        try:
            price = float(price)
            if floor <= price <= ceiling and "Wanted:" not in listing.find(class_="title").get_text().strip() and not check_ad(link):
                array.append([price, title, link])
        except ValueError:  # ignores "Please Contact", "Free", "Swap / Trade" prices
            pass

    return array


def run(search, pages, floor, ceiling):
    array = []
    url = format_link(search)

    for page in range(pages):
        array += scraper(url, floor, ceiling)
        url = get_next_link(url)

    dataframe = pd.DataFrame(array, columns=fieldnames)
    return dataframe


def send_email(subject, dataframe):
    server = SMTP(email_protocol)
    server.ehlo()
    server.starttls()
    server.login(email_address, password)

    time = datetime.now(timezone(my_timezone)).strftime("%m/%d/%Y, %H:%M:%S")
    msg = dataframe.to_string(columns=fieldnames, header=False, index=False)
    message = "Subject: {}\n\n{}".format(subject, time + "\n\n" + msg)

    server.sendmail(email_address, recipient, message)
    server.quit()


def initiate(search, pages, floor, ceiling):
    old_dataframe = pd.read_pickle(directory + search + ".pkl")
    new_dataframe = run(search, pages, floor, ceiling)

    old = old_dataframe.to_numpy()
    new = new_dataframe.to_numpy()
    array = []

    for item in new:
        if item not in old:
            array.append(item)

    if len(array) > 0:
        try:
            old_temp = pd.read_pickle(temp_dir + search + ".pkl").to_numpy()
            array += old_temp
        except FileNotFoundError:
            pass
        temp = pd.DataFrame(array, columns=fieldnames)
        temp.to_pickle(temp_dir + search + ".pkl")

    new_dataframe.to_pickle(directory + search + ".pkl")


pd.set_option("display.max_colwidth", 10000)
kijiji = "http://kijiji.ca"
fieldnames = ["Listing Name", "Price", "Link"]
temp_dir = directory + "temp" + slash

try:  # makes the proper save locations
    makedirs(directory)
    makedirs(temp_dir)
except FileExistsError:
    pass
