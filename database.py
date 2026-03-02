import sqlite3

def create_tables():
    conn = sqlite3.connect("placement.db")
    cur = conn.cursor()

    # Admin table
    cur.execute("""
        CREATE TABLE IF NOT EXISTS admin(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE,
            password TEXT
        )
    """)

    # Students
    cur.execute("""
        CREATE TABLE IF NOT EXISTS students(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            email TEXT UNIQUE,
            password TEXT,
            department TEXT,
            resume TEXT,
            status TEXT DEFAULT 'active'
        )
    """)

    # Companies
    cur.execute("""
        CREATE TABLE IF NOT EXISTS companies(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            email TEXT UNIQUE,
            password TEXT,
            hr_contact TEXT,
            website TEXT,
            approval TEXT DEFAULT 'pending'
        )
    """)

    # Drives
    cur.execute("""
        CREATE TABLE IF NOT EXISTS drives(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            company_id INTEGER,
            job_title TEXT,
            description TEXT,
            eligibility TEXT,
            deadline TEXT,
            status TEXT DEFAULT 'pending',
            FOREIGN KEY(company_id) REFERENCES companies(id)
        )
    """)

    # Applications
    cur.execute("""
        CREATE TABLE IF NOT EXISTS applications(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            student_id INTEGER,
            drive_id INTEGER,
            status TEXT DEFAULT 'Applied',
            FOREIGN KEY(student_id) REFERENCES students(id),
            FOREIGN KEY(drive_id) REFERENCES drives(id)
        )
    """)

    # Insert default admin
    cur.execute("SELECT * FROM admin")
    if cur.fetchone() is None:
        cur.execute("INSERT INTO admin(username, password) VALUES(?, ?)", 
                    ("admin", "admin123"))

    conn.commit()
    conn.close()


if __name__ == "__main__":
    create_tables()