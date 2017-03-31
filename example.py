import cmd
import readline
import shlex
import sys
import signal

import db
import help
from repo import RepoManager


def signal_handler(signal, frame):
    db.close()
    sys.exit(0)
signal.signal(signal.SIGINT, signal_handler)

if 'libedit' in readline.__doc__:
    readline.parse_and_bind("bind ^I rl_complete")
else:
    readline.parse_and_bind("tab: complete")


class Example(cmd.Cmd):
    """Example"""

    def __init__(self, stage):
        super().__init__()
        valid_stages = ["local", "staging", "prod"]
        try:
            valid_stages.index(stage)
        except ValueError:
            print("Unknown stage: " + stage)
            print("Valid stages: " + str(valid_stages))
            sys.exit(-1)

        db.init(stage)
        self.prompt = "(%s) " % db.stage

    def emptyline(self):
        if self.lastcmd:
            self.lastcmd = ""
            return self.onecmd('\n')

    def do_create_repo(self, line):
        try:
            name, git = shlex.split(line)
            RepoManager.create_repo(name, git)
        except ValueError:
            print("Error: Name and git url must be specified. Use quotes if name contains spaces. ")

    def help_create_repo(self):
        help.display("Creates a new repository entry", "create_repo <name> <git url>",
                     "create_repo \"My Repo\" git@github.com:user/repo.git")

    def do_find_repo(self, line):
        nameQuery = line.strip()
        if nameQuery:
            RepoManager.find_and_print(nameQuery)
        else:
            print("Error: Search string must be specified.")

    def help_find_repo(self):
        help.display("Search repos by name", "find_repo <db_query>", "find_repo My Re%")


    def do_EOF(self, line):
        db.close()
        return True

    def help_EOF(self):
        help.display("Exit application", "Ctrl+D")

    do_exit = do_EOF
    help_exit = help_EOF


if __name__ == '__main__':
    if len(sys.argv) != 2:
        print("Stage must be specified!")
        sys.exit(-1)
    Example(sys.argv[1]).cmdloop()
