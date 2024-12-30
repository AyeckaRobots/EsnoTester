import sqlite3

# Data
data = {
    "QPSK": {
        "1/4": -1.5,
        "1/3": -0.4,
        "2/5": 0.5,
        "1/2": 1.8,
        "3/5": 3,
        "2/3": 3.9,
        "3/4": 4.8,
        "4/5": 5.6,
        "5/6": 6,
        "8/9": 7,
        "9/10": 7.2
    },
    "8PSK": {
        "3/5": 6.8,
        "2/3": 7.6,
        "3/4": 8.9,
        "5/6": 10.3,
        "8/9": 11.7,
        "9/10": 12
    },
    "16PSK": {
        "2/3": 10.2,
        "3/4": 11.1,
        "4/5": 12.1,
        "5/6": 12.7,
        "8/9": 13.9,
        "9/10": 14.2
    },
    "32PSK": {
        "3/4": 13.9,
        "4/5": 14.8,
        "5/6": 15.4,
        "8/9": 16.8,
        "9/10": 17.1
    }
}

# Define the database file path
DATABASE = "modulation_data.db"

# Keep a global variable to store the database connection
db = None

def get_db():
    """Connect to the SQLite database."""
    global db
    if db is None:
        db = sqlite3.connect(DATABASE)
    return db

# Create table and insert some data
def init_db():
    db = get_db()
    db.execute('''CREATE TABLE IF NOT EXISTS info_table (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    modulation TEXT NOT NULL,
                    code TEXT NOT NULL,
                    exp_esno REAL NOT NULL)''')
    # Insert data
    for modulation, codes in data.items():
        for code, exp_esno in codes.items():
            db.execute("INSERT INTO info_table (modulation, code, exp_esno) VALUES (?, ?, ?)", (modulation, code, exp_esno))
    db.commit()  # Commit the changes

def insert_db(modulation, code, exp_esno):
    db = get_db()
    db.execute("INSERT INTO info_table (modulation, code, exp_esno) VALUES (?, ?, ?)", (modulation, code, exp_esno))
    db.commit()  # Commit the changes

def get_data_as_string():
    db = get_db()
    cursor = db.execute("SELECT * FROM info_table")
    info_table = cursor.fetchall()

    # Format the rows into a string
    esno_dict = {}
    for info in info_table:
        esno_dict[f"{info[0]}"] = {f"{info[1]}": {f"{info[2]}": info[3]}}

    return esno_dict

def close_db():
    """Close the database connection."""
    global db
    if db is not None:
        db.close()
        db = None

def main():
    init_db()
    print(get_data_as_string())  # Print the data as a string
    close_db()  # Close the database connection

if __name__ == "__main__":
    main()
