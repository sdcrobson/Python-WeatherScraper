''' This module creates a class called DBOperations which handles various aspects of creating, updating and purging the database'''
import sqlite3
import logging
from dbcm import DBCM
from datetime import datetime
import logging

class DBOperations():
    def initialize_db(self):
        """Method that initializes the database and creates the table sample"""
        try:
            
            with DBCM('weather.sqlite') as openDB:
                openDB.execute("""create table if not exists samples
                    (id integer primary key autoincrement not null,
                    sample_date text not null,
                    location text not null,
                    max_temp real not null,
                    min_temp real not null,
                    avg_temp real not null,
                    UNIQUE(sample_date));""")
        
        except Exception as e:
            logging.error("Error creating table:", e)

    def save_data(self, weather):
        """Method that inserts a dictionary of weather into the DB"""
        
        try:
            
            sql = """INSERT OR REPLACE INTO samples (sample_date,location,max_temp,min_temp,avg_temp)
            values (?,?,?,?,?)"""     
            myArray = []
            
            for date, value in weather.items():
                try:
                    myArray.append(date)
                    myArray.append('Winnipeg, MB')
                except Exception as e:
                    loggin.error("Error appending the data.", e)

                for k, v in value.items():
                    try:
                        myArray.append(v)
                    except Exception as e:
                        logging.error("Error appending values to the array.", e)
                
                with DBCM("weather.sqlite") as openDB:
                    openDB.execute(sql, myArray)
                myArray.clear()
        
        except Exception as e:
            logging.error("Error inserting sample.", e)

    def update_data(self):
        """Method that returns the latest sample date from the database"""
        try:
            
            max_value = ""
            
            with DBCM("weather.sqlite") as openDB:
            
                results = openDB.execute("select max(sample_date) from samples")
            
                for row in results:
                    try:
                        max_value = row[0]
                    except Exception as e:
                        logging.error("Data failed to update.", e)
            return max_value
        
        except Exception as e:
            logging.error("Error updating data: ", e)

    def validation(self):
        """Method that returns the oldest sample date from the database"""
        try:
            
            min_value = ""
            with DBCM("weather.sqlite") as openDB:
            
                results = openDB.execute("select min(sample_date) from samples")
            
                for row in results:
                    min_value = row[0]

            return min_value
        
        except Exception as e:
            logging.error("Error retrieving oldest date: ", e)

    def fetch_data_lineplot(self, year, month):
        """Function that returns a dictionary of dates and average temperatures based on the year and month the years enters"""
        try:
            plotting = {}
            with DBCM("weather.sqlite") as openDB:

                results = openDB.execute(f"select sample_date, avg_temp from samples WHERE substr(sample_date, 1, 7) = '{year}'||'-'||'{month}'")
                for row in results:
                    try:
                        key = row[0]
                        plotting[key] = row[1]
                    except Exception as e:
                        logging.error("Error fetching data for line plot: ", e)
            return plotting

        except Exception as e:
            logging.error("Error fetching samples.", e)

    def fetch_data_boxplot(self, year_one, year_two):
        """Function that returns a dictionary of dates and average temperatures between years that the user enters"""
        try:
            plotting = {}
            with DBCM("weather.sqlite") as openDB:

                results = openDB.execute(f"select sample_date, avg_temp from samples WHERE sample_date BETWEEN '{year_one}' AND '{year_two}'")
                for row in results:
                    try:
                        key = row[0]
                        plotting[key] = row[1]
                    except Exception as e:
                        logging.error("Error fetching data for box plot: ", e)
            return plotting
        except Exception as e:
            logging.error("Error fetching samples.", e)             

    def purge_data(self):
        """Method that purges all the data from the DB for when the program fetches all new weather data"""
        try:
            with DBCM("weather.sqlite") as openDB:
                        openDB.execute("""DROP TABLE samples;""")
        except Exception as e:
            logging.error("Error purging data: ", e)

        try:
            self.initialize_db()
        except Exception as e:
            logging.error("Error creating table:", e)

