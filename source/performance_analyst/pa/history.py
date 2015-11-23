"""
Print history of the database

usage: pa history <database>

arguments:
    database    Name of database
"""
import os.path
import sqlite3
import sys
import docopt
import util


def history(
        database_name):

    assert os.path.isfile(database_name), \
         "Database {} does not exist".format(database_name)

    connection = sqlite3.connect(database_name)
    cursor = connection.cursor()
    util.update_database(connection, cursor)

    records = cursor.execute(
        "SELECT * FROM History ORDER BY timestamp ASC").fetchall()

    for record in records:
        timestamp = util.string_to_timestamp(record[0])
        version = record[1]
        description = record[2]

        sys.stdout.write("{} {} {}\n".format(timestamp, version,
            description))


@util.checked_call
def run(
        arguments):
    database_name = arguments["<database>"]
    history(database_name)


if __name__ == "__main__":
    arguments = docopt.docopt(__doc__)
    sys.exit(run(arguments))
