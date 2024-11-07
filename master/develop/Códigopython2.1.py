from fastapi import FastAPI, HTTPException
import psycopg2  # Librería para la conexion con la bases de datos PostgreSQL

# Inicializacion de la app de FastAPI
app = FastAPI()

# Configuración de la conexión hacia la base de datos
def get_db_connection():
        conn = psycopg2.connect(
        dbname="challenge_db",
        user="admin",
        password="pasword123",
        host="host",
        port="8080"
    )
    return conn

@app.get("/data")
async def read_data():
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("SELECT * FROM mi_tabla LIMIT 10;")
        rows = cursor.fetchall()
        return {"data": rows}
    except Exception as e:
        raise HTTPException(status_code=500, detail="Error al leer datos")
    finally:
        cursor.close()
        conn.close()
