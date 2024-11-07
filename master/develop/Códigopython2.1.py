import json
import psycopg2

def handler(event, context):
    # Conexión a la base de datos
    connection = psycopg2.connect(
        host="db-identifier.region.rds.amazonaws.com",
        database="analytica_db",
        user="admin",
        password="password123"  # Esto debería manejarse como una variable segura
    )

    cursor = connection.cursor()
    cursor.execute("SELECT * FROM datos LIMIT 10;")
    rows = cursor.fetchall()

    cursor.close()
    connection.close()

    return {
        "statusCode": 200,
        "body": json.dumps(rows)
    }
