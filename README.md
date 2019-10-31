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

2. Add your my.t login details to the config.ini file. 

3. To install the dependencies, navigate to the folder and run `python -m pip install -r requirements.txt`

4. To run the script `python3 mytusage.py`

## Configuration

The config.ini file is used to configure the script. The following values should be set:

`USERNAME` and `PASSWORD`: These are the same credentials that you use to log in to internetaccount.myt.mu. If you don't know your login details, contact the Mauritius Telecom Hotline

`THRESHOLD`: The default value of 0 will send all notifications. Setting a value here will send you a notification only if your remaining data is below a certain amount. For example, a value of `100` will notify you if you have 99 GB left, but will not send a notification if you have 200 GB left.

`SYNTAX`: The Apprise syntax which will determine the type of notification you will receive:

### Apprise Syntax Examples:

Refer to 

`windows://` will send the notification to the Windows Notification Centre (`pypwin32` required).


`TIME`: The time format. The only valid values are `12h` or `24h`