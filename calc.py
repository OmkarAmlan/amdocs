import sqlite3

# Function to get connection strength between two users based on their connections
def get_connection_strength(user_id_1, user_id_2):
    # Establish a connection to the SQLite database
    conn = sqlite3.connect('your_database.db')  # Replace with your actual database path
    cursor = conn.cursor()

    # Check if there is a direct connection between the two users
    cursor.execute('''
        SELECT connection_strength 
        FROM connections 
        WHERE (user_id_1 = ? AND user_id_2 = ?) OR (user_id_1 = ? AND user_id_2 = ?)
    ''', (user_id_1, user_id_2, user_id_2, user_id_1))

    direct_connection = cursor.fetchone()

    if direct_connection:
        # If a direct connection exists, return the connection strength
        conn.close()
        return direct_connection[0]

    # If no direct connection exists, check for an indirect connection (i.e., mutual connections)
    cursor.execute('''
        SELECT DISTINCT c1.user_id_2 AS mutual_user
        FROM connections c1
        JOIN connections c2 ON c1.user_id_2 = c2.user_id_1
        WHERE c1.user_id_1 = ? AND c2.user_id_2 = ?
    ''', (user_id_1, user_id_2))

    mutual_connections = cursor.fetchall()

    if mutual_connections:
        # If there are mutual connections, return connection strength 2
        conn.close()
        return 2

    # If there are no direct or indirect connections, return connection strength 3+
    conn.close()
    return "3+"

print(get_connection_strength(1,4))