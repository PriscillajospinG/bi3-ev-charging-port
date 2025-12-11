import psycopg2

conn = psycopg2.connect(
    host="dxa9gx2exf.o5no6bjuna.tsdb.cloud.timescale.com",
    port=39979,
    database="tsdb",
    user="tsdbadmin",
    password="roiu4nalbvaabahr",
    sslmode="require"
)

cursor = conn.cursor()

def save_vehicle_metrics(timestamp, vehicle_count, session_count, occupancy_rate, queue_length):
    """
    Save vehicle metrics for a given timestamp/frame.
    """
    query = """
        INSERT INTO vehicle_metrics (timestamp, vehicle_count, session_count, occupancy_rate, queue_length)
        VALUES (%s, %s, %s, %s, %s)
    """
    cursor.execute(query, (timestamp, vehicle_count, session_count, occupancy_rate, queue_length))
    conn.commit()