import psycopg2
import CONSTANTS

# database connection
con = psycopg2.connect(host=CONSTANTS.HOST,
                       database=CONSTANTS.DATABASE,
                       user=CONSTANTS.USER,
                       password=CONSTANTS.PASSWORD)

#database cursor
cur=con.cursor()

