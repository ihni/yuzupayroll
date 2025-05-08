from app import db, create_app

app = create_app()

if __name__ == '__main__':
    cnx = db.get_connection()
    app.run(debug=True, host='0.0.0.0', port=5000,)