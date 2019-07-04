import configparser
import re
import sys

import apprise
import dateparser
import mechanicalsoup

config = configparser.ConfigParser()
config.read('config.ini')

# Get values from config file
username = config['DEFAULT']['USERNAME']
password = config['DEFAULT']['PASSWORD']
apprise_syntax = config['APPRISE']['SYNTAX']
time_format = config['FORMAT']['TIME']
threshold = config['DEFAULT']['THRESHOLD']

# Create apprise object
apprise_object = apprise.Apprise()
apprise_object.add(apprise_syntax)

# To receive Windows Notifications (pypiwin32 required)
# apprise_object.add('windows://')

# Set browser
browser = mechanicalsoup.StatefulBrowser()

# Open my.t website
browser.open("http://internetaccount.myt.mu")

# Enter credentials
form = browser.select_form('.loginarea')
browser["signInForm.username"] = username
browser["signInForm.password"] = password

# Sign in
form = browser.select_form()
form.choose_submit('signInContainer:submit')
resp = browser.submit_selected()

# Load page
page = browser.get_current_page()

# For debugging:
# browser.launch_browser()

# Check if login is successful
login_verify = page.select("#ContentBody")

if login_verify:
    # Get values from page
    stats = (page.find_all("table")[5]).find_all("table")[1].find_all("td", bgcolor="#FFFFFF")

    # Extract remaining data
    remaining_data = stats[5]

    # Regex black magic to extract the value
    amt = float(re.findall(r'\d*\.?\d+', remaining_data.text)[0])

    # Conversion to GB
    gb_amount = amt * float(0.001)
    remaining = str(round(gb_amount, 1)) + " GB"

    # Extract expiry date
    expiry_date = stats[6]

    # Date conversion
    convert_date = dateparser.parse(expiry_date.text)

    if time_format == "12h":
        converted_date = convert_date.strftime("%d/%m/%Y - %I:%M %p")
    elif time_format == "24h":
        converted_date = convert_date.strftime("%d/%m/%Y - %H:%M")
    else:
        print("Error: Invalid Time Format.")
        sys.exit()

    message = 'Remaining Data: ' + remaining + '\nExpiry: ' + converted_date

    if threshold is '0' or float(threshold) <= gb_amount:
        # Send notification
        apprise_object.notify(
            body=message,
            title='my.t Data Usage'
        )
    elif float(threshold) > gb_amount:
        print("Value Above Threshold")
        sys.exit()
    else:
        print("Invalid Threshold Value")
        sys.exit()

    print(message)

# If login fails, print error message from website
else:
    error_message = page.select(".feedbackPanelERROR")[0]
    print("Error: Login Failed. ", error_message.text)
    sys.exit()
