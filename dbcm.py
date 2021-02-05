import sqlite3

class DBCM:

    def __init__(self, filename):
        try:
            self.filename = filename
        except Exception as e:
            print(e)


    def __enter__(self):
        try:
            self.conn = sqlite3.connect(self.filename)          
            self.c = self.conn.cursor()
            return self.c
        except Exception as e:
            print(e)
        
    def __exit__(self, exc_type, exc_value, exc_traceback):
        try:
            self.conn.commit()
            self.c.close()
            self.conn.close()
        except Exception as e:
            print(e)
