# pa.py
The PerformanceAnalyst stores information in a database. This command
can be used to query and manage this database and to create plots of
the performance results.

The commandline syntax is similar to tools like
[svn](http://subversion.tigris.org) and
[git](http://git-scm.com). The command uses multiple sub-commands with
their own set of commandline options.

Type:

```bash
pa.py --help
```

```bash
pa.py help
```

for the general commandline usage.

Type:

```bash
pa.py help <command>
```

```bash
pa.py <command> --help
```

For the commandline usage of a sub-command.

Here is an example that creates a pdf with a plot with three graphs:

```bash
pa.py plot test_timings.pdf test_timings.sqlite \
    my_module_timers_time_a \
    my_module_timers_time_b \
    my_module_timers_time_c
```

Now follows a short rundown of the usage of the sub-commands of the pa.py command. Check the tool's usage for further details.

The high-level usage of the pa.py command is as folows:

```bash
pa.py [options] <command>
```

Command is one of the sub-commands:

##ls
List the contents of the performance database:

```bash
pa.py ls [options] <database> {timer}+
```

| **argument** | **description**               |
| ------------ | ----------------------------- |
| database     | Name of performance database  |
| timer        | Name of timer                 |


##mv
Move (rename) timers stored in the performance database:

```bash
pa.py mv [options] <database> <current timer> <new timer>
```

| **argument**  | **description**               |
| ------------- | ----------------------------- |
| database      | Name of performance database  |
| current timer | Current name of timer         |
| new timer     | New name of timer             |


##plot
Plot timers stored in the performance database:

```bash
pa.py plot [options] <output> <database> <timer>+
```

The plot will contain two lines for each timer: a solid line for the
cpu-time and a dashed line for the real-time.

| **argument**  | **description**               |
| ------------- | ----------------------------- |
| output        | Name of output pdf            |
| database      | Name of performance database  |
| timer         | Name of timer                 |


##rm
Remove timers stored in the performance database:

```bash
pa.py rm [options] <database> <timer>+
```

| **argument**  | **description**               |
| ------------- | ----------------------------- |
| database      | Name of performance database  |
| timer         | Name of timer                 |


##stat
Calculate statistics of timers stored in the performance database:

```bash
pa.py stat [options] <database> <timer>+
```

| **argument**  | **description**               |
| ------------- | ----------------------------- |
| database      | Name of performance database  |
| timer         | Name of timer                 |


##history
Print history of the database:

```bash
pa.py stat [options] <database>
```

| **argument**  | **description**               |
| ------------- | ----------------------------- |
| database      | Name of performance database  |
