from streamlit import cache_data
from pandas import DataFrame
from math import ceil

@cache_data(ttl=3600)
def run_query(query, _conn, rows):
    iterations = rows / 10000
    finalList = list()
    for i in range(iterations):
        offset = i * 10000
        query += f' LIMIT 10000 OFFSET {offset}'
        with _conn.cursor() as cur:
            cur.execute(query)
            rows = cur.fetchall()
            columns = [column[0] for column in cur.description]
            results = list()
            for row in rows:
                results.append(dict(zip(columns, row)))
            
            finalList.append(results)
            
    return DataFrame(finalList)
    
def get_row_nums(table, _conn):
    with _conn.cursor() as cur:
        cur.execute(f"SELECT COUNT(*) FROM {table}")
        rows = cur.fetchall()
        return rows[0][0]