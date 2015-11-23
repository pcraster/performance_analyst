"""
List timers in the database

usage: pa ls <database> [<timer>...]

arguments:
    database    Name of database
    timer       Name of timer

List all timers if no timer is provided. Shows some details if one or more
timers are provided.

List all timers:

    pa.py ls timings.db

List all timers matching a pattern:

    pa.py ls timings.db ".*add.*"
"""
import os.path
import sqlite3
import sys
import docopt
import util


def ls(
        database_name,
        timer_names):

    assert os.path.isfile(database_name), \
         "Database {} does not exist".format(database_name)

    connection = sqlite3.connect(database_name)
    cursor = connection.cursor()
    util.update_database(connection, cursor)

    if len(timer_names) == 0:
        for record in cursor.execute(
                "select * from sqlite_master").fetchall():
            sys.stdout.write("{}\n".format(record[1]))
    else:
        timer_names = util.parse_timer_names(cursor, timer_names)

        for name in timer_names:
            records = cursor.execute(
                "select * from %s" % (name)).fetchall()
            timestamps = {}

            for record in records:
                if not record[0] in timestamps:
                    timestamps[record[0]]  = 1
                else:
                    timestamps[record[0]] += 1

            # Print name of timer.
            if len(timestamps) > 0:
                sys.stdout.write("{}\n".format(name))

            # Print info per run.
            for timestamp in sorted(timestamps.keys()):
                sys.stdout.write("{}\t{}\n".format(timestamp,
                    timestamps[timestamp]))


@util.checked_call
def run(
        arguments):
    database_name = arguments["<database>"]
    timer_names = arguments["<timer>"]
    ls(database_name, timer_names)


if __name__ == "__main__":
    arguments = docopt.docopt(__doc__)
    sys.exit(run(arguments))
