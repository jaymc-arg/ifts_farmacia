# db.py
import sqlite3
from datetime import datetime
from config.constants import DB_NAME

class Database:
    
    def __init__(self, db_name=DB_NAME):
        self.connection = sqlite3.connect(db_name)
        self.create_tables()
        self.start_up()

    def create_tables(self):
        with self.connection as conn:
            conn.executescript(
                "CREATE TABLE IF NOT EXISTS users (username TEXT PRIMARY KEY, password TEXT);" \
                "CREATE TABLE IF NOT EXISTS filas (id INTEGER PRIMARY KEY AUTOINCREMENT, \
                    station TEXT, \
                    created_at TIMESTAMP NOT NULL DEFAULT (datetime('now','localtime')), \
                    attended_at TIMESTAMP DEFAULT NULL, \
                    waiting_time INTEGER DEFAULT NULL, \
                    finished_at TIMESTAMP DEFAULT NULL, \
                    attention_time INTEGER DEFAULT NULL);" \
                "CREATE TABLE IF NOT EXISTS productos (product_id INTEGER PRIMARY KEY AUTOINCREMENT, nombre TEXT, cantidad INTEGER);" \

            )
            

    def start_up(self):
        with self.connection as conn:
            try:
                # Check if the tables are empty
                cursor = conn.cursor()
                cursor.execute("SELECT COUNT(*) FROM users")
                users_count = cursor.fetchone()[0]

                cursor.execute("SELECT COUNT(*) FROM productos")
                products_count = cursor.fetchone()[0]

                print(users_count, products_count)
                if users_count == 0 and products_count == 0:
                    conn.executescript(
                        "INSERT INTO users (username, password) VALUES ('admin', 'admin'); \
                         INSERT INTO users (username, password) VALUES ('recepcion', 'recepcion'); \
                         INSERT INTO users (username, password) VALUES ('reportes', 'reportes'); \
                         INSERT INTO users (username, password) VALUES ('atencion', 'atencion'); \
                         INSERT INTO productos (nombre, cantidad) VALUES ('remedio', 10);"
                    )
                return True
            except sqlite3.IntegrityError:
                return False
            except sqlite3.Error as e:
                print(f"An error occurred: {e}")
                return False


    
    def get_user(self, username):
        # print('>>>>>>>>>', username)
        with self.connection as conn:
            cursor = conn.execute(
                "SELECT password FROM users WHERE username = ?", (username, )
            )

            return cursor.fetchone()

    def insert_event(self, station):
        with self.connection as conn:
            conn.execute(
                "INSERT INTO filas (station) VALUES (?)",
                (station,)
            )

            cursor = conn.execute(
                "SELECT * FROM filas ORDER BY created_at DESC"
            ).fetchone()
            
            return cursor[0]
    
    def get_events(self, station):
        with self.connection as conn :
            cursor = conn.execute(
                "SELECT * FROM filas WHERE station = ? AND finished_at IS NULL AND attended_at IS NULL ORDER BY created_at ASC;",
                # "SELECT * FROM filas WHERE station = ? ORDER BY created_at DESC;",
                (station,)
            ).fetchall()
            
            
            return cursor
        
    def get_every_event(self, station):
        with self.connection as conn :
            cursor = conn.execute(
                "SELECT * FROM filas ORDER BY created_at ASC;",
                # "SELECT * FROM filas WHERE station = ? ORDER BY created_at DESC;",
            ).fetchall()
            return cursor


    def get_last_event(self, station):
        with self.connection as conn :
            cursor = conn.execute(
                "SELECT * FROM filas WHERE station = ? AND finished_at IS NULL AND attended_at IS NULL ORDER BY created_at ASC;",
                # "SELECT * FROM filas WHERE station = ? ORDER BY created_at DESC;",
                (station,)
            ).fetchone()
            
            # print(cursor)
            return cursor
            
    def attend_event(self, id):
        local_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        
        with self.connection as conn :
            conn.execute(
                "UPDATE filas SET attended_at = ? WHERE id = ?;",
                (local_time, id, )
            )
            conn.execute(
                "UPDATE filas SET waiting_time = (strftime('%s', attended_at) - strftime('%s', created_at))"
                "WHERE attended_at IS NOT NULL AND created_at IS NOT NULL AND finished_at IS NULL and id = ?",
                (id, )
            )
            
    def finish_event(self, id):
        local_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        
        with self.connection as conn :
            conn.execute(
                "UPDATE filas SET finished_at = ? WHERE id = ?;",
                (local_time, id, )
            )
            conn.execute(
                "UPDATE filas SET attention_time = (strftime('%s', finished_at) - strftime('%s', attended_at))"
                "WHERE finished_at IS NOT NULL AND attended_at IS NOT NULL and id = ?",
                (id, )
            )
            
    def get_stock(self):
        with self.connection as conn :
            cursor = conn.execute("SELECT cantidad FROM productos").fetchone()
        return cursor[0]
            
    def sale_product(self):
        
        with self.connection as conn :          
            conn.execute(
                "UPDATE productos SET cantidad = cantidad - 1 WHERE nombre = 'remedio'",
            )
    
    
            
            
    def get_report(self, local_now):
        with self.connection as conn :
            finished = conn.execute(
                "SELECT id, waiting_time, attention_time FROM filas WHERE attended_at IS NOT NULL ORDER BY created_at ASC;",
            ).fetchall()
            
            not_finished = conn.execute(
                """
                SELECT id,
                    (strftime('%s', ?) - strftime('%s', created_at)) AS waiting_time
                FROM filas
                WHERE waiting_time IS NULL;
                """, (local_now, )
            ).fetchall()
            
            return finished, not_finished
        

    
        