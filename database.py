import sqlite3


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
def insert_project(conn, project_name, project_path, atime, mtime, is_git):
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO projects (project_name, project_path, atime, mtime, is_git)
        VALUES (?, ?, ?, ?, ?)
    ''', (project_name, project_path, atime, mtime, is_git))
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


def fetch_projects(conn):
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM projects')
    return cursor.fetchall()


def create_db_connection(db_file):
    return sqlite3.connect(db_file)


def example():
    connection = sqlite3.connect("database/term_mark.sqlite")
    create_table(connection)
    connection.close()


if __name__ == "__main__":
    example()
