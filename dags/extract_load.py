import os
import pandas as pd
from dotenv import load_dotenv
from db import PostgreConnection, EDWConnection

load_dotenv()

POSTGRE_CONN = {
    "user": os.getenv('POSTGRE_USERNAME'),
    "password": os.getenv('POSTGRE_PASSWORD'),
    "host": os.getenv('POSTGRE_HOST'),
    "port": os.getenv('POSTGRE_PORT'),
    "dbname": os.getenv('POSTGRE_DBNAME'),
}

EDW_CONN = {
    "user": os.getenv('EDW_USERNAME'),
    "password": os.getenv('EDW_PASSWORD'),
    "host": os.getenv('EDW_HOST'),
    "port": os.getenv('EDW_PORT'),
    "dbname": os.getenv('EDW_DBNAME'),
}

SCHEMA = os.getenv('EDW_SCHEMA')

TABLE_NAME = os.getenv('EDW_TABLE_NAME')

QUERY = """
WITH applicant_cte AS (
	SELECT DISTINCT
		a.applicant_id,
		a.curp,
		CONCAT_WS(' ',trim(p.first_name), trim(p.last_name)) AS "full_name",
		COUNT(curp) OVER (PARTITION BY curp) as "total_applications"
	FROM hudson_hornet_db.applicant a
	LEFT JOIN hudson_hornet_db.person p ON p.person_id = a.person_id
), agency_cte AS (
	SELECT
		se.employment_id,
		a.agency_id,
		a.name
	FROM hudson_hornet_db.seller_employment se
	LEFT JOIN hudson_hornet_db.agency a ON a.agency_id = se.agency_id
)

SELECT
	ca.application_id,
	ca.status,
	a.curp,
	a.full_name,
	a.total_applications,
	e.name AS "agency_name"
FROM hudson_hornet_db.credit_application ca
LEFT JOIN applicant_cte a ON a.applicant_id = ca.applicant_id
LEFT JOIN agency_cte e ON e.employment_id = ca.employment_id
ORDER BY COALESCE(a.total_applications,0) DESC;
"""  # noqa


def extract() -> pd.DataFrame:
    postgre = PostgreConnection(config=POSTGRE_CONN)
    postgre.get_conn()
    df = postgre.extract_data(query=QUERY)
    postgre.close_conn()
    return df


def load(data: pd.DataFrame) -> None:
    edw_table = EDWConnection(config=EDW_CONN, schema=SCHEMA, table_name=TABLE_NAME)
    edw_table.get_conn()
    edw_table.create_table()
    edw_table.load_data(df=data)
    edw_table.close_conn()


def extract_and_load() -> None:
    df = extract()
    load(data=df)
