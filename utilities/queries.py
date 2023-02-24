from streamlit import cache_data
from pandas import DataFrame

@cache_data(ttl=3600)
def run_query(query, _conn):
    with _conn.cursor() as cur:
        cur.execute(query)
        rows = cur.fetchall()
        columns = [column[0] for column in cur.description]
        results = list()
        for row in rows:
            results.append(dict(zip(columns, row)))
        
        return DataFrame(results)
    
def get_row_nums(table, _conn):
    with _conn.cursor() as cur:
        cur.execute(f"SELECT COUNT(*) FROM {table}")
        rows = cur.fetchall()
        return rows[0][0]