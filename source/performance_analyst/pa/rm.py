"""
Remove timer cases from a database

usage: pa rm [--timestamps=<timestamps>] <database> <timer>...

options:
    --timestamps=<timestamps>   Timestamps to select (yyyy-mm-dd, 'latest'
                                or -1, -2, -3, etc)

arguments:
    database                    Name of database
    timer                       Name of timer
"""
# self.parser.add_option("--before",
#      dest="before",
#      help="timestamp before which all data must be removed (timestamp)")
import os.path
import sqlite3
import sys
import docopt
import util


def rm(
        database_name,
        timer_names,
        timestamps):

    assert os.path.isfile(database_name), \
        "Database {} does not exist".format(database_name)

    connection = sqlite3.connect(database_name)
    cursor = connection.cursor()
    util.update_database(connection, cursor)

    timer_names = util.parse_timer_names(cursor, timer_names)

    if timestamps is not None:
        timestamps = util.parse_time_stamps(cursor, timer_names, timestamps)

        for i in xrange(len(timer_names)):
            for timestamp in timestamps[i]:
                tuple_ = (timestamp,)
                cursor.execute("delete from {} where timestamp=?".format(
                    timer_names[i]), tuple_)

    # if not self.before is None:
    #   pass

    # Remove whole table:
    # cursor.execute("drop table %s" % (timer_names[i]))

    connection.commit()


@util.checked_call
def run(
        arguments):
    database_name = arguments["<database>"]
    timestamps = arguments["--timestamps"]
    timer_names = arguments["<timer>"]

    rm(database_name, timer_names, timestamps)


if __name__ == "__main__":
    arguments = docopt.docopt(__doc__)
    sys.exit(run(arguments))
