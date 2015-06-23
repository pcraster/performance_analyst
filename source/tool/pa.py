#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
*****
pa.py
*****
"""
import datetime
from optparse import OptionParser
import os.path
import re
import sqlite3
import sys

import matplotlib.pyplot as pyplot
import matplotlib.ticker as ticker
import numpy
import pylab

from performance_analyst import sqlite_timer_runner


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


class _OptionParser(OptionParser):

    def format_epilog(self,
            formatter):
        return "\n{}\n".format(self.epilog.strip())


class Command(object):

    def __init__(self,
            arguments,
            usage,
            epilog=""):
        self.arguments = arguments
        self.parser = _OptionParser(usage=usage, epilog=epilog)
        self.database_name = None

    def print_help(self):
        self.parser.print_help()

    def add_timestamp_option(self,
            default):
        self.parser.add_option("--timestamp",
            dest="timestamp",
            default=default,
            help="timestamp to select (timestamp, 'latest' or -1, -2, -3, etc)")

    def timestamps(self,
            cursor,
            name):
        records = cursor.execute(
            "select timestamp from %s order by timestamp" % (name)).fetchall()
        assert len(records) > 0, "No records found for %s" % (name)

        # Remove duplicates and sort result.
        records = list(set([record[0] for record in records]))
        records.sort()

        return records

    def timestamp_by_index(self,
            cursor,
            name,
            offset):
        result = None
        timestamps = self.timestamps(cursor, name)

        if len(timestamps) >= abs(offset):
            result = timestamps[offset]

        return result

    def parse_time_stamps(self,
            cursor,
            names,
            timestamps):
        symbols = timestamps.split(":")
        timestamps = [[] for _ in range(len(names))]

        for symbol in symbols:
            for i in range(len(names)):
                if symbol == "latest":
                    timestamp = self.timestamp_by_index(cursor, names[i], -1)

                    if not timestamp is None:
                        timestamps[i].append(timestamp)
                elif re.match("-\d+", symbol):
                    timestamp = self.timestamp_by_index(cursor, names[i],
                        int(symbol) - 1)

                    if not timestamp is None:
                        timestamps[i].append(timestamp)
                else:
                    timestamps[i].append(symbol)

        assert len(timestamps) == len(names)

        return timestamps

    def timer_names(self,
            cursor):
        return [record[1] for record in \
            cursor.execute("select * from sqlite_master").fetchall()]

    def parse_timer_names(self,
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
        timer_names = self.timer_names(cursor)

        for pattern in patterns:
            pattern = re.compile("^{}$".format(pattern))
            for timer_name in timer_names:
                if pattern.match(timer_name):
                    result.append(timer_name)

        return uniquefy_list(result)

    def update_database(self,
            connection,
            cursor):
        # The runner knows best whether the database must be updated
        # and how to do it.
        sqlite_timer_runner.SQLiteTimerRunner.update_database(connection,
            cursor)


class Plot(Command):

    def __init__(self,
            arguments=[]):
        Command.__init__(self, arguments,
            usage="Usage: plot [options] <output> <database> <timer>+",
            epilog= """
Creates a pdf with a plot of all timers supplied.
""")
        self.add_timestamp_option(default="2000-01-01")

    def parse_arguments(self):
        (options, arguments) = self.parser.parse_args(self.arguments)

        if len(arguments) < 3:
            self.print_help()
            sys.exit(2)

        self.timestamp = string_to_timestamp(options.timestamp)
        self.output_filename = arguments[0]
        self.database_name = arguments[1]
        self.names = arguments[2:]

    def aggregate_data(self,
            data,
            algorithm):
        algorithms = {
            "min": numpy.nanmin,
            "mean": numpy.mean,
            "std": numpy.std,
        }

        return algorithms[algorithm](data)

    def read_data(self,
            cursor,
            tableName):
        assert not cursor.execute(
            "PRAGMA TABLE_INFO({})".format(tableName)).fetchone() is None, \
                "Table {} does not exist".format(tableName)

        real_times = {}
        cpu_times = {}

        for record in cursor.execute("select * from {}".format(
                tableName)).fetchall():
            timestamp = string_to_timestamp(record[0])

            print timestamp, self.timestamp

            if not timestamp < self.timestamp:
                real_time = float(record[1])
                cpu_time = float(record[2])

                if not timestamp in real_times:
                    assert not timestamp in cpu_times
                    real_times[timestamp] = [real_time]
                    cpu_times[timestamp] = [cpu_time]
                else:
                    assert timestamp in cpu_times
                    real_times[timestamp].append(real_time)
                    cpu_times[timestamp].append(cpu_time)

        # Convert lists to numpy arrays.
        for timestamp in real_times:
            real_times[timestamp] = numpy.array(real_times[timestamp])
            cpu_times[timestamp] = numpy.array(cpu_times[timestamp])

        # Dicts, with per timestamp a numpy array with values.
        return real_times, cpu_times

    def run(self):
        self.parse_arguments()

        assert os.path.isfile(self.database_name), \
            "Database {} does not exist".format(self.database_name)

        connection = sqlite3.connect(self.database_name)
        cursor = connection.cursor()
        self.update_database(connection, cursor)

        figure = pyplot.figure(figsize=(15, 10))
        axis = figure.add_subplot(111)
        real_times, real_times_mean, real_times_std = {}, {}, {}
        cpu_times, cpu_times_mean, cpu_times_std = {}, {}, {}

        for name in self.names:
            real_times[name], cpu_times[name] = self.read_data(cursor, name)

        lines = {}

        # Calculate statistics.
        for name in self.names:
            real_times_mean[name] = [self.aggregate_data(
                real_times[name][timestamp], algorithm="mean") for timestamp in
                sorted(real_times[name])]
            cpu_times_mean[name] = [self.aggregate_data(
                cpu_times[name][timestamp], algorithm="mean") for timestamp in
                sorted(cpu_times[name])]
            real_times_std[name] = [self.aggregate_data(
                real_times[name][timestamp], algorithm="std") for timestamp in
                sorted(real_times[name])]
            cpu_times_std[name] = [self.aggregate_data(
                cpu_times[name][timestamp], algorithm="std") for timestamp in
                sorted(cpu_times[name])]

        # Plot mean timing.
        for name in self.names:
            # Store properties of plot with real-time values.
            lines[name] = axis.plot(sorted(real_times[name]),
                real_times_mean[name], "o--")[0]
            axis.plot(sorted(cpu_times[name]), cpu_times_mean[name], "o-",
                color=lines[name].get_color())

        # Plot error bars.
        for name in self.names:
            if len(real_times_mean[name]) > 0:
                axis.errorbar(sorted(real_times[name]), real_times_mean[name],
                    real_times_std[name], fmt="o",
                    color=lines[name].get_color())
            if len(cpu_times_mean[name]) > 0:
                axis.errorbar(sorted(cpu_times[name]), cpu_times_mean[name],
                    cpu_times_std[name], fmt="o",
                    color=lines[name].get_color())

        legend = pyplot.figlegend([lines[name] for name in self.names],
            self.names, "upper right") # loc=(0.0, 0.0))

        for text in legend.get_texts():
            text.set_fontsize("small")

        axis.set_title(self.database_name)
        axis.set_xlabel("Timestamps")
        axis.set_ylabel("Time (s)")
        limits = axis.get_xlim()
        axis.set_xlim(limits[0] - 0.1, limits[1] + 0.1)
        axis.grid(True)

        figure.autofmt_xdate()

        pylab.savefig(self.output_filename)

        return 0


class Ls(Command):

    def __init__(self,
            arguments=[]):
        Command.__init__(self, arguments,
            usage="Usage: ls [options] <database> {timer}+",
            epilog="""
Lists all timers if no timer is provided. Shows some details if one or more
timers are provided.
""")

    def parse_arguments(self):
        (options, arguments) = self.parser.parse_args(self.arguments)

        if len(arguments) < 1:
            self.print_help()
            sys.exit(2)

        self.database_name = arguments[0]
        self.names = arguments[1:]

    def run(self):
        self.parse_arguments()

        assert os.path.isfile(self.database_name), \
             "Database {} does not exist".format(self.database_name)

        connection = sqlite3.connect(self.database_name)
        cursor = connection.cursor()
        self.update_database(connection, cursor)

        if len(self.names) == 0:
            for record in cursor.execute(
                    "select * from sqlite_master").fetchall():
                sys.stdout.write("{}\n".format(record[1]))
        else:
            self.names = self.parse_timer_names(cursor, self.names)

            for name in self.names:
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

        return 0


class Mv(Command):

    def __init__(self,
            arguments=[]):
        Command.__init__(self, arguments,
            usage="Usage: mv [options] <database> <current timer> <new timer>",
            epilog="""
Rename a timer case.
""")

    def parse_arguments(self):
        (options, arguments) = self.parser.parse_args(self.arguments)

        if len(arguments) != 3:
            self.print_help()
            sys.exit(2)

        self.database_name = arguments[0]
        self.names = arguments[1:]

    def run(self):
        self.parse_arguments()

        assert os.path.isfile(self.database_name), \
            "Database {} does not exist".format(self.database_name)

        connection = sqlite3.connect(self.database_name)
        cursor = connection.cursor()
        self.update_database(connection, cursor)

        assert len(self.names) == 2

        cursor.execute("alter table {} rename to {}".format(self.names[0],
            self.names[1]))
        connection.commit()

        return 0


class Rm(Command):

    def __init__(self,
            arguments=[]):
        Command.__init__(self, arguments,
            usage="Usage: rm [options] <database> <timer>+",
            epilog="""
Remove a timer case from the database.
""")
        self.parser.add_option("--timestamp",
            dest="timestamp",
            help="timestamp to remove data for (timestamp, 'latest' "
                "or -1, -2, -3, etc)")
        # self.parser.add_option("--before",
        #      dest="before",
        #      help="timestamp before which all data must be removed (timestamp)")

    def parse_arguments(self):
        (options, arguments) = self.parser.parse_args(self.arguments)

        if len(arguments) < 2:
            self.print_help()
            sys.exit(2)

        self.timestamps = options.timestamp
        # self.before = options.before
        self.database_name = arguments[0]
        self.names = arguments[1:]

    def run(self):
        self.parse_arguments()

        # print self.timestamps
        # print self.before

        assert os.path.isfile(self.database_name), \
            "Database {} does not exist".format(self.database_name)

        connection = sqlite3.connect(self.database_name)
        cursor = connection.cursor()
        self.update_database(connection, cursor)

        self.names = self.parse_timer_names(cursor, self.names)

        if not self.timestamps is None:
            self.timestamps = self.parse_time_stamps(cursor, self.names,
                self.timestamps)

            for i in xrange(len(self.names)):
                for timestamp in self.timestamps[i]:
                    tuple_ = (timestamp,)
                    cursor.execute("delete from {} where timestamp=?".format(
                        self.names[i]), tuple_)

        # if not self.before is None:
        #   pass

        # Remove whole table:
        # cursor.execute("drop table %s" % (self.names[i]))

        connection.commit()

        return 0


class Stat(Command):

    def __init__(self,
            arguments=[]):
        Command.__init__(self, arguments,
            usage="Usage: stat [options] <database> <timer>+",
            epilog="""
{}

