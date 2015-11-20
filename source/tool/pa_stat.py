"""
Query the database and calculates some statistics

usage: pa stat [--summary|--quotient|--timing] [--timestamp=<timestamp>]
            <database> <timer>...

options:
    --summary                   Print some summary statistics (min, max, mean,
                                etc)
    --quotient                  Print quotient of timings. If the name
                                of one timer case is passed, than a
                                temporal quotient is calculated: the
                                quotient of the last and previous timing
                                of the timer case.
                                If more than one timer case is passed,
                                than quotients are calculated between
                                the first timer case and all subsequent
                                timer cases.
                                Quotients are calculated in pairs:
                                one for the real-time timings and one
                                for the cpu-timings. These values are
                                printed in that order.
    --timing                    Print the timing of each timer case,
                                as found in the database. Nothing is
                                calculated in this case. For each timer
                                case, the real-time and cpu-time timings
                                are printed, in that order.
    --timestamp=<timestamp>     Timestamp to select (yyyy-mm-dd, 'latest'
                                or -1, -2, -3, etc), default: 'latest'

arguments:
    database                    Name of database
    timer                       Name of timer
"""
import os.path
import sqlite3
import sys
import docopt
import numpy
import util


def write_summary_statistics(
        cursor,
        timer_names,
        timestamps):
    for i in range(len(timer_names)):
        assert len(timestamps[i]) == 1
        real_timings, cpu_timings = util.timings(cursor, timer_names[i],
            timestamps[i][0])
        assert len(real_timings) > 0
        assert len(cpu_timings) > 0

        real_timings_mean = numpy.mean(real_timings, dtype=numpy.float64)
        cpu_timings_mean = numpy.mean(cpu_timings, dtype=numpy.float64)
        real_timings_std = numpy.std(real_timings, dtype=numpy.float64)
        cpu_timings_std = numpy.std(cpu_timings, dtype=numpy.float64)
        real_cv = real_timings_std / real_timings_mean
        cpu_cv = cpu_timings_std / cpu_timings_mean

        sys.stdout.write("{} ({}):\n".format(
            timer_names[i], timestamps[i]))
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


def write_temporal_quotient(
        cursor,
        timer_names,
        timestamps):
    assert len(timer_names) == 1, timer_names

    name = timer_names[0]
    timestamps = timestamps[0]

    if len(timestamps) == 1:
        # Append the previous timestamp.
        index = util.index_of_timestamp(cursor, name, timestamps[0]) - 1
        timestamps.append(util.timestamp_by_index(cursor, name, index))

    real_timings1, cpu_timings1 = util.timings(cursor, name, timestamps[0])
    real_timing1, cpu_timing1 = numpy.min(real_timings1), \
        numpy.min(cpu_timings1)
    real_timings2, cpu_timings2 = util.timings(cursor, name, timestamps[1])
    real_timing2, cpu_timing2 = numpy.min(real_timings2), \
        numpy.min(cpu_timings2)

    sys.stdout.write(
        "{real_timing_quotient} {cpu_timing_quotient}\n".format(
            real_timing_quotient=real_timing1 / real_timing2,
            cpu_timing_quotient=cpu_timing1 / cpu_timing2))


def write_quotient2(
        cursor,
        timer_names,
        timestamps):
    assert len(timer_names) > 1, "At least two names required for quotient"

    assert len(timestamps[0]) == 1
    real_timings, cpu_timings = util.timings(cursor, timer_names[0],
        timestamps[0][0])
    real_timing, cpu_timing = numpy.min(real_timings), \
        numpy.min(cpu_timings)

    for i in range(1, len(timer_names)):
        assert len(timestamps[i]) == 1
        real_timings, cpu_timings = util.timings(cursor, timer_names[i],
            timestamps[i][0])
        sys.stdout.write(
            "{real_timing_quotient} {cpu_timing_quotient}\n".format(
                real_timing_quotient=real_timing / numpy.min(real_timings),
                cpu_timing_quotient=cpu_timing / numpy.min(cpu_timings)))

def write_quotient(
        cursor,
        timer_names,
        timestamps):
    if len(timer_names) <= 1:
        write_temporal_quotient(cursor, timer_names, timestamps)
    else:
        write_quotient2(cursor, timer_names, timestamps)

def write_timing(
        cursor,
        timer_names,
        timestamps):
    for i in range(len(timer_names)):
        assert len(timestamps[i]) == 1
        real_timings, cpu_timings = util.timings(cursor, timer_names[i],
            timestamps[i][0])
        sys.stdout.write("{real_timing} {cpu_timing}\n".format(
            real_timing=numpy.min(real_timings),
            cpu_timing=numpy.min(cpu_timings)))

def stat(
        database_name,
        timer_names,
        timestamps,
        statistic):

    assert os.path.isfile(database_name), \
        "Database {} does not exist".format(database_name)

    connection = sqlite3.connect(database_name)
    cursor = connection.cursor()
    util.update_database(connection, cursor)

    timer_names = util.parse_timer_names(cursor, timer_names)
    timestamps = util.parse_time_stamps(cursor, timer_names,
        timestamps)

    if statistic == "summary":
        write_summary_statistics(cursor, timer_names, timestamps)
    elif statistic == "quotient":
        write_quotient(cursor, timer_names, timestamps)
    elif statistic == "timing":
        write_timing(cursor, timer_names, timestamps)


@util.checked_call
def run(
        arguments):
    statistic = "summary"
    if arguments["--quotient"]:
        statistic = "quotient"
    elif arguments["--timing"]:
        statistic = "timing"

    timestamp = util.string_to_timestamp(arguments["--timestamp"]) if \
        arguments["--timestamp"] else "latest"
    database_name = arguments["<database>"]
    timer_names = arguments["<timer>"]

    stat(database_name, timer_names, timestamp, statistic)


if __name__ == "__main__":
    arguments = docopt.docopt(__doc__)
    sys.exit(run(arguments))
