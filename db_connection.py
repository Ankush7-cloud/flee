import duckdb

def get_connection():
    return duckdb.connect("device_data.duckdb")
