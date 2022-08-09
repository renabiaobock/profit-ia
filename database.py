import psycopg2
import CONSTANTS

# database connection
con = psycopg2.connect(host=CONSTANTS.HOST,
                       database=CONSTANTS.DATABASE,
                       user=CONSTANTS.USER,
                       password=CONSTANTS.PASSWORD)

#database cursor
cur = con.cursor()


def insert_new_entry_on_database(entry_id, trade_type, asset, payout, stake):
    sql = f"insert into entries values (default, '{entry_id}', '{trade_type}', '{asset}', {payout}, {stake})"
    cur.execute(sql)
    con.commit()

