from streamlit import cache_resource
from pandas import DataFrame

@cache_resource(ttl=3600)
def run_query(query, _conn):
    try:
        with _conn.cursor() as cur:
            cur.execute(query)
            rows = cur.fetchall()
            columns = [column[0] for column in cur.description]
            results = list()
            for row in rows:
                results.append(dict(zip(columns, row)))
        return DataFrame(results)
    except Exception as e:
        return {'query': query, 'e': e}
