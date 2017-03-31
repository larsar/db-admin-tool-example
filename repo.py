import db
import psycopg2
from db import CommitRollbackCommand, CommitScope


class Repo(object):
    def __init__(self, id, name, git_url):
        self.id = id
        self.name = name
        self.git_url = git_url

    def print_details(self):
        db.select_and_print(
            "SELECT id, name, git_url from sec.repos WHERE id = %s",
            [self.id])


class RepoManager(object):
    @staticmethod
    def create_repo(name, git_url):
        cur = db.conn.cursor()
        try:
            cur.execute("INSERT into sec.repos(name, git_url) VALUES (%s, %s) RETURNING id",
                        [name, git_url])
            row = cur.fetchone()
        except psycopg2.IntegrityError as error:
            print("ERROR: Inserting repo (%s) failed" % (name))
            db.conn.rollback()
            return
        finally:
            cur.close()

        repo_id = row[0]

        print("New repo:")
        db.select_and_print("SELECT id, name, git_url from sec.repos WHERE id = %s",
                            [repo_id])

        cs = CommitScope("Save new repo(yes/no)?")
        CommitRollbackCommand(cs).cmdloop()

    @staticmethod
    def find(nameQuery):
        cur = db.conn.cursor()
        cur.execute("SELECT id, name, git_url from sec.repos WHERE LOWER(name) LIKE LOWER(%s)", [nameQuery])
        rows = cur.fetchall()
        cur.close()
        return RepoManager.rows_to_repos(rows)

    @staticmethod
    def find_and_print(nameQuery):
        db.select_and_print("SELECT id, name, git_url from sec.repos WHERE LOWER(name) LIKE LOWER(%s)", [nameQuery])


    @staticmethod
    def get_by_id(id):
        cur = db.conn.cursor()
        cur.execute("SELECT id, name, git_url from sec.repos where id = %s", [id])
        row = cur.fetchone()
        if row == None:
            return None
        cur.close()
        return RepoManager.row_to_repos(row)


    @staticmethod
    def row_to_repos(row):
        return Repo(row[0], row[1], row[2])

    @staticmethod
    def rows_to_repos(rows):
        repos = []
        for row in rows:
            repos.append(Repo(row[0], row[1], row[2]))
        return repos
