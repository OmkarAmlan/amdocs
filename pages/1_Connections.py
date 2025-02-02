import streamlit as st
import sqlite3
import networkx as nx
import matplotlib.pyplot as plt

# Function to create a SQLite connection and create the connections table if not exists
def create_connection():
    # Establish a connection to the SQLite database
    conn = sqlite3.connect('your_database.db')  # Replace with your actual database path
    
    # Create the 'connections' table if it doesn't exist
    cursor = conn.cursor()
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS connections (
        user_id_1 INTEGER NOT NULL,
        user_id_2 INTEGER NOT NULL,
        connection_strength INTEGER CHECK(connection_strength IN (1, 2, 3)) NOT NULL,
        PRIMARY KEY (user_id_1, user_id_2)
    );
    ''')
    conn.commit()
    
    return conn


# Function to get connections and strength from the database
def get_connections():
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT user_id_1, user_id_2, connection_strength FROM connections')
    connections = cursor.fetchall()
    conn.close()
    return connections

# Function to visualize connections using NetworkX
def visualize_connections():
    connections = get_connections()
    G = nx.Graph()

    # Add edges to the graph with connection strength as edge attribute
    for user_id_1, user_id_2, strength in connections:
        G.add_edge(user_id_1, user_id_2, weight=strength)

    # Create a layout for visualization
    pos = nx.spring_layout(G)

    # Draw the graph
    plt.figure(figsize=(10, 8))
    nx.draw(G, pos, with_labels=True, node_color='lightblue', node_size=2000, font_size=12, font_weight='bold')
    
    # Draw edge labels for connection strength
    edge_labels = nx.get_edge_attributes(G, 'weight')
    nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels)
    
    st.pyplot()

# Function to connect users by clicking a button
def connect_users(user_id_1, user_id_2):
    conn = create_connection()
    cursor = conn.cursor()

    # Check if a connection already exists
    cursor.execute('''
        SELECT connection_strength 
        FROM connections 
        WHERE (user_id_1 = ? AND user_id_2 = ?) OR (user_id_1 = ? AND user_id_2 = ?)
    ''', (user_id_1, user_id_2, user_id_2, user_id_1))

    existing_connection = cursor.fetchone()
    if existing_connection:
        connection_strength = existing_connection[0]
        st.write(f"Connection already exists with strength {connection_strength}.")
    else:
        # Ask user for connection strength
        connection_strength = st.selectbox(
            f"Select connection strength between user {user_id_1} and user {user_id_2}",
            [1, 2, 3]
        )

        # Insert the connection into the database
        cursor.execute('''
            INSERT INTO connections (user_id_1, user_id_2, connection_strength)
            VALUES (?, ?, ?)
        ''', (user_id_1, user_id_2, connection_strength))
        conn.commit()
        st.write(f"Connection established with strength {connection_strength}.")

    conn.close()

# Main Streamlit interface
st.title("User Connections")

# User selection for connection
user_id_1 = st.selectbox("Select first user", range(1, 11))
user_id_2 = st.selectbox("Select second user", range(1, 11))

if st.button("Connect"):
    if user_id_1 != user_id_2:
        connect_users(user_id_1, user_id_2)
    else:
        st.warning("You cannot connect a user to themselves.")

# Visualize the current connections
st.subheader("Current User Connections")
visualize_connections()
