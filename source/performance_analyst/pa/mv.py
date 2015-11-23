"""
Rename a timer case

usage: pa mv <database> <current_timer> <new_timer>

arguments:
    database        Name of database
    current_timer   Name of timer to rename
    new_timer       New name of timer
"""
import os.path
import sqlite3
import sys
import docopt
import util


def mv(
        database_name,
        current_timer_name,
        new_timer_name):

    assert os.path.isfile(database_name), \
        "Database {} does not exist".format(database_name)

    connection = sqlite3.connect(database_name)
    cursor = connection.cursor()
    util.update_database(connection, cursor)

    cursor.execute("alter table {} rename to {}".format(current_timer_name,
        new_timer_name))
    connection.commit()


@util.checked_call
def run(
        arguments):
    database_name = arguments["<database>"]
    current_timer_name = arguments["<current_timer>"]
    new_timer_name = arguments["<new_timer>"]
    mv(database_name, current_timer_name, new_timer_name)


if __name__ == "__main__":
    arguments = docopt.docopt(__doc__)
    sys.exit(run(arguments))
