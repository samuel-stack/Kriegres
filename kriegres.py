
import pandas as pd
import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT

class kriegres:

    '''
    Kriegres is a class wrapper for the Psycopg2 library in order to interact with Postgres SQL Databases and servers.
    This class is designed to make interacting with Postgres via Psycopg2 much simpler as it will automate much
    of the additional actions needed for such interactions, such as setting cursors, opening and closing connections,
    writing to tables and returning tables as pandas style dataframes.  Additionally, it will be much simpler to
    retrive the metadata for databases and servers.
    '''


    host = None
    port = None
    database = None
    server_connection = None
    db_connection = None


    def __init__(self, host, port,):

        self.host = str(host)
        self.port = str(port)
        self.server_connection = "host='{}' port='{}'".format(host,port)

        # Invalid Host/port combination will result in error.
        psycopg2.connect(self.server_connection)

    # Set the current database for querying.
    def set_database(self, database):
        '''Sets the database to connect to on the server.  This can be changed at any time.'''
        con = psycopg2.connect(self.server_connection)
        cur = con.cursor()
        cur.execute("""SELECT datname from pg_database""")
        dbs = cur.fetchall()
        datas = [row[0] for row in dbs]
        con.close()

        if database in datas:
            self.database = str(database)
            self.db_connection = "host='{}' dbname='{}' port='{}'".format(self.host, self.database, self.port)
        else:
            print('Invalid database name, active Database has been set to "None"')


    # List Database Names
    def get_databases(self):
        '''Returns the database names on the connected server.'''
        con = psycopg2.connect(self.server_connection)
        cur = con.cursor()
        cur.execute("""SELECT datname from pg_database""")
        datas = [row[0] for row in cur.fetchall()]
        con.close()
        return datas

    # Create Database
    def create_database(self, db_name):
        con = psycopg2.connect(self.server_connection)
        con.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
        cur = con.cursor()
        cur.execute('''CREATE DATABASE {}'''.format(str(db_name)))
        con.close()

    # Drop Database
    def delete_database(self, db_name):
        '''Drops a specified database'''
        con = psycopg2.connect(self.server_connection)
        con.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
        cur = con.cursor()
        cur.execute('''DROP DATABASE {} '''.format(db_name))
        con.close()


    # Returns dictionary of Databases info where Keys are database names on said server
    # and values are a list of tables on said database.
    def database_schemas(self):
        '''Returns the Database Name and public table info for all databases on the server.'''
        con = psycopg2.connect(self.server_connection)
        cur = con.cursor()
        cur.execute("""SELECT datname from pg_database""")
        dbs = cur.fetchall()
        # dbs = con.cursor().fetchmany()
        dbs_list = [db[0] for db in dbs]


        database_dict = {}
        for database in dbs_list:
            try:
                connie = "host='{}' dbname='{}' port='{}'".format(self.host, database, self.port)
                con = psycopg2.connect(connie)
                cur = con.cursor()
                cur.execute("""SELECT table_name FROM information_schema.tables
                WHERE table_schema = 'public'
                ORDER BY table_name ;""")
                table_info = cur.fetchall()

                if not table_info:

                    database_dict[database] = None
                else:

                    database_dict[database] = [name[0] for name in table_info]
            except:

                database_dict[database] = None
        con.close()

        return database_dict



    # directly update the specified table with a insert SQL insert query.
    def update(self, insert_query):
        """Utilizes insert queries to manually update a table."""
        con = psycopg2.connect(self.db_connection)
        cur = con.cursor()
        cur.execute(insert_query)
        con.commit()
        con.close()


    #Uses a list to insert one list into specified table or current database
    def insert_one(self, table, value_list):

        tuple_value_list = tuple(value_list)
        con = psycopg2.connect(self.db_connection)
        cur = con.cursor()

        # test to see if value like is comparable to length of table.
        cur.execute("""SELECT * from {} LIMIT 1""".format(table))
        row_len = len(cur.fetchall()[0])
        if row_len != len(value_list):
            print("""Invalid value_list.  Length of value_list must be equal to number of columns.
            Table {} has {} columns.""".format(table, str(row_len)))
            return

        # if appropriate length, inserts.
        cur.execute('''INSERT INTO {} VALUES {}'''.format(table, tuple_value_list))
        con.commit()
        con.close()


    #Uses a list to insert many into specified table or current database
    def insert_many(self, table, list_of_values_list):
        con = psycopg2.connect(self.db_connection)
        cur = con.cursor()

        # Validate length or lists in list
        cur.execute("""SELECT * from {} LIMIT 1""".format(table))
        row_len = len(cur.fetchall()[0])
        for n_row in list_of_values_list:
            if len(n_row) != row_len:
                print("""Invalid row in list_of_values_list. Length of rows in list_of_values_list
                must be equal to number of columns in target table.
                Table {} has {} columns.""".format(table, str(row_len)))
                return


        # If valid lengths, inserts all lists.
        for n_row in list_of_values_list:
            cur.execute('''INSERT INTO {} VALUES {}'''.format(table,tuple(n_row)))
            con.commit()
        con.close()


    # Query's Table and returns query as a Pandas Dataframe
    def query(self, query):
        con = psycopg2.connect(self.db_connection)
        cur = con.cursor()
        cur.execute(query)
        rows = cur.fetchall()
        cols = [desc[0] for desc in cur.description]

        df = pd.DataFrame(data =rows, columns = cols)
        con.close()
        return df
