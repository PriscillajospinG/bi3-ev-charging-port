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
def save_vehicle_event(track_id, class_name, entry, exit_time=None):
    query = """
        INSERT INTO vehicle_event (track_id, class_name, entry_time, exit_time)
        VALUES (%s, %s, %s, %s)
    """
    cursor.execute(query, (track_id, class_name, entry, exit_time))
    conn.commit()