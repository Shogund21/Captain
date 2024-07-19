import sqlite3

class JobApplicationTracker:
    def __init__(self, db_path='data/applications.db'):
        self.db_path = db_path
        self.conn = sqlite3.connect(self.db_path)
        self.create_table()

    def create_table(self):
        with self.conn:
            self.conn.execute('''CREATE TABLE IF NOT EXISTS applications (
                                 id INTEGER PRIMARY KEY,
                                 company TEXT NOT NULL,
                                 position TEXT NOT NULL,
                                 date TEXT NOT NULL,
                                 status TEXT NOT NULL)''')

    def add_application(self, company, position, date, status):
        with self.conn:
            self.conn.execute("INSERT INTO applications (company, position, date, status) VALUES (?, ?, ?, ?)",
                              (company, position, date, status))

    def get_applications(self):
        with self.conn:
            cur = self.conn.cursor()
            cur.execute("SELECT company, position, date, status FROM applications")
            return cur.fetchall()

    def update_application_status(self, application_id, new_status):
        with self.conn:
            self.conn.execute("UPDATE applications SET status = ? WHERE id = ?",
                              (new_status, application_id))

    def clear_all_applications(self):
        with self.conn:
            self.conn.execute("DELETE FROM applications")

    def close(self):
        self.conn.close()
