import streamlit as st
import numpy as np
import pandas as pd
import plotly.express as px

@st.cache_data(ttl=3600)
def run_query(query, conn):
    with conn.cursor() as cur:
        cur.execute(query)
        rows = cur.fetchall()
        columns = [column[0] for column in cur.description]
        results = list()
        for row in rows:
            results.append(dict(zip(columns, row)))
        
        return pd.DataFrame(results)

def create_ar_reports(st, conn):
    try:
        rows = run_query("""SELECT AR.*, C.*, D.AGING_PERIOD_SORT, D.AGING_PERIOD as OG_PERIOD 
            from TRANS_AR AR 
                INNER JOIN DIM_CLIENT_MASTER C ON C.ContIndex = AR.ContIndex 
                INNER JOIN DIM_DATES D ON D.CALENDAR_DATE = AR.DEBTTRANDATE 
            WHERE DEBTTRANUNPAID <> 0;""", conn)

        office_office_AR = rows[['OFFICE', 'DEBTTRANUNPAID']]
        office_office_AR = office_office_AR.groupby('OFFICE', as_index=False).agg(OUTSTANDING_AR = ('DEBTTRANUNPAID', 'sum')).reset_index()

        levels = [
            st.selectbox('Office', ['All'] + [i for i in office_office_AR.OFFICE.unique()])
        ]


        if levels[0] == 'All':
            office_AR_DF = office_office_AR
            yVal = 'OFFICE'
            title = 'AR by Office w/ drilldown'
        else:
            office_partner_AR = rows[rows['OFFICE'] == levels[0]]
            office_partner_AR = office_partner_AR[['CLIENTPARTNER', 'DEBTTRANUNPAID']]
            levels.append(st.selectbox('Client Partner', ['All'] + [i for i in office_partner_AR.CLIENTPARTNER.unique()]))

            office_AR_DF = office_partner_AR.groupby('CLIENTPARTNER', as_index=False).agg(OUTSTANDING_AR = ('DEBTTRANUNPAID', 'sum')).reset_index()
            yVal = 'CLIENTPARTNER'
            title = levels[0] + ' AR by Client Partner w/ drilldown'

            if levels[1] != 'All':
                office_AR_DF = rows[(rows['OFFICE'] == levels[0]) & (rows['CLIENTPARTNER'] == levels[1])]
                office_AR_DF = office_AR_DF[['CLIENT', 'DEBTTRANUNPAID']]
                office_AR_DF = office_AR_DF.groupby('CLIENT', as_index=False).agg(OUTSTANDING_AR = ('DEBTTRANUNPAID', 'sum')).reset_index()
                yVal = 'CLIENT'
                title = f'{levels[1]}\'s {levels[0]} AR by Client w/ drilldown'
                
        st.write(px.bar(office_AR_DF, x='OUTSTANDING_AR', y=yVal, orientation='h', barmode='group', title=title, text='OUTSTANDING_AR'))

        partner_AR = rows[['CLIENTPARTNER', 'DEBTTRANUNPAID']].copy()
        partner_AR = partner_AR.groupby('CLIENTPARTNER', as_index=False).agg(OUTSTANDING_AR=('DEBTTRANUNPAID', 'sum')).reset_index()

        st.write(px.bar(partner_AR, y='CLIENTPARTNER', x='OUTSTANDING_AR', orientation='h', title='AR by Client Partner'))

        aging_AR = rows[['AGING_PERIOD_SORT', 'OG_PERIOD', 'DEBTTRANUNPAID']].copy()
        aging_AR['AGING_PERIOD'] = np.where(aging_AR['AGING_PERIOD_SORT'] < 4, aging_AR['OG_PERIOD'] + ' AR', 'Overdue 90+ AR')
        aging_AR = aging_AR[['AGING_PERIOD', 'DEBTTRANUNPAID']]
        aging_AR = aging_AR.groupby('AGING_PERIOD', as_index=False).agg(OUTSTANDING_AR=('DEBTTRANUNPAID', 'sum')).reset_index()
        st.write(px.pie(aging_AR, values='OUTSTANDING_AR', names='AGING_PERIOD', title='AR Aging Periods'))
        
    except Exception as e:
        print(st.write(e))
