import streamlit as st
import numpy as np
import pandas as pd
import snowflake.connector
import plotly.express as px

st.write("# Hello, AR! :wave:")

@st.cache_resource
def init_connection():
    return snowflake.connector.connect(
        **st.secrets["snowflake"], client_session_keep_alive=True
    )

conn = init_connection()

@st.cache_data(ttl=3600)
def run_query(query):
    with conn.cursor() as cur:
        cur.execute(query)
        rows = cur.fetchall()
        columns = [column[0] for column in cur.description]
        results = list()
        for row in rows:
            results.append(dict(zip(columns, row)))
        
        return pd.DataFrame(results)

try:
    rows = run_query("""SELECT AR.*, C.*, D.AGING_PERIOD_SORT, D.AGING_PERIOD as OG_PERIOD 
        from TRANS_AR AR 
            INNER JOIN DIM_CLIENT_MASTER C ON C.ContIndex = AR.ContIndex 
            INNER JOIN DIM_DATES D ON D.CALENDAR_DATE = AR.DEBTTRANDATE 
        WHERE DEBTTRANUNPAID <> 0;""")

    # Print resultant columns.
    st.write(rows.columns)

    office_AR = rows[['OFFICE', 'DEBTTRANUNPAID', 'CLIENTPARTNER', 'CLIENT']].copy()
    officeIndex = pd.MultiIndex.from_frame(rows[['OFFICE', 'CLIENTPARTNER', 'CLIENT']])
    office_AR.index = officeIndex
    office_AR.index.set_names(['OFFICE', 'CLIENTPARTNER', 'CLIENT'], inplace=True)
    # office_AR = office_AR.groupby('OFFICE', as_index=False).agg(OUTSTANDING_AR=('DEBTTRANUNPAID', 'sum')).reset_index()
    levels = [
        st.selectbox('Level 1', ['All'] + [i for i in office_AR.index.get_level_values(0).unique()]),
        st.selectbox('Level 2', ['All'] + [i for i in office_AR.index.get_level_values(1).unique()]),
        st.selectbox('Level 3', ['All'] + [i for i in office_AR.index.get_level_values(2).unique()])
    ]
    for idx, level in enumerate(levels):
        if level == 'All':
            levels[idx] = slice(None)

    # Make a cross section with the level values and pass in the index names.

    st.dataframe(
        office_AR.xs(
            (levels[0], levels[1], levels[2]),
            level=['OFFICE', 'CLIENTPARTNER', 'CLIENT']
        )
    )

    st.bar_chart(office_AR, x='OFFICE', y='OUTSTANDING_AR')

    partner_AR = rows[['CLIENTPARTNER', 'DEBTTRANUNPAID']].copy()
    partner_AR = partner_AR.groupby('CLIENTPARTNER', as_index=False).agg(OUTSTANDING_AR=('DEBTTRANUNPAID', 'sum')).reset_index()
    # partner_AR = partner_AR[partner_AR['OUTSTANDING_AR'] != 0]
    # st.bar_chart(partner_AR, x='CLIENTPARTNER', y='OUTSTANDING_AR')
    st.write(px.bar(partner_AR, y='CLIENTPARTNER', x='OUTSTANDING_AR', orientation='h'))

    aging_AR = rows[['AGING_PERIOD_SORT', 'OG_PERIOD', 'DEBTTRANUNPAID']].copy()
    aging_AR['AGING_PERIOD'] = np.where(aging_AR['AGING_PERIOD_SORT'] < 4, aging_AR['OG_PERIOD'] + ' AR', 'Overdue 90+ AR')
    aging_AR = aging_AR[['AGING_PERIOD', 'DEBTTRANUNPAID']]
    aging_AR = aging_AR.groupby('AGING_PERIOD', as_index=False).agg(OUTSTANDING_AR=('DEBTTRANUNPAID', 'sum')).reset_index()
    st.write(px.pie(aging_AR, values='OUTSTANDING_AR', names='AGING_PERIOD'))
    st.write(aging_AR)


    # First, let's set up the multi index with 2 levels:
    # city and store. We will create an empty frame with some
    # column data (fruits) and pass in the multi index as index.
    # Index names are set for accessing later

    # multi_index = pd.MultiIndex.from_product([
    #     ['city_1', 'city_2'],
    #     ['store_1', 'store_2', 'store_3'],
    # ])
    # df = pd.DataFrame(columns=['apples', 'oranges'], index=multi_index)
    # df.index.set_names(['city', 'store'], inplace=True)

    # Now let's make some selectboxes for drilling up/down

    # levels = [
    #     st.selectbox('Level 1', ['All'] + [i for i in df.index.get_level_values(0).unique()]),
    #     st.selectbox('Level 2', ['All'] + [i for i in df.index.get_level_values(1).unique()])
    # ]

    # We need to use slice(None) if the user selects 'All'.
    # The specified level with 'All' will take all values in that level.

    # for idx, level in enumerate(levels):
    #     if level == 'All':
    #         levels[idx] = slice(None)

    # # Make a cross section with the level values and pass in the index names.

    # st.dataframe(
    #     df.xs(
    #         (levels[0], levels[1]),
    #         level=['city', 'store']
    #     )
    # )
except Exception as e:
    print(st.write(e))
