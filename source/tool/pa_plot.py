"""
Create a pdf with a plot of all timers supplied

usage: pa plot [--real] [--cpu] [--timestamp=<timestamp>]
    <output> <database> <timer>...

options:
    --real                      Plot real (user) times
    --cpu                       Plot cpu times
    --timestamp=<timestamp>     Timestamp to select (yyyy-mm-dd, 'latest'
                                or -1, -2, -3, etc), default: today

arguments:
    database                    Name of database
    timer                       Name of timer

In case --real and --cpu are not passed, both real and cpu times are plotted.
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
        indicators,
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

    # http://stackoverflow.com/questions/4805048/how-to-get-different-colored-lines-for-different-plots-in-a-single-figure/4805456#4805456
    nr_timers = len(timer_names)
    nr_plots = nr_timers
    # http://matplotlib.org/1.2.1/examples/pylab_examples/show_colormaps.html
    colormap = pyplot.cm.brg
    colors = [colormap(i) for i in numpy.linspace(0, 0.9, nr_plots)]
    labels = []

    # Plot mean timing.
    # for name in timer_names:
    for i in xrange(nr_timers):
        timer_name = timer_names[i]
        labels.append(timer_name)

        if "real" in indicators:
            axis.plot(sorted(real_times[timer_name]),
                real_times_mean[timer_name], "o--", color=colors[i],
                label="{} (real)".format(timer_name))

        if "cpu" in indicators:
            axis.plot(sorted(cpu_times[timer_name]),
                cpu_times_mean[timer_name], "o-", color=colors[i],
                label="{} (cpu)".format(timer_name))

    # Plot error bars.
    for i in xrange(nr_timers):
        timer_name = timer_names[i]

        if "real" in indicators:
            if len(real_times_mean[timer_name]) > 0:
                axis.errorbar(sorted(real_times[timer_name]),
                    real_times_mean[timer_name], real_times_std[timer_name],
                    fmt="o", color=colors[i])

        if "cpu" in indicators:
            if len(cpu_times_mean[timer_name]) > 0:
                axis.errorbar(sorted(cpu_times[timer_name]),
                    cpu_times_mean[timer_name], cpu_times_std[timer_name],
                    fmt="o", color=colors[i])

    legend = pyplot.legend(loc="upper right", fancybox=True, shadow=True)

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
    plot_real_times = arguments["--real"]
    plot_cpu_times = arguments["--cpu"]

    if not plot_real_times and not plot_cpu_times:
        plot_real_times, plot_cpu_times = True, True

    indicators = []
    if plot_real_times:
        indicators.append("real")
    if plot_cpu_times:
        indicators.append("cpu")

    timestamp = util.string_to_timestamp(arguments["--timestamp"]) if \
        arguments["--timestamp"] else datetime.datetime.combine(
            datetime.date.today(), datetime.datetime.min.time())
    output_pathname = arguments["<output>"]
    database_name = arguments["<database>"]
    timer_names = arguments["<timer>"]

    plot(database_name, timer_names, timestamp, indicators, output_pathname)


if __name__ == "__main__":
    arguments = docopt.docopt(__doc__)
    sys.exit(run(arguments))
