import sqlite3
import time
import Data

# Logs a drink to the database
def log_drink(id, stddrinks):
    con = sqlite3.connect('main.db')

    cur = con.cursor()

    cur.execute(f"INSERT INTO Drank VALUES ({id}, {stddrinks}, {int(time.time())});")
    con.commit()
    con.close()



# Determines if a user has had in excess of the standard drink limit in the past hour
def is_drunk(id):
    current_time = int(time.time())
    threshold_time = current_time - 3600  # Cut-off time for last drink

    # Open a connection to the database
    con = sqlite3.connect('main.db')
    cur = con.cursor()

    # Get the total std drinks consumed in the last hour
    cur.execute(f"SELECT SUM(stddrinks) FROM Drank WHERE studentid={id} and time >= {threshold_time};")

    drinks_sum = cur.fetchone()[0]

    if drinks_sum is None:
        return False

    # Check if the user is over the limit
    drunk = drinks_sum >= Data.maxDrinks

    con.commit()
    con.close()

    return drunk
