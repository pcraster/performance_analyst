"""
*****************
SQLiteTimerRunner
*****************

.. Warning::

   * This is work in progress, so don't forget to create backups of your timings database file. Bugs in the software can easely render the database file useless. Since the whole database is stored in a single file, just copying the file to a safe location suffices.
   * Once in a while a new version of the software may require a database structure change (new tables, new fields, etc). The performance_analyst tries to hide this fact as much as possible. Database updates will happen behind the scenes, when an old database is used by a new version of the software for the first time. This may take a long time to complete, depending on the size of the database and the exact changes that need to be made. Do not interupt this process!
"""
import sqlite3
import datetime
import configuration
import timer_runner


class SQLiteTimerRunner(timer_runner.TimerRunner):

    @classmethod
    def version(cls,
            cursor):
        """
        Return the version of the software that updated the database
        the last time.

        An integer value is returned.
        """
        record = cursor.execute(
            "SELECT version FROM History ORDER BY version DESC").fetchone()
        return record[0]

    @classmethod
    def initialize_timing_table(cls,
            cursor,
            name):
        cursor.execute("""CREATE TABLE %s (
            timestamp TEXT,
            real_time REAL,
            cpu_time REAL)""" % (name))
            # real_time REAL CONSTRAINT DEFAULT 0.0)""" % (table_name))

    @classmethod
    def initialize_history_table(cls,
            cursor):
        # History table doesn't exist already.
        # Create it and put in a dummy version number that's lower than
        # the one that introduced the history table.
        assert cursor.execute("PRAGMA TABLE_INFO(History)").fetchone() is None
        assert configuration.version_as_integer() >= 5

        cursor.execute("""CREATE TABLE History (
            timestamp TEXT,
            version INTEGER,
            description TEXT)""")
        timestamp = datetime.datetime.utcnow().isoformat(" ")
        version = 5 # 0.0.5
        description = "Initialized History table"
        tuple_ = (timestamp, version, description)
        cursor.execute(
            "INSERT INTO History VALUES (\"{}\", {}, \"{}\")".format(*tuple_))

    @classmethod
    def update_database(cls,
            connection,
            cursor):
        """
        Do everything necessary to bring the database up to date with
        the current version of the software.

        Once in a while a new version of the software may require a
        database structure change (new tables, new fields, etc). This
        function should be called before other parts of the software
        start using the database file.
        """
        # The database layout depends on the version of the Performance Analyst
        # that has been used to update the database last. This information is
        # stored in the a table called 'History'. This table has the folowing
        # layout:
        #
        # | date | version | description |
        #
        # With these fields:
        # date       : Date the run started.
        # version    : Version of Performance Analyst used in run.
        # description: Description of why the database changed.

        # The History table was added to the database after the first
        # versions of the Performance Analyst where already released.
        if cursor.execute("PRAGMA TABLE_INFO(History)").fetchone() is None:
            cls.initialize_history_table(cursor)

        assert cursor.execute("PRAGMA TABLE_INFO(History)").fetchone() is \
            not None
        database_version = cls.version(cursor)

        assert database_version <= configuration.version_as_integer(), \
            "Database created with newer version of the software. " \
            "Update software."

        # Database changes, by version:
        # 0.0.6:
        # - Renamed field duration to cpu_time
        # - Added field real_time

        if database_version < 6:
            # For each table containing timings:
            # - Rename the table to some tmp name.
            # - Create new currentVersion of the table.
            # - Copy original data from tmp table to new table. Insert
            #   dummy value for new fields.
            # - Remove tmp table.
            for record in \
                    cursor.execute("SELECT * FROM sqlite_master").fetchall():
                table_name = record[1]

                if table_name.find("_time") != -1:
                    tmp_table_name = "{}_tmp".format(table_name)
                    cursor.execute("ALTER TABLE {} RENAME TO {}".format(
                        table_name, tmp_table_name))
                    cls.initialize_timing_table(cursor, table_name)
                    # Use cpu_time for real_time too. We don't have
                    # anything better right now.
                    cursor.execute("""\
                        INSERT INTO {}(timestamp, real_time, cpu_time)
                        SELECT timestamp, duration, duration
                        FROM {}""".format(table_name, tmp_table_name))
                    cursor.execute("DROP TABLE {}".format(tmp_table_name))

            # Add info to the history table.
            timestamp = datetime.datetime.utcnow().isoformat(" ")
            version = 6 # 0.0.6
            description = "Renamed field duration to cpu_time. " \
                "Added field real_time."
            tuple_ = (timestamp, version, description)
            cursor.execute(
                "INSERT INTO History VALUES (\"{}\", {}, \"{}\")".format(
                    *tuple_))

        # if database_version < 7:
        #   ...

        connection.commit()

    def __init__(self,
            database_name): # ="Timings"):
        """
        :param str database_name: Name of sqlite3 database to write results to.
        """
        assert not database_name is None

        timer_runner.TimerRunner.__init__(self)
        self.database_name = database_name

    def set_up(self,
            nr_timer_cases):
        self.connection = sqlite3.connect(self.database_name)
        self.cursor = self.connection.cursor()
        self.update_database(self.connection, self.cursor)

    def tear_down(self):
        # Otherwise data might not be written!
        self.connection.commit()

        self.cursor.close()
        self.connection.close()

        self.cursor = None
        self.connection = None

    def process_timer_result(self,
            result):
        key = result.keys()[0]
        table_name = key.replace(".", "_")

        if self.cursor.execute("PRAGMA TABLE_INFO({})".format(
                table_name)).fetchone() is None:
            self.initialize_timing_table(self.cursor, table_name)

        timestamp = result[key][0].isoformat(" ")
        # description = result[key][1]

        for timings in result[key][2]:
            # timings is a tuple of (real_time, cpu_time).
            tuple_ = (timestamp, timings[0], timings[1])
            self.cursor.execute("INSERT INTO {} VALUES (?, ?, ?)".format(
                table_name), tuple_)

    def database_is_consistent(self):
        """
        Test the integrity of the database.

        This function should always return True. If not, the database may be
        corrupt.
        """
        connection = sqlite3.connect(self.database_name)
        cursor = connection.cursor()

        # All tables must be non-empty.
        for master_table_record in cursor.execute(
                "select * from sqlite_master").fetchall():
            table_name = master_table_record[1]

            if table_name.find("time") != -1:
                table_record = cursor.execute(
                    "select * from {0}".format(table_name)).fetchone()
                if table_record is None:
                    return False

        # Passed all tests.
        return True
