from streamlit import cache_data, cache_resource, session_state, secrets
from snowflake.connector import connect
from pandas import DataFrame
from rsa import decrypt, PrivateKey
from base64 import b64decode
from ast import literal_eval

@cache_resource(ttl=3600)
def init_connection():
    key = ['-----BEGIN RSA PRIVATE KEY-----', secrets['snowflake-encrypted']['secret'].replace(' ', '\n'),'-----END RSA PRIVATE KEY-----']
    conn_string = decrypt(b64decode(session_state['company']['CONNECTION'].iloc[0]), PrivateKey.load_pkcs1(bytes(''.join(key), 'utf-8')))
    return connect(    
        **literal_eval(conn_string.decode()), client_session_keep_alive=True
    )

def validation_company(domain):
    try:
        key = ['-----BEGIN RSA PRIVATE KEY-----', secrets['snowflake-encrypted']['secret'].replace(' ', '\n'),'-----END RSA PRIVATE KEY-----']
        conn_string = decrypt(b64decode(secrets['snowflake-encrypted']['conn_string']), PrivateKey.load_pkcs1(bytes(''.join(key), 'utf-8')))
        conn = connect(**literal_eval(conn_string.decode()))
    except Exception as e:
        return {'process': 'validation_company snowflake connection', 'error': e}

    try:
        with conn.cursor() as cur:
            cur.execute(f"SELECT * FROM COMPANIES WHERE DOMAIN = '{domain}'")
            rows = cur.fetchall()
            columns = [column[0] for column in cur.description]
        
        conn.close()

        return DataFrame.from_records(rows, columns=columns)
    except Exception as e:
        conn.close()
        return {'process': 'validation_company getting company data', 'error': e}
    
def get_new_data(query):
    update_timestamp = 1
    return get_rows(query, update_timestamp)

@cache_data(ttl=3600)
def get_rows(query, timestamp):

    if 'conn' in session_state:
        conn = session_state['conn']

    try:
        with conn.cursor() as cur:
            cur.execute(query)
            rows = cur.fetchall()
            columns = [column[0] for column in cur.description]
        return DataFrame.from_records(rows, columns=columns)
    except Exception as e:
        return {'query': query, 'e': e, 'query': query}
    
def insert_rows(schema, table, columns, values, json_val=0):
    from json import dumps
    try:
        sqlValues = str()
        for value in values:
            if type(value) == str:
                sqlValues += f"'{value}',"
            else:
                sqlValues += f"{value},"
        with session_state['conn'].cursor() as cur:
            if json_val == 0:
                cur.execute(f"INSERT INTO {schema}.{table}({columns}) SELECT {sqlValues[:-1]};")
            else:
                cur.execute(f'INSERT INTO {schema}.{table}({columns}) SELECT {sqlValues} PARSE_JSON($${dumps(json_val)}$$);')
        # return cur.sfqid
    except Exception as e:
        return {'e': e, 'query': f'INSERT INTO {schema}.{table}({columns}) SELECT {sqlValues} PARSE_JSON($${dumps(json_val)}$$);'}
    
def update_rows(schema, table, set_col, set_val, where_col, where_val):
    try:
        with session_state['conn'].cursor() as cur:
            cur.execute(f'UPDATE {schema}.{table} SET {set_col} = {set_val} WHERE {where_col} = {where_val};')
        # return cur.sfqid
    except Exception as e:
        return {'e': e, 'query': f'UPDATE {schema}.{table} SET {set_col} = {set_val} WHERE {where_col} = {where_val};'}