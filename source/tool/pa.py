#!/usr/bin/env python

commandnames = {
    "history",
    "ls",
    "mv",
    "plot",
    "rm",
    "stat",
}
__doc__ = """
Manipulate and query a Performance Analyst database with timings

usage:
    pa [--help] <command> [<argument> ...]

options:
    -h, --help  Print help message

Supported pa commands are: {}

See 'pa <command> --help' for more information on a specific command.
""".format(", ".join(commandnames))
import importlib
import sys
import docopt


if __name__ == "__main__":

    arguments = docopt.docopt(__doc__,
                  version="pa version 0.0.10",
                  options_first=True)

    commandname = arguments["<command>"]

    if commandname not in commandnames:
        sys.exit("{} is not a pa command. See 'pa --help'.".format(commandname))

    argv = [commandname] + arguments["<argument>"]
    module_name = "pa_{}".format(commandname)
    module = importlib.import_module(module_name)
    result = docopt.docopt(module.__doc__, argv=argv)

    sys.exit(module.run(result))
