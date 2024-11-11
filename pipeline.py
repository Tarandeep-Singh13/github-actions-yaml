from prefect import flow, task
import psycopg2
import psycopg2.extras


@task
def extract_data_from_postgres():
    conn = psycopg2.connect(
        dbname="postgres",
        user="mt24002",
        password="mt24002@m04y24",
        host="w3.training5.modak.com",
        port="5432"
    )
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM taran")
    rows = cursor.fetchall()
    columns = [desc[0] for desc in cursor.description]
    cursor.close()
    conn.close()
    return rows, columns


@task
def load_data_into_postgres(data):
    rows, columns = data
    conn = psycopg2.connect(
        dbname="postgres",
        user="mt24002",
        password="mt24002@m04y24",
        host="w3.training5.modak.com",
        port="5432"
    )
    cursor = conn.cursor()

    # Insert data into taran13
    insert_query = f"INSERT INTO taran13 ({', '.join(columns)}) VALUES %s"
    # Prepare data for batch insert
    psycopg2.extras.execute_values(cursor, insert_query, rows)

    conn.commit()
    cursor.close()
    conn.close()


@flow
def pipeline():
    data = extract_data_from_postgres()
    load_data_into_postgres(data)


if __name__ == "__main__":
    pipeline()
