from streamlit import cache_data, session_state
from pandas import DataFrame

@cache_data(ttl=3600)
def get_rows(query):
    try:
        with session_state['conn'].cursor() as cur:
            cur.execute(query)
            rows = cur.fetchall()
            columns = [column[0] for column in cur.description]
        return DataFrame.from_records(rows, columns=columns)
    except Exception as e:
        return {'query': query, 'e': e, 'data': rows}
    
def insert_rows(schema, table, values):
    try:
        values = ','.join(values)
        with session_state['conn'].cursor() as cur:
            cur.execute(f'INSERT INTO {schema}.{table} VALUES ({values[:-1]});')
        return cur.sfqid
    except Exception as e:
        return {'e': e}