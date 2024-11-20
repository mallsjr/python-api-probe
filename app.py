from flask import Flask, request, jsonify
import sqlite3

def get_db_connection():
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row

    # Create the table if it doesn't exist
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS items (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            description TEXT,
            price REAL Not NULL
        )
    ''')
    conn.commit()
    return conn

app = Flask(__name__)

# Create a new record
@app.route('/items', methods=['POST'])
def create_item():
    conn = get_db_connection()
    cursor = conn.cursor()
    item = request.get_json()
    cursor.execute("INSERT INTO items (name, description, price) VALUES (?, ?, ?)", (item['name'], item['description'], item['price']))
    conn.commit()
    new_item = dict(cursor.execute('SELECT * FROM items WHERE id = ?', (cursor.lastrowid,)).fetchone())
    conn.close()
    return jsonify(new_item), 201

# Read all records
@app.route('/items', methods=['GET'])
def get_items():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM items')
    items = cursor.fetchall()
    conn.close()
    return jsonify([dict(row) for row in items])

# Read a single record
@app.route('/items/<int:id>', methods=['GET'])
def get_item(id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM items WHERE id = ?', (id,))
    item = cursor.fetchone()
    conn.close()
    if item is None:
        return jsonify({'error': 'Item not found'}), 404
    return jsonify(dict(item))

# Update a record
@app.route('/items/<int:id>', methods=['PUT'])
def update_item(id):
    conn = get_db_connection()
    cursor = conn.cursor()
    item = request.get_json()
    cursor.execute("UPDATE items SET name = ?, description = ?, price = ? WHERE id = ?", (item['name'], item['description'], item['price'], id))
    conn.commit()
    conn.close()
    return jsonify(item)

# Delete a record
@app.route('/items/<int:id>', methods=['DELETE'])
def delete_item(id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('DELETE FROM items WHERE id = ?', (id,))
    conn.commit()
    conn.close()
    return '', 204

if __name__ == '__main__':
    app.run(debug=True)
