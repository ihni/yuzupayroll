from db import Database
from config import DATABASE_CONFIG

# singleton pattern
db = Database(**DATABASE_CONFIG)

def create_app():
    return None

app = create_app()

if __name__ == '__main__':
    print("main will run the app")
    cnx = db.get_connection()