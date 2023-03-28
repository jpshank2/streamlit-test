from streamlit import cache_data, cache_resource, session_state, secrets, write
from snowflake.connector import connect
from pandas import DataFrame

@cache_resource(ttl=3600)
def init_connection():
    write(__file__)
    return connect(
        **secrets["snowflake"], client_session_keep_alive=True
    )


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
    
def insert_rows(schema, table, columns, values, json_val):
    from json import dumps
    try:
        sqlValues = str()
        for value in values:
            if type(value) == str:
                sqlValues += f"'{value}',"
            else:
                sqlValues += f"{value},"
        with session_state['conn'].cursor() as cur:
            cur.execute(f'INSERT INTO {schema}.{table}({columns}) SELECT {sqlValues} PARSE_JSON($${dumps(json_val)}$$);')
        return cur.sfqid
    except Exception as e:
        return {'e': e, 'query': f'INSERT INTO {schema}.{table}({columns}) SELECT {sqlValues} PARSE_JSON($${dumps(json_val)}$$);'}