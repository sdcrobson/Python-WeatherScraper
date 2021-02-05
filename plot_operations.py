'''This module creates a boxplot and lineplot of daily mean temperatures based off user input'''

import logging
import matplotlib.pyplot as plt
from db_operations import DBOperations

class PlotOperations:
    
    def boxplot(self, year_one, year_two):
        """Method that creates a box plot of mean temperatures in a range of years based off user input."""
        try:
            db = DBOperations()
            data = db.fetch_data_boxplot(year_one, year_two)
            jan, feb, mar, apr, may, jun, jul, aug, sep, oct, nov, dec = [], [], [], [], [], [], [], [], [], [], [], []

            for key, value in data.items():
                try:                
                    if value != 'N/A':
                        if key[5:7] == '01':
                            jan.append(value)
                        elif key[5:7] == '02':
                            feb.append(value)
                        elif key[5:7] == '03':
                            mar.append(value)
                        elif key[5:7] == '04':
                            apr.append(value)
                        elif key[5:7] == '05':
                            may.append(value)
                        elif key[5:7] == '06':
                            jun.append(value)
                        elif key[5:7] == '07':
                            jul.append(value)
                        elif key[5:7] == '08':
                            aug.append(value)
                        elif key[5:7] == '09':
                            sep.append(value)
                        elif key[5:7] == '10':
                            oct.append(value)
                        elif key[5:7] == '11':
                            nov.append(value)
                        elif key[5:7] == '12':
                            dec.append(value)
                except Exception as e:
                    logging.error(e)

            data = [jan, feb, mar, apr, may, jun, jul, aug, sep, oct, nov, dec]

            plt.title('Monthly Temperature Distribution for: {} to {}'.format(year_one, year_two))
            plt.ylabel('Temperature(Celsius)')
            plt.xlabel('Month')
            plt.boxplot(data)
            plt.show()
        
        except Exception as e:
            logging.error(e)


    def linegraph(self, year, month):
        """Method that creates a lineplot of daily temperature means for a specific year and month based off user input"""

        try:
            db = DBOperations()
            data = db.fetch_data_lineplot(year, month)
            temps = []

            for key, value in data.items():
                try:
                    if value != 'N/A':
                        temps.append(value)
                except Exception as e:
                    logging.error(e)
            
            plt.title('Daily Mean Temperatures for: {} - {}'.format(year, month))
            plt.plot(temps)
            plt.ylabel('Temperature(Celsius)')
            plt.xlabel('Day')
            plt.show()
        except Exception as e:
            logging.error(e)
