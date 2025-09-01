# Proyecto ETL Usuarios Sospechosos 🕵🏼‍♂️

Proyecto para automatizar el proceso ETL desde la base de datos PostgreSQL de `Hudson Hornet` hacia un Data Warehouse.

## Descripción 📝

Este proyecto utiliza Apache Airflow para ejecutar un DAG diario que extrae información de la base de datos PostgreSQL y la almacena en un Data Warehouse (DW). El objetivo es identificar usuarios con múltiples aplicaciones de crédito y guardar estos datos en una tabla dedicada del DW.

## Estructura de los DAGs 👨🏽‍💻

- [`dags/dag_etl.py`](dags/dag_etl.py): Define el DAG principal `etl_suspicious_users`, que ejecuta diariamente el proceso ETL.
- [`dags/extract_load.py`](dags/extract_load.py): Contiene las funciones `extract`, `load` y `extract_and_load` para extraer datos de PostgreSQL y cargarlos en el DW.

## Clases de conexión a bases de datos 🐍

- [`dags/db/connection.py`](dags/db/connection.py):
  - [`db.DatabaseConection`](dags/db/connection.py): Clase base para manejar conexiones a bases de datos.
  - [`db.PostgreConnection`](dags/db/connection.py): Extrae datos desde PostgreSQL.
  - [`db.EDWConnection`](dags/db/connection.py): Crea tablas y carga datos en el Data Warehouse.

## Configuración de variables de entorno 🛠️

Es necesario crear un archivo `.env` en la raíz del proyecto con las variables de conexión para PostgreSQL y el Data Warehouse. Ejemplo:

```env
POSTGRE_USERNAME="usuario_postgres"
POSTGRE_PASSWORD="password_postgres"
POSTGRE_HOST="host_postgres"
POSTGRE_PORT=5432
POSTGRE_DBNAME="nombre_db_postgres"

EDW_USERNAME="usuario_dw"
EDW_PASSWORD="password_dw"
EDW_HOST="host_dw"
EDW_PORT=5432
EDW_DBNAME="nombre_db_dw"
EDW_SCHEMA="public"
EDW_TABLE_NAME="dw_suspicious_users"
```

**Recuerda agregar la información de tu Data Warehouse en el `.env`.**

## Recomendación de entorno virtual 🖥️

Se recomienda crear un entorno virtual con `venv` para instalar las dependencias necesarias:

```sh
python3 -m venv .venv
source venv/bin/activate
pip install -r requirements.txt
```

Esto asegura que todas las dependencias del proyecto se instalen correctamente y evita conflictos con otras librerías del sistema.

## Ejecución local con Docker 🐋

1. Clona el repositorio y navega al directorio del proyecto.
2. Crea el archivo `.env` con las variables necesarias.
3. Ejecuta los servicios con Docker Compose:

```sh
docker-compose up
```

Esto levantará los servicios de Airflow, PostgreSQL y Redis. El DAG se ejecutará automáticamente cada día y podrás monitorear la ejecución desde la interfaz web de Airflow en [http://localhost:8080](http://localhost:8080).

- Usuario default: `airflow`
- Password default: `airflow`

---

Para más detalles revisa los archivos:

- [dags/dag_etl.py](dags/dag_etl.py)
- [dags/extract_load.py](dags/extract_load.py)
- [dags/db/connection.py](dags/db/connection.py)
