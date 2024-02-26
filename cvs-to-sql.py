import psycopg2
from psycopg2 import sql
import csv


def create_table_from_csv(table_name, csv_file_path):

    try:
        connection = psycopg2.connect(
            database="portofolio",
            user="postgres",
            password="postgres",
            host="localhost",
            port="5432",
        )
        cursor = connection.cursor()

        with open(csv_file_path, "r") as file:
            csv_reader = csv.reader(file)
            header = next(csv_reader)
            columns = [sql.Identifier(column) for column in header]

        create_table_query = sql.SQL("CREATE TABLE {} ({})").format(
            sql.Identifier(table_name),
            sql.SQL(", ").join(
                [sql.SQL("{} VARCHAR").format(column) for column in columns]
            ),
        )

        cursor.execute(create_table_query)
        connection.commit()

        with open(csv_file_path, "r") as file:
            cursor.copy_expert(
                sql.SQL("COPY {} FROM STDIN CSV HEADER").format(
                    sql.Identifier(table_name)
                ),
                file,
            )
            connection.commit()

        print(f"Table '{table_name}' created successfully and data loaded from CSV.")
    except psycopg2.Error as e:
        print("Error:", e)
    finally:
        if connection is not None:
            connection.close()


create_table_from_csv("covid_data", "ds/csvs/riginal/covid_data.csv")
