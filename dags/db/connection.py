import psycopg2
import pandas as pd
import datetime as dt


class DatabaseConection():
    def __init__(self, config: dict) -> None:
        self.config = config

    def get_conn(self):
        """ Connect to the database server """
        try:
            with psycopg2.connect(**self.config) as self.conn:
                print('Connected to the database server. ✅')
                return self.conn
        except (Exception, psycopg2.DatabaseError) as error:
            print(error)
            exit()

    def close_conn(self) -> None:
        """ Close connection """
        try:
            self.conn.close()
            print('Connection closed...✅')
        except (Exception, psycopg2.DatabaseError) as error:
            print(error)
            exit()


class PostgreConnection(DatabaseConection):
    def __init__(self, config):
        super().__init__(config)

    def extract_data(self, query: str) -> pd.DataFrame:
        """ Extract data from PostgreSQL """
        try:
            df = pd.read_sql_query(query, self.conn)
            print("Extract data... ✅")
        except (Exception, psycopg2.DatabaseError) as error:
            print(error)
        return df


class EDWConnection(DatabaseConection):
    def __init__(self, config: dict, schema: str, table_name: str):
        super().__init__(config)
        self.schema = schema
        self.table_name = table_name

    def create_table(self) -> None:
        """ Create table if not exist """
        try:
            with self.conn.cursor() as cursor:
                cursor.execute(f"""
                    CREATE TABLE IF NOT EXISTS {self.table_name} (
                        application_id      INT,
                        status              VARCHAR(50),
                        curp                VARCHAR(50),
                        full_name           VARCHAR(200),
                        total_applications  INT,
                        agency_name         VARCHAR(100),
                        load_date           TIMESTAMP
                    );
                """)
                self.conn.commit()
                print(f"Table {self.table_name} created successfully ✅")
        except (Exception, psycopg2.DatabaseError) as error:
            print(error)
            self.conn.rollback()

    def load_data(self, df: pd.DataFrame) -> None:
        """ Load data into the Datawarehouse """
        try:
            with self.conn.cursor() as cursor:
                for _, row in df.iterrows():
                    cursor.execute(f"""
                        INSERT INTO {self.schema}.{self.table_name}
                        (application_id, status, curp, full_name, total_applications, agency_name, load_date)
                        VALUES (%s, %s, %s, %s, %s, %s, %s)
                    """, (row['application_id'],
                          row['status'],
                          row['curp'],
                          row['full_name'],
                          row['total_applications'],
                          row['agency_name'],
                          dt.datetime.now().replace(microsecond=0)))
                self.conn.commit()
                print(f"Data inserted successfully into {self.table_name}. ✅")
        except (Exception, psycopg2.DatabaseError) as error:
            print(error)
            self.conn.rollback()
