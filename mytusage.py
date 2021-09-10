import configparser
import os
import re
import sys

import apprise
import dateparser
import mechanicalsoup
from bs4 import BeautifulSoup

__author__ = 'sjdvda'


def get_myt_usage():
    configfile = 'config.ini'

    config = configparser.ConfigParser()

    # Check if config file exists
    if not (os.path.isfile(configfile)):
        print("Error: Config file not found.")
        sys.exit(1)
    else:
        config.read(configfile)

    # Get values from config file
    username = config['DEFAULT']['USERNAME']
    password = config['DEFAULT']['PASSWORD']
    apprise_syntax = config['APPRISE']['SYNTAX']
    time_format = config['FORMAT']['TIME']
    threshold = config['DEFAULT']['THRESHOLD']

    # Create apprise object
    apprise_object = apprise.Apprise()
    apprise_object.add(apprise_syntax)

    # Set browser
    browser = mechanicalsoup.StatefulBrowser()

    # Login to my.t website
    browser.open("https://internetaccount.myt.mu")

    # Enter credentials
    login_form = browser.select_form('#id3')
    browser["signInForm.username"] = username
    browser["signInForm.password"] = password

    # Sign in
    login_form.choose_submit('signInContainer:submit')
    browser.submit_selected()

    # Load page
    page = browser.get_current_page()

    # For debugging:
    # browser.launch_browser()

    # Check if login is successful
    login_verify = page.select("#ContentBody")

    if login_verify:
        # Get values from page
        stats = (page.find_all("table")[5]).find_all("table")[1].find_all("td", bgcolor="#FFFFFF")

        # Extract remaining volume allowance and expiry date
        remaining_allowance = stats[5]
        expiry_date = stats[6]

        # Extract the value and convert to GB
        gb_amount = float(re.findall(r'\d*\.?\d+', remaining_allowance.text)[0]) * float(0.001)
        gb_amount_readable = str(round(gb_amount, 1)) + " GB"

        # Date conversion
        convert_date = dateparser.parse(expiry_date.text, settings={'TIMEZONE': 'GMT+4'})

        if time_format == "12h":
            converted_date = convert_date.strftime("%d/%m/%Y - %I:%M %p")
        elif time_format == "24h":
            converted_date = convert_date.strftime("%d/%m/%Y - %H:%M")
        else:
            print("Error: Invalid Time Format.")
            sys.exit(1)

        message = 'Remaining Data: ' + gb_amount_readable + '\nExpiry: ' + converted_date

        if threshold == '0' or float(threshold) <= gb_amount:
            # Send notification
            apprise_object.notify(
                body=message,
                title='my.t Data Usage'
            )
        elif float(threshold) > gb_amount:
            print("Value Above Threshold")
            sys.exit(0)
        else:
            print("Invalid Threshold Value")
            sys.exit(1)

        print(message)

    # If login fails, print error message from my.t portal
    else:
        error_message = page.select(".feedbackPanelERROR")[0]
        print("Error: Login Failed. ", error_message.text)
        sys.exit(1)


if __name__ == '__main__':
    get_myt_usage()
