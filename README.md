# my.t Usage Checker

A simple script that checks how much remaining monthly data you have from the my.t (Mauritius Telecom) portal and sends a notification.

## Requirements
You need Python 3.5 or later.

In Ubuntu, Mint and Debian you can install Python 3 like this:

    $ sudo apt-get install python3 python3-pip

For other Linux flavors, macOS and Windows, packages are available at

  http://www.python.org/getit/

## How To Use

1. Clone or download this repository to your computer

2. Edit the config.ini file (refer to the configuration section below). 

3. Navigate to the folder and install the requirements`python3 -m pip install -r requirements.txt`

4. Run the script `python3 mytusage.py`

5. You can run the script on a schedule using `cron`, [Windows Task Scheduler](https://datatofish.com/python-script-windows-scheduler/), or any other scheduler that supports python scripts. 

## Configuration
The config.ini file is used to configure the script. The following values should be set:

`USERNAME` and `PASSWORD`: These are the same credentials that you use to log in to internetaccount.myt.mu. If you don't know your login details, contact the Mauritius Telecom Hotline

`THRESHOLD`: The default value of 0 will send all notifications. Setting a value here will send you a notification only if your remaining data is below a certain amount. For example, a value of `100` will notify you if you have 99 GB left, but will not send a notification if you have 200 GB left.

`TIME`: The time format. The only valid values are `12h` or `24h`

`SYNTAX`: The Apprise syntax which will determine the type of notification you will receive. You can leave this blank if you only need command line output.

### Apprise Syntax:

Refer to the [Apprise documentation](https://github.com/caronc/apprise/wiki) for detailed examples. Over 40 different services are supported.

#### Examples: 
`mailto://{userid}:{password}@gmail.com` will send the notification by email.

`pbul://{accesstoken}` will send a Pushbullet notification

`windows://` will send the notification to the Windows Notification Centre (`pypwin32` required).

### Home Assistant Component
If you are a Home Asssistant user, I have also created a component that will save the value as a sensor, which can then be displayed in your UI: [my.t Usage (Home Assistant)](https://github.com/sjdvda/myt-usage-home-assistant)

## Credits
 - This project uses [MechanicalSoup](https://pypi.org/project/MechanicalSoup/) to scrape the my.t portal.
 - Notifications are sent using [Apprise](https://github.com/caronc/apprise).
<!--stackedit_data:
eyJoaXN0b3J5IjpbLTE5Nzk3MzU1MDMsMzgxMDI5MjgwLDE3NT
kxNTk3OTBdfQ==
-->