import psycopg2
import re
import sys
from tabulate import tabulate
from subprocess import Popen, PIPE
import cmd


def init(db_stage):
    global conn, stage
    stage = db_stage.upper()
    if db_stage == 'local':
        conn = local_connection()
    else:
        conn = heroku_connection(db_stage)
    cursor = conn.cursor()
    cursor.execute("set search_path to core,public")
    conn.commit()
    cursor.close()
    print("Connected to stage: %s" % stage)


def close():
    conn.close()
    print("\nGoodbye!")


def local_connection():
    connection_string = "dbname='postgres' user='postgres' host='db' port='5432' password=''"
    return psycopg2.connect(connection_string)


def heroku_connection(stage):
    app = "heroku_app_name-" + stage
    p = Popen(["heroku", "pg:credentials", "DATABASE", "-a", app], stdin=PIPE, stdout=PIPE,
              stderr=PIPE)
    output, err = p.communicate()
    rc = p.returncode

    if rc != 0:
        print("Unable to get db credentials for %s: %s" % (app, err.decode('utf-8')))
        sys.exit(1)

    regex = 'dbname=(.*) host=(.*) port=(.*) user=(.*) password=(.*) sslmode=(.*)'
    match = re.search(regex, output.decode('utf-8'))

    connection_string = "dbname='%s' user='%s' host='%s' port='%s' password='%s' sslmode='require'" % (
        match.group(1), match.group(4), match.group(2), match.group(3), match.group(5))
    return psycopg2.connect(connection_string)


def select_and_print(statement, arguments):
    cur = conn.cursor()
    cur.execute(statement, arguments)
    data_rows = []
    column_names = [desc[0] for desc in cur.description]
    for row in cur:
        data_rows.append(row)
    cur.close()

    print(tabulate(data_rows, column_names))


class CommitScope:
    def __init__(self, description):
        self.description = description
        self.committed = False


class CommitRollbackCommand(cmd.Cmd):
    def __init__(self, scope):
        super().__init__()
        self.scope = scope
        self.prompt = "%s " % (scope.description)

    def do_yes(self, line):
        conn.commit()
        print("Saved!")
        self.scope.committed = True
        return True

    def do_no(self, line):
        conn.rollback()
        print("Discarded!")
        self.scope.committed = False
        return True

    def do_exit(self, line):
        conn.rollback()
        close()
        sys.exit(0)
