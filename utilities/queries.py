from streamlit import cache_data
from pandas import DataFrame
from math import ceil

@cache_data(ttl=3600)
def run_query(query, _conn, rows):
    try:
        # iterations = ceil(rows / 10000)
        # finalList = list()
        # for i in range(iterations):
        #     offset = i * 10000
        #     iter_query = query + f'\nLIMIT 100000 OFFSET {offset};'
        with _conn.cursor() as cur:
            cur.execute(query)
            rows = cur.fetchall()
            columns = [column[0] for column in cur.description]
            results = list()
            for row in rows:
                results.append(dict(zip(columns, row)))
                
                # finalList += results
        return DataFrame(results)
    except Exception as e:
        iter_query = query + f'\nLIMIT 10000 OFFSET 0;'
        return {'query': iter_query, 'e': e}
    
def get_row_nums(table, _conn):
    with _conn.cursor() as cur:
        cur.execute(f"SELECT COUNT(*) FROM {table}")
        rows = cur.fetchall()
        return rows[0][0]