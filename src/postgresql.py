""" python-postgresql interaction module """

from configparser import ConfigParser
import psycopg2

DB_CONFIG_FILE = 'src/database.ini'
DB_CONFIG_SCTN = 'postgresql'

def config(filename=DB_CONFIG_FILE, section=DB_CONFIG_SCTN):
    """ load DB config """
    # create a parser
    parser = ConfigParser()
    # read config file
    parser.read(filename)

    # get section, default to postgresql
    db = {}
    if parser.has_section(section):
        params = parser.items(section)
        for param in params:
            db[param[0]] = param[1]
    else:
        raise ValueError(f"Section {section} not found in the {filename} file")

    return db

def connect():
    """ Connect to the PostgreSQL database server """
    conn = None
    try:
        # read connection parameters
        params = config()

        # connect to the PostgreSQL server
        print('Connecting to the PostgreSQL database...')
        conn = psycopg2.connect(**params)
        # create a cursor
        cur = conn.cursor()

	    # execute a statement
        print('PostgreSQL database version:')
        cur.execute('SELECT version()')

        # display the PostgreSQL database server version
        db_version = cur.fetchone()
        print(db_version)

	    # close the communication with the PostgreSQL
        cur.close()
    except (ValueError, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()
            print('Database connection closed.')


if __name__ == '__main__':
    connect()
