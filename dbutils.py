import sqlite3
import os

class NobelDB:
    def __init__(self) -> None:
        self.create_table_query = '''
                create table nobel_laureates
                (
                    id INTEGER,
                    portion VARCHAR,
                    known_name_en VARCHAR,
                    full_name_en VARCHAR,
                    motivation_en VARCHAR,
                    award_year INTEGER,
                    date_awarded date, 
                    prize_amount INTEGER,
                    prize_amount_adjusted INTEGER,
                    category_en VARCHAR, 
                    category_se VARCHAR, 
                    category_full_name_en VARCHAR
                )
            '''
        self.db = "nobel.db"
        self.check_db = self.__check_create_db()
        self.create_nobel_table = self.__create_table__(self.create_table_query)
    
    def __check_create_db(self):
        try:
            os.makedirs('data')
        except:
            print("Directory already exists")

        if os.path.exists(f"data/{self.db}"):
            print(f"Database {self.db} exists")
        else:
            conn = sqlite3.connect(f"data/{self.db}")
            print(f"Database {self.db} created")
            conn.close()
        return True
    
    def insert_table(self, values):
        conn = sqlite3.connect(f"data/{self.db}")
        insert_query = ''' insert into nobel_laureates ('id',
                    'portion', 'known_name_en', 'full_name_en', 'motivation_en', 'award_year',
                    'date_awarded', 'prize_amount','prize_amount_adjusted','category_en', 
                    'category_se', 'category_full_name_en') 
                    values (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?) '''
        try:
            conn.execute(insert_query, values)
            conn.commit()
            result = f"Insert - Complete"
        except Exception as e:
            print(e)
            conn.rollback()
            result = f"Insert- InComplete"
        finally:
            conn.close()
        print(result)
        return result
    
    def __create_table__(self, query):
        """
            Runs create table query but ideally this is abstracted
        """
        conn = sqlite3.connect(f"data/{self.db}")
        # create table
        try:
            conn.execute(f"{query}")
            conn.commit()
        except sqlite3.OperationalError as e:
            print(e)
        finally:
            conn.close()
        return

    def list_tables(self):
        """
            Listing tables from Sqlite
        """
        return self.run_select_fetch_all('''SELECT name FROM sqlite_master WHERE type='table';''')
    
    def run_select_fetch_all(self, query) -> list:
        """
            Runs fetch all for a given query and returns the result
            Returns List
        """
        conn = sqlite3.connect(f"data/{self.db}")
        try:
            result = conn.execute(query).fetchall()
        except:
            return {}
        conn.close()
        return result
    
    def run_select_fetch_one(self, query) -> tuple:
        """
            Runs fetch one for given query
        """
        conn = sqlite3.connect(f"data/{self.db}")
        try:
            result = conn.execute(query).fetchone()
        except Exception as e:
            print(e)
            return {}
        conn.close()
        return result
    
    def run_query(self, query):
        conn = sqlite3.connect(f"data/{self.db}")
        try:
            conn.execute(query)
            conn.commit()
        except Exception as e:
            print(e)
            return {}
        conn.close()
        return f"Executed - {query}"

   