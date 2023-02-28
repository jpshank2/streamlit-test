from streamlit import cache_resource
from pandas import DataFrame
from math import ceil

@cache_resource(ttl=3600)
# this puts the query into a dataframe that can be displayed 
def run_query(query, _conn):
    try:
        # iterations = ceil(rows / 10000)
        # finalList = list()
        # for i in range(iterations):
        #     offset = i * 10000
        #     iter_query = query + f'\nLIMIT 100000 OFFSET {offset};'
        with _conn.cursor() as cur:
            cur.execute(query)
            rows = cur.fetchall()
            #This allows the column headers to be displayed by the cur.description
            columns = [column[0] for column in cur.description]
            results = list()
            for row in rows:
                
                #the zip function will combine them up together
                results.append(dict(zip(columns, row)))
                
                # finalList += results
        #You then return the results into a dataframe        
        return DataFrame(results)
    except Exception as e:
        iter_query = query + f'\nLIMIT 10000 OFFSET 0;'
        return {'query': iter_query, 'e': e}
    
def get_row_nums(table, _conn):
    with _conn.cursor() as cur:
        cur.execute(f"SELECT COUNT(*) FROM {table}")
        rows = cur.fetchall()
        return rows[0][0]

#Need to figure out if I need the table passed into the function
def get_services(table, _conn):
    with _conn.cursor() as cur:
        cur.execute(f"SELECT services FROM tblServices") #Double check query in Snowflake
        rows = cur.fetchall()
        return rows[0][0]