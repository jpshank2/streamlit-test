from streamlit import cache_data
from pandas import DataFrame

@cache_data(ttl=3600)
def run_query(query, _conn):
    try:
        with _conn.cursor() as cur:
            rows = cur.execute(query)
            # rows = cur.fetchall()
            columns = [column[0] for column in cur.description]
            # results = list()
            # for row in rows:
            #     results.append(dict(zip(columns, row)))
        return DataFrame.from_records(iter(rows), columns=columns)
    except Exception as e:
        return {'query': query, 'e': e}