Queries the database and calculates some statistics for the timings passed in:

  summary
    Print some summary statistics (min, max, mean, etc).

  quotient
    Print quotient of timings. If the name of one timer case is passed, than a
    temporal quotient is calculated: the quotient of the last and previous
    timing of the timer case.
    If more than one timer case is passed, than quotients are calculated
    between the first timer case and all subsequent timer cases.
    Quotients are calculated in pairs: one for the real-time timings
    and one for the cpu-timings. These values are printed in that order.

  timing
    Print the timing of each timer case, as found in the database. Nothing is
    calculated in this case. For each timer case, the real-time and cpu-time
    timings are printed, in that order.
""".format("Statistic types are: {}".format("|".join(["summary", "quotient", "timing"]))))
        # self.parser.add_option("--summary",
        #      help="print summary statistics")
        self.add_timestamp_option(default="latest")
        self.parser.add_option("--type",
            dest="type",
            choices=["summary", "quotient", "timing"],
            default="summary",
            help="calculate some statistic (%default)")

    def parse_arguments(self):
        (options, arguments) = self.parser.parse_args(self.arguments)

        if len(arguments) < 2:
            self.print_help()
            sys.exit(2)

        self.timestamps = options.timestamp
        self.type = options.type
        self.database_name = arguments[0]
        self.names = arguments[1:]

    def index_of_timestamp(self,
            cursor,
            name,
            timestamp):
        return self.timestamps(cursor, name).index(timestamp)

    def timings(self,
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

    def write_summary_statistics(self,
            cursor):
        for i in range(len(self.names)):
            assert len(self.timestamps[i]) == 1
            real_timings, cpu_timings = self.timings(cursor, self.names[i],
                self.timestamps[i][0])
            assert len(real_timings) > 0
            assert len(cpu_timings) > 0

            real_timings_mean = numpy.mean(real_timings, dtype=numpy.float64)
            cpu_timings_mean = numpy.mean(cpu_timings, dtype=numpy.float64)
            real_timings_std = numpy.std(real_timings, dtype=numpy.float64)
            cpu_timings_std = numpy.std(cpu_timings, dtype=numpy.float64)
            real_cv = real_timings_std / real_timings_mean
            cpu_cv = cpu_timings_std / cpu_timings_mean

            sys.stdout.write("{} ({}):\n".format(
                self.names[i], self.timestamps[i]))
            sys.stdout.write("min : {} {}\n".format(
                numpy.min(real_timings), numpy.min(cpu_timings)))
            sys.stdout.write("max : {} {}\n".format(
                numpy.max(real_timings), numpy.max(cpu_timings)))
            sys.stdout.write("mean: {} {}\n".format(
                real_timings_mean, cpu_timings_mean))
            sys.stdout.write("std : {} {}\n".format(
                real_timings_std, cpu_timings_std))
            sys.stdout.write("cv  : {} {}\n".format(
                real_cv, cpu_cv))

    def write_temporal_quotient(self,
            cursor):
        assert len(self.names) == 1, self.names

        name = self.names[0]
        timestamps = self.timestamps[0]

        if len(timestamps) == 1:
            # Append the previous timestamp.
            index = self.index_of_timestamp(cursor, name, timestamps[0]) - 1
            timestamps.append(self.timestamp_by_index(cursor, name, index))

        real_timings1, cpu_timings1 = self.timings(cursor, name, timestamps[0])
        real_timing1, cpu_timing1 = numpy.min(real_timings1), \
            numpy.min(cpu_timings1)
        real_timings2, cpu_timings2 = self.timings(cursor, name, timestamps[1])
        real_timing2, cpu_timing2 = numpy.min(real_timings2), \
            numpy.min(cpu_timings2)

        sys.stdout.write(
            "{real_timing_quotient} {cpu_timing_quotient}\n".format(
                real_timing_quotient=real_timing1 / real_timing2,
                cpu_timing_quotient=cpu_timing1 / cpu_timing2))

    def write_quotient2(self,
            cursor):
        assert len(self.names) > 1, "At least two names required for quotient"

        assert len(self.timestamps[0]) == 1
        real_timings, cpu_timings = self.timings(cursor, self.names[0],
            self.timestamps[0][0])
        real_timing, cpu_timing = numpy.min(real_timings), \
            numpy.min(cpu_timings)

        for i in range(1, len(self.names)):
            assert len(self.timestamps[i]) == 1
            real_timings, cpu_timings = self.timings(cursor, self.names[i],
                self.timestamps[i][0])
            sys.stdout.write(
                "{real_timing_quotient} {cpu_timing_quotient}\n".format(
                    real_timing_quotient=real_timing / numpy.min(real_timings),
                    cpu_timing_quotient=cpu_timing / numpy.min(cpu_timings)))

    def write_quotient(self,
            cursor):
        if len(self.names) <= 1:
            self.write_temporal_quotient(cursor)
        else:
            self.write_quotient2(cursor)

    def write_timing(self,
            cursor):
        for i in range(len(self.names)):
            assert len(self.timestamps[i]) == 1
            real_timings, cpu_timings = self.timings(cursor, self.names[i],
                self.timestamps[i][0])
            sys.stdout.write("{real_timing} {cpu_timing}\n".format(
                real_timing=numpy.min(real_timings),
                cpu_timing=numpy.min(cpu_timings)))

    def run(self):
        self.parse_arguments()

        assert os.path.isfile(self.database_name), \
            "Database {} does not exist".format(self.database_name)

        connection = sqlite3.connect(self.database_name)
        cursor = connection.cursor()
        self.update_database(connection, cursor)

        self.names = self.parse_timer_names(cursor, self.names)
        self.timestamps = self.parse_time_stamps(cursor, self.names,
            self.timestamps)

        if self.type == "summary":
            self.write_summary_statistics(cursor)
        elif self.type == "quotient":
            self.write_quotient(cursor)
        elif self.type == "timing":
            self.write_timing(cursor)

        return 0


class History(Command):

    def __init__(self,
            arguments=[]):
        Command.__init__(self, arguments,
            usage="Usage: history [options] <database>",
            epilog= """
