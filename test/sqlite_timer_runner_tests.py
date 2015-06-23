import os.path
import sqlite3
import unittest
import performance_analyst as pa
import my_module_timers


class SQLiteTimerRunnerTests(unittest.TestCase):

    database_name = "TestTimings.sqlite"

    def setUp(self):
        if os.path.exists(self.database_name):
            os.remove(self.database_name)

    def tearDown(self):
        if os.path.exists(self.database_name):
            os.remove(self.database_name)

    def test001(self):
        """Test running the example timer case"""
        runner = pa.sqlite_timer_runner.SQLiteTimerRunner(database_name=
            self.database_name)
        result = runner.run(pa.timer_suite.TimerSuite([
            my_module_timers.MyModuleTimers("time_a"),
            my_module_timers.MyModuleTimers("time_b"),
            my_module_timers.MyModuleTimers("time_c"),
        ]))

        self.assert_(runner.database_is_consistent())

        self.assertEqual(len(result), 3)
        self.assert_("MyModuleTimers.time_a" in result)
        self.assert_("MyModuleTimers.time_b" in result)
        self.assert_("MyModuleTimers.time_c" in result)

        self.assert_(os.path.isfile(self.database_name))
        connection = sqlite3.connect(self.database_name)
        cursor = connection.cursor()

        table_names = [
            "MyModuleTimers_time_a",
            "MyModuleTimers_time_b",
            "MyModuleTimers_time_c"
        ]

        for table_name in table_names:
            # Check existence of tables in data base.
            self.assert_(not cursor.execute(
                "pragma table_info(%s)" % (table_name)).fetchone() is None)

            # Check format of tables.
            # TODO

            # Check contents of tables.
            # TODO

        records = cursor.execute(
            "select * from MyModuleTimers_time_a").fetchall()
        self.assertEqual(len(records), 2)
        records = cursor.execute(
            "select * from MyModuleTimers_time_b").fetchall()
        self.assertEqual(len(records), 3)
        records = cursor.execute(
            "select * from MyModuleTimers_time_c").fetchall()
        self.assertEqual(len(records), 1)

        connection.close()
        self.assert_(os.path.isfile(self.database_name))
        connection = sqlite3.connect(self.database_name)
        cursor = connection.cursor()

        # Make sure we can run the timers again using the same database.
        result = runner.run(pa.timer_suite.TimerSuite([
            pa.timer_suite.TimerSuite([
                my_module_timers.MyModuleTimers("time_a"),
                my_module_timers.MyModuleTimers("time_b"),
                my_module_timers.MyModuleTimers("time_c"),
        ])]))

        self.assert_(runner.database_is_consistent())

        # Test that tables have grown.
        records = cursor.execute(
            "select * from MyModuleTimers_time_a").fetchall()
        self.assertEqual(len(records), 4)
        records = cursor.execute(
            "select * from MyModuleTimers_time_b").fetchall()
        self.assertEqual(len(records), 6)
        records = cursor.execute(
            "select * from MyModuleTimers_time_c").fetchall()
        self.assertEqual(len(records), 2)

    def test002(self):
        """Test running a failing timer case"""
        runner = pa.sqlite_timer_runner.SQLiteTimerRunner(database_name=
            self.database_name)

        self.assertRaises(AssertionError, runner.run,
                pa.timer_suite.TimerSuite([
            my_module_timers.MyModuleTimers("timeRaiseException"),
        ]))

        self.assert_(runner.database_is_consistent())
