'''This module handles scraping data from the Government of Canada's weather database'''

from html.parser import HTMLParser
from html.entities import name2codepoint
from datetime import datetime
from db_operations import DBOperations
import urllib.request
import logging



class WeatherScraper(HTMLParser):

    def __init__(self):
        try:
            HTMLParser.__init__(self)
            self.in_td = False
            self.in_tr = False
            self.in_span = False
            self.in_th = False
            self.date_string = ""
            self.daily_temp = {"Max": "", "Min": "", "Mean":""}
            self.weather = {}
            self.recording = 0
            self.counter = 0
        except Exception as e:
            logging.error(e)

    def handle_starttag(self, tag, attrs):
        try:
            if tag == 'td':
                self.in_td = True
                self.recording +=1
            if tag == 'tr':
                self.in_tr = True
            if tag == 'span':
                self.in_span = True
            if tag == 'th':
                self.in_th = True
            if tag == 'abbr':
                self.date_string = attrs
        except Exception as e:
            logging.error(e)

    def handle_endtag(self, tag):
        try:
            if tag == 'td':
                self.in_td = False
            if tag == 'tr':
                self.in_tr = False
                self.recording = 0
            if tag == 'span':
                self.in_span = False
            if tag == 'th':
                self.in_th = False
        except Exception as e:
            logging.error(e)

    def handle_data(self, data):
        try:
            if self.in_td and self.in_tr and not self.in_span and self.recording <= 3:

                if data == 'M' or data == '\xa0' :
                    data = 'N/A'

                elif data == 'E':
                    return

                if 'kilometres per hour' not in self.date_string[0][1] and 'Extreme' not in self.date_string[0][1] and 'Average' not in self.date_string[0][1] and datetime.strptime(self.date_string[0][1], '%B %d, %Y').date() not in self.weather.keys():


                    if self.counter == 0:
                        self.daily_temp['Max'] = data
                        self.counter += 1


                    elif self.counter == 1:
                        self.daily_temp['Min'] = data
                        self.counter += 1

                    else:
                        self.daily_temp['Mean'] = data
                        self.weather[datetime.strptime(self.date_string[0][1], '%B %d, %Y').date()] = self.daily_temp
                        self.daily_temp = {}
                        self.counter = 0

        except Exception as e:
            logging.error(e)


    def start_scraping(self):
        '''Returns a dictionary that is populated after being parsed from the weather database'''
        try:
            today = datetime.today()
            day = today.day
            month = today.month
            year = today.year
            myparser = WeatherScraper()
            db = DBOperations()
            temporary_dict = {}
            data = True
            
            if day == 1:
                month = month - 1

            if db.update_data() is None:
                mostRecentDate = 0
                mostRecentYear = 0
                mostRecentMonth = 0

            else:
                mostRecentDate =  db.update_data()
                mostRecentYear = mostRecentDate[0:4]
                mostRecentMonth = mostRecentDate[5:7]


            while data:
                try:
                    with urllib.request.urlopen("https://climate.weather.gc.ca/climate_data/daily_data_e.html?StationID=27174&timeframe=2&StartYear=1840&EndYear=2018&Day=1&Year={}&Month={}#".format(year,month)) as response:
                        html = str(response.read())

                        myparser.feed(html)

                    if temporary_dict == myparser.weather and len(temporary_dict) != 0:
                        data = False


                    db.save_data(myparser.weather)

                    temporary_dict = myparser.weather.copy()
                    myparser.weather.clear()

                    if int(mostRecentYear) == year and int(mostRecentMonth) == month:
                        break

                    print(year)
                    print(month)

                    month -=1
                    
                    if month == 0:
                        year -=1
                        month = 12

                except Exception as e:
                    logging.error(e)

        except Exception as e:
            logging.error(e)

