"""
Create a pdf with a plot of all timers supplied

usage: pa plot [--timestamp=<timestamp>] <output> <database> <timer>...

options:
    --timestamp=<timestamp>     Timestamp to select (yyyy-mm-dd, 'latest'
                                or -1, -2, -3, etc), default: today

arguments:
    database                    Name of database
    timer                       Name of timer
"""
import datetime
import os.path
import sqlite3
import sys
import docopt
import matplotlib.pyplot as pyplot
import matplotlib.ticker as ticker
import numpy
import pylab
import util


def aggregate_data(
        data,
        algorithm):
    algorithms = {
        "min": numpy.nanmin,
        "mean": numpy.mean,
        "std": numpy.std,
    }

    return algorithms[algorithm](data)


def read_data(
        cursor,
        tablename,
        timestamp):
    assert not cursor.execute(
        "PRAGMA TABLE_INFO({})".format(tablename)).fetchone() is None, \
            "Table {} does not exist".format(tablename)

    real_times = {}
    cpu_times = {}

    for record in cursor.execute("select * from {}".format(
            tablename)).fetchall():
        timestamp_ = util.string_to_timestamp(record[0])

        # print timestamp_, timestamp

        if not timestamp_ < timestamp:
            real_time = float(record[1])
            cpu_time = float(record[2])

            if not timestamp_ in real_times:
                assert not timestamp_ in cpu_times
                real_times[timestamp_] = [real_time]
                cpu_times[timestamp_] = [cpu_time]
            else:
                assert timestamp_ in cpu_times
                real_times[timestamp_].append(real_time)
                cpu_times[timestamp_].append(cpu_time)

    # Convert lists to numpy arrays.
    for timestamp_ in real_times:
        real_times[timestamp_] = numpy.array(real_times[timestamp_])
        cpu_times[timestamp_] = numpy.array(cpu_times[timestamp_])

    # Dicts, with per timestamp a numpy array with values.
    return real_times, cpu_times


def plot(
        database_name,
        timer_names,
        timestamp,
        output_pathname):

    assert os.path.isfile(database_name), \
        "Database {} does not exist".format(database_name)

    connection = sqlite3.connect(database_name)
    cursor = connection.cursor()
    util.update_database(connection, cursor)

    figure = pyplot.figure(figsize=(15, 10))
    axis = figure.add_subplot(111)
    real_times, real_times_mean, real_times_std = {}, {}, {}
    cpu_times, cpu_times_mean, cpu_times_std = {}, {}, {}

    for name in timer_names:
        real_times[name], cpu_times[name] = read_data(cursor, name, timestamp)

    lines = {}

    # Calculate statistics.
    for name in timer_names:
        real_times_mean[name] = [aggregate_data(
            real_times[name][timestamp], algorithm="mean") for timestamp in
            sorted(real_times[name])]
        cpu_times_mean[name] = [aggregate_data(
            cpu_times[name][timestamp], algorithm="mean") for timestamp in
            sorted(cpu_times[name])]
        real_times_std[name] = [aggregate_data(
            real_times[name][timestamp], algorithm="std") for timestamp in
            sorted(real_times[name])]
        cpu_times_std[name] = [aggregate_data(
            cpu_times[name][timestamp], algorithm="std") for timestamp in
            sorted(cpu_times[name])]

    # Plot mean timing.
    for name in timer_names:
        # Store properties of plot with real-time values.
        lines[name] = axis.plot(sorted(real_times[name]),
            real_times_mean[name], "o--")[0]
        # axis.plot(sorted(cpu_times[name]), cpu_times_mean[name], "o-",
        #     color=lines[name].get_color())

    # Plot error bars.
    for name in timer_names:
        if len(real_times_mean[name]) > 0:
            axis.errorbar(sorted(real_times[name]), real_times_mean[name],
                real_times_std[name], fmt="o",
                color=lines[name].get_color())
        # if len(cpu_times_mean[name]) > 0:
        #     axis.errorbar(sorted(cpu_times[name]), cpu_times_mean[name],
        #         cpu_times_std[name], fmt="o",
        #         color=lines[name].get_color())

    legend = pyplot.figlegend([lines[name] for name in timer_names],
        timer_names, "upper right") # loc=(0.0, 0.0))

    for text in legend.get_texts():
        text.set_fontsize("small")

    axis.set_title(database_name)
    axis.set_xlabel("Timestamps")
    axis.set_ylabel("Time (s)")
    limits = axis.get_xlim()
    axis.set_xlim(limits[0] - 0.1, limits[1] + 0.1)
    axis.grid(True)

    figure.autofmt_xdate()

    pylab.savefig(output_pathname)


@util.checked_call
def run(
        arguments):
    timestamp = util.string_to_timestamp(arguments["--timestamp"]) if \
        arguments["--timestamp"] else datetime.datetime.combine(
            datetime.date.today(), datetime.datetime.min.time())
    output_pathname = arguments["<output>"]
    database_name = arguments["<database>"]
    timer_names = arguments["<timer>"]

    plot(database_name, timer_names, timestamp, output_pathname)


if __name__ == "__main__":
    arguments = docopt.docopt(__doc__)
    sys.exit(run(arguments))
