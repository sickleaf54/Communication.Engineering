import sqlite3

class app:
    def _init_(self, db_name):
        self.db_name = db_name
        self.create_table()

    def create_table(self):
        conn = sqlite3.connect(self.db_name)
        c = conn.cursor()
        c.execute('''CREATE TABLE IF NOT EXISTS match_results
                     (id INTEGER PRIMARY KEY AUTOINCREMENT,
                      time TEXT,
                      winner TEXT,
                      loser TEXT)''')
        conn.commit()
        conn.close()

    def save_match_result(self, time, winner, loser):
        conn = sqlite3.connect(self.db_name)
        c = conn.cursor()
        c.execute("INSERT INTO match_results (time, winner, loser) VALUES (?, ?, ?)", (time, winner, loser))
        conn.commit()
        conn.close()

    def get_match_results(self):
        conn = sqlite3.connect(self.db_name)
        c = conn.cursor()
        c.execute("SELECT * FROM match_results")
        rows = c.fetchall()
        conn.close()
        return rows

def generate_random_date(start_date, end_date):
    start_timestamp = datetime.timestamp(start_date)
    end_timestamp = datetime.timestamp(end_date)
    random_timestamp = random.uniform(start_timestamp, end_timestamp)
    return datetime.fromtimestamp(random_timestamp)

if _name_ == "_main_":
    db_name = "match_results.db"
    adapter = DataAdapter(db_name)

    start_date = datetime(2024, 4, 10)
    end_date = datetime(2024, 4, 11)

    for i in range(1, 11):
        match_time = generate_random_date(start_date, end_date)
        winner = "Player 1" if random.random() < 0.5 else "Player 2"
        loser = "Player 2" if winner == "Player 1" else "Player 1"
        adapter.save_match_result(match_time.strftime("%d/%m/%Y %I:%M %p"), winner, loser)

    print("Match results saved to SQLite database.")

    # Now, retrieve data from the database and generate HTML table
    match_results = adapter.get_match_results()

    # Generate HTML table
    html_table = "<table>\n<thead>\n<tr>\n<th>S.No.</th>\n<th>Time</th>\n<th>Winner</th>\n<th>Looser</th>\n</tr>\n</thead>\n<tbody>\n"

    for idx, result in enumerate(match_results, 1):
        html_table += f"<tr>\n<td>{idx}</td>\n<td>{result[1]}</td>\n<td>{result[2]}</td>\n<td>{result[3]}</td>\n</tr>\n"

    html_table += "</tbody>\n</table>\n"

    print("Generated HTML Table:")
    print(html_table)
