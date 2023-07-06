import os
import time
import sys
import psycopg2
from psycopg2 import pool
from dotenv import load_dotenv
from .logger_config import logger

# Load the .env file
load_dotenv()

# You might want to move these credentials to a configuration file
db_name = os.environ.get("DB_NAME")
db_user = os.environ.get("DB_USER")
db_password = os.environ.get("DB_PASSWORD")
db_host = os.environ.get("DB_HOST")
db_port = os.environ.get("DB_PORT")

try:
    connection_pool = psycopg2.pool.SimpleConnectionPool(
        1,
        20,
        database=db_name,
        user=db_user,
        password=db_password,
        host=db_host,
        port=db_port,
        sslmode="require",
    )

    if connection_pool:
        logger.info("Connection pool created successfully")

except (Exception, psycopg2.DatabaseError) as error:
    logger.error("Error while connecting to PostgreSQL", exc_info=True)


def get_connection():
    max_retries = 3
    backoff_factor = 0.2  # delay will be [0.2, 0.4, 0.8] seconds

    for i in range(max_retries):
        conn = connection_pool.getconn()

        # Verify the connection is valid before returning it
        try:
            conn.cursor().execute("SELECT 1")
            return conn  # If we get here, the connection is valid
        except psycopg2.DatabaseError as err:
            logger.error("Invalid connection: ", exc_info=True)
            connection_pool.putconn(conn)  # Put the connection back to the pool

            # If we've exhausted the retries, raise the exception to the caller
            if i == max_retries - 1:
                logger.error(
                    "Failed to get a valid connection after %d retries", max_retries
                )
                raise
            else:
                delay = backoff_factor * (2**i)  # Exponential backoff
                time.sleep(delay)


def release_connection(conn):
    return connection_pool.putconn(conn)


def execute_query(query, params):
    try:
        conn = get_connection()
    except psycopg2.DatabaseError as error:
        logger.error("Failed to connect to the database", exc_info=True)
        sys.exit(1)

    try:
        cursor = conn.cursor()
        cursor.execute(query, params)
        conn.commit()
    except Exception as e:
        logger.error(f"Error executing query: {e}", exc_info=True)
        conn.rollback()
        return False
    finally:
        cursor.close()
        release_connection(conn)

    return True


def fetch_query(query, params):
    try:
        conn = get_connection()
    except psycopg2.DatabaseError as error:
        logger.error("Failed to connect to the database", exc_info=True)
        sys.exit(1)

    try:
        cursor = conn.cursor()
        cursor.execute(query, params)
        result = cursor.fetchall()
    except Exception as error:
        error_message = f"Error executing query: {error}"
        logger.error(error_message, exc_info=True)
        conn.rollback()
        return None
    finally:
        cursor.close()
        release_connection(conn)

    return result
