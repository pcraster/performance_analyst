import datetime
import functools
import re
import sqlite3
import sys
import traceback
from performance_analyst import sqlite_timer_runner


def checked_call(
        function):
    @functools.wraps(function)
    def wrapper(
            *args,
            **kwargs):
        result = 0
        try:
            result = function(*args, **kwargs)
        except:
            traceback.print_exc(file=sys.stderr)
            result = 1
        return 0 if result is None else result
    return wrapper


def update_database(
        connection,
        cursor):
    # The runner knows best whether the database must be updated
    # and how to do it.
    sqlite_timer_runner.SQLiteTimerRunner.update_database(connection,
        cursor)


def uniquefy_list(
        list_):
    """
    Remove duplicates from `list_` and retain the order of the items.

    The first occurrence of an item is retained. Subsequent items with
    the same value are deleted.

    A new list with the resulting items is returned.
    """
    seen = set()
    return [item for item in  list_ if item not in seen and not seen.add(item)]


def timer_names(
        cursor):
    return [record[1] for record in \
        cursor.execute("select * from sqlite_master").fetchall()]


def parse_timer_names(
        cursor,
        patterns):
    """
    Determine which timer names match the regular expressions in
    `patterns`.

    The patterns in `patterns` are used as regular expressions. The
    rules for matching regular expressions is different from shell
    expansion rules. Use the `ls` sub-command of `pa.py` to test
    your expressions patterns before issueing the `rm` sub-command,
    for example.
    """
    result = []
    timer_names_ = timer_names(cursor)

    for pattern in patterns:
        pattern = re.compile("^{}$".format(pattern))
        for timer_name in timer_names_:
            if pattern.match(timer_name):
                result.append(timer_name)

    return uniquefy_list(result)


def string_to_timestamp(
        string):
    try:
        # String with microseconds.
        timestamp = datetime.datetime.strptime(string, "%Y-%m-%d %H:%M:%S.%f")
    except ValueError:
        try:
            # String without microseconds.
            timestamp = datetime.datetime.strptime(string, "%Y-%m-%d %H:%M:%S")
        except ValueError:
            # String without time.
            timestamp = datetime.datetime.strptime(string, "%Y-%m-%d")

    return timestamp


def timestamps(
        cursor,
        name):
    records = cursor.execute(
        "select timestamp from %s order by timestamp" % (name)).fetchall()
    assert len(records) > 0, "No records found for %s" % (name)

    # Remove duplicates and sort result.
    records = list(set([record[0] for record in records]))
    records.sort()

    return records


def timestamp_by_index(
        cursor,
        name,
        offset):
    result = None
    timestamps_ = timestamps(cursor, name)

    if len(timestamps_) >= abs(offset):
        result = timestamps_[offset]

    return result


def parse_time_stamps(
        cursor,
        names,
        timestamps):
    symbols = timestamps.split(":")
    timestamps = [[] for _ in range(len(names))]

    for symbol in symbols:
        for i in range(len(names)):
            if symbol == "latest":
                timestamp = timestamp_by_index(cursor, names[i], -1)

                if not timestamp is None:
                    timestamps[i].append(timestamp)
            elif re.match("-\d+", symbol):
                timestamp = timestamp_by_index(cursor, names[i],
                    int(symbol) - 1)

                if not timestamp is None:
                    timestamps[i].append(timestamp)
            else:
                timestamps[i].append(symbol)

    assert len(timestamps) == len(names)

    return timestamps


def index_of_timestamp(
        cursor,
        name,
        timestamp):
    return timestamps(cursor, name).index(timestamp)


def timings(
        cursor,
        name,
        timestamp):
    real_times = []
    cpu_times = []
    tuple_ = (timestamp,)
    for record in cursor.execute(
        "SELECT real_time, cpu_time FROM {} WHERE timestamp=?".format(
            name), tuple_).fetchall():
        real_times.append(record[0])
        cpu_times.append(record[1])

    return real_times, cpu_times


