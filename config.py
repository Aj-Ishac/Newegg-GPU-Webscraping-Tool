header_values = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3',
    'Accept-Encoding':	'gzip, deflate',
    'Accept-Language':	'en-US,en;q=0.9,hi;q=0.8',
    'Connection':	'keep-alive',
    'Referer':	'https://www.google.com/',
    'Upgrade-Insecure-Requests':	'1',
    'User-Agent':	'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36'
    }

#directory where CSV storage
csv_folder = (r"E:\Personal Projects\scrappy\CSV storage")

#email to SEND FROM
#default NULL
USER_NAME_send = ""
USER_PASS_send = ""

#email to SEND TO
USER_NAME_receive = ""

#price threshold for email to be sent out
#default 0
price_threshold = 0;

#Time to wait in seconds for the tool to automatilly do another search
#default 60seconds
time_wait_secs = 60;