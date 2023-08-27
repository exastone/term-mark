import os
import sqlite3


def table_exists(connection, table_name="project"):
    cursor = connection.cursor()
    cursor.execute(f"SELECT name FROM sqlite_master WHERE type='table' AND name='{table_name}'")
    return cursor.fetchone() is not None


def create_table(conn):
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS projects (
            id INTEGER PRIMARY KEY,
            project_name TEXT,
            project_path TEXT,
            atime INT,
            mtime INT,
            is_git INT
        )
    ''')
    conn.commit()


# add project row
def insert_project(conn, proj):
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO projects (project_name, project_path, atime, mtime, is_git)
        VALUES (?, ?, ?, ?, ?)
    ''', (proj["project_name"], proj["project_path"], proj["atime"], proj["mtime"], proj["is_git"]))

    # Commit the changes
    conn.commit()


def remove_project_by_name(conn, project_name):
    cursor = conn.cursor()
    cursor.execute('''
        DELETE FROM projects
        WHERE project_name = ?
    ''', (project_name,))
    # Commit the changes
    conn.commit()


def remove_project_by_path(conn, project_path):
    cursor = conn.cursor()
    cursor.execute('''
        DELETE FROM projects
        WHERE project_path = ?
    ''', (project_path,))
    # Commit the changes
    conn.commit()


# check if directory exists
def directory_exists(conn, project_path):
    cursor = conn.cursor()
    cursor.execute('''
        SELECT EXISTS(
            SELECT 1
            FROM projects
            WHERE project_path = ?
        )
    ''', (project_path,))
    return cursor.fetchone()[0] == 1


def fetch_projects(conn):
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM projects')
    return cursor.fetchall()


def create_db_connection(db_file):
    return sqlite3.connect(db_file)


def example():
    connection = sqlite3.connect(os.environ["TM_PATH_DB"])
    create_table(connection)
    connection.close()


if __name__ == "__main__":
    example()