Print history of the database.
""")

    def parse_arguments(self):
        (options, arguments) = self.parser.parse_args(self.arguments)

        if len(arguments) != 1:
            self.print_help()
            sys.exit(2)

        self.database_name = arguments[0]

    def run(self):
        self.parse_arguments()

        assert os.path.isfile(self.database_name), \
            "Database {} does not exist".format(self.database_name)

        connection = sqlite3.connect(self.database_name)
        cursor = connection.cursor()
        self.update_database(connection, cursor)

        records = cursor.execute(
            "SELECT * FROM History ORDER BY timestamp ASC").fetchall()

        for record in records:
            timestamp = string_to_timestamp(record[0])
            version = record[1]
            description = record[2]

            sys.stdout.write("{} {} {}\n".format(timestamp, version,
                description))


if __name__ == "__main__":
    commands = {
        "plot": Plot,
        "ls": Ls,
        "mv": Mv,
        "rm" : Rm,
        "stat" : Stat,
        "history" : History,
    }

    def test_command(
            command):
        if not command in commands:
            sys.stderr.write("Command not one of '{}'\n".format(
                ", ".join(commands)))
            sys.exit(2)

        usage = "Usage: %prog [options] <command>"
        epilog = """
See 'pa.py help <command>' for more information on a specific command.

Commands are: {}
""".format(" | ".join(commands))

    parser = _OptionParser(usage=usage, epilog=epilog)
    parser.disable_interspersed_args()
    (options, arguments) = parser.parse_args()

    command = None

    if len(arguments) >= 1:
        command = arguments[0]

    if command is None:
        parser.print_help()
        sys.exit(2)
    elif command == "help":
        if len(arguments) < 2:
            parser.print_help()
        else:
            command2 = arguments[1]
            test_command(command2)
            commands[command2]().print_help()

        sys.exit(0)

    test_command(command)
    sys.exit(commands[command](arguments[1:]).run())
