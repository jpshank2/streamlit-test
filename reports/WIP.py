from numpy import sum
from pandas import pivot_table
from utilities.queries import get_rows
from plotly.express import bar, pie

def create_wip_reports(st):
    try:
        # rowNums = q.get_row_nums('TRANS_WIP', conn)
        # st.write(rowNums)
        rows = get_rows("""SELECT WIP.WIPOUTSTANDING, C.CLIENT_PARTNER, C.CLIENT, C.OFFICE, D.AGING_PERIOD_SORT, D.AGING_PERIOD as OG_PERIOD 
            from TRANS_WIP WIP
                INNER JOIN DIM_CLIENT_MASTER C ON C.ContIndex = WIP.ContIndex 
                INNER JOIN DIM_DATES D ON D.CALENDAR_DATE = WIP.WIPDATE
            WHERE WIP.ContIndex < 900000
                AND WIP.WIPOUTSTANDING <> 0""").copy()
        
        outstanding_WIP = round(rows['WIPOUTSTANDING'].sum(), 2)
        
        st.markdown(f'Outstanding WIP is {outstanding_WIP}')
        
        st.write(pivot_table(rows, index=['CLIENT_PARTNER', 'CLIENT'], values=['WIPOUTSTANDING'], aggfunc=sum))

        # office_office_AR = rows[['OFFICE', 'DEBTTRANUNPAID']]
        # office_office_AR = office_office_AR.groupby('OFFICE', as_index=False).agg(OUTSTANDING_AR = ('DEBTTRANUNPAID', 'sum')).reset_index()

        # levels = [
        #     st.selectbox('Office', ['All'] + [i for i in office_office_AR.OFFICE.unique()])
        # ]


        # if levels[0] == 'All':
        #     office_AR_DF = office_office_AR
        #     yVal = 'OFFICE'
        #     title = 'AR by Office w/ drilldown'
        # else:
        #     office_partner_AR = rows[rows['OFFICE'] == levels[0]]
        #     office_partner_AR = office_partner_AR[['CLIENTPARTNER', 'DEBTTRANUNPAID']]
        #     levels.append(st.selectbox('Client Partner', ['All'] + [i for i in office_partner_AR.CLIENTPARTNER.unique()]))

        #     office_AR_DF = office_partner_AR.groupby('CLIENTPARTNER', as_index=False).agg(OUTSTANDING_AR = ('DEBTTRANUNPAID', 'sum')).reset_index()
        #     yVal = 'CLIENTPARTNER'
        #     title = levels[0] + ' AR by Client Partner w/ drilldown'

        #     if levels[1] != 'All':
        #         office_AR_DF = rows[(rows['OFFICE'] == levels[0]) & (rows['CLIENTPARTNER'] == levels[1])]
        #         office_AR_DF = office_AR_DF[['CLIENT', 'DEBTTRANUNPAID']]
        #         office_AR_DF = office_AR_DF.groupby('CLIENT', as_index=False).agg(OUTSTANDING_AR = ('DEBTTRANUNPAID', 'sum')).reset_index()
        #         yVal = 'CLIENT'
        #         title = f'{levels[1]}\'s {levels[0]} AR by Client w/ drilldown'
                
        # st.write(px.bar(office_AR_DF, x='OUTSTANDING_AR', y=yVal, orientation='h', barmode='group', title=title, text='OUTSTANDING_AR'))

        # partner_AR = rows[['CLIENTPARTNER', 'DEBTTRANUNPAID']].copy()
        # partner_AR = partner_AR.groupby('CLIENTPARTNER', as_index=False).agg(OUTSTANDING_AR=('DEBTTRANUNPAID', 'sum')).reset_index()

        # st.write(px.bar(partner_AR, y='CLIENTPARTNER', x='OUTSTANDING_AR', orientation='h', title='AR by Client Partner'))

        # aging_AR = rows[['AGING_PERIOD_SORT', 'OG_PERIOD', 'DEBTTRANUNPAID']].copy()
        # aging_AR['AGING_PERIOD'] = np.where(aging_AR['AGING_PERIOD_SORT'] < 4, aging_AR['OG_PERIOD'] + ' AR', 'Overdue 90+ AR')
        # aging_AR = aging_AR[['AGING_PERIOD', 'DEBTTRANUNPAID']]
        # aging_AR = aging_AR.groupby('AGING_PERIOD', as_index=False).agg(OUTSTANDING_AR=('DEBTTRANUNPAID', 'sum')).reset_index()
        # st.write(px.pie(aging_AR, values='OUTSTANDING_AR', names='AGING_PERIOD', title='AR Aging Periods'))
        
    except Exception as e:
        st.write(e)

def level_4_wip(st):
    try:
        static_one, static_two, static_three, static_four, static_five = st.columns(5)
        filter_one, filter_two = st.columns(2)
        visuals_one, visuals_two = st.columns(2)
        partner_visual, partner_table = visuals_one.tabs(['Visual', 'Table'])
        current_visual, current_table = visuals_one.tabs(['Visual', 'Table'])
        office_visual, office_table = visuals_two.tabs(['Visual', 'Table'])
        aging_visual, aging_table = visuals_two.tabs(['Visual', 'Table'])
        dynamic_one, dynamic_two, dynamic_three, dynamic_four, dynamic_five = st.columns(5)

        wip_df = st.session_state['wip'].copy()

        partner_filter = filter_one.selectbox('Client Partner', ['All'] + [i for i in wip_df.CLIENT_PARTNER.unique()])
        office_filter = filter_two.selectbox('Client Office', ['All'] + [i for i in wip_df.OFFICE.unique()])

        if partner_filter == 'All' and office_filter == 'All':
            filtered_df = wip_df.copy()
            partner_df = filtered_df[['WIPOUTSTANDING', 'CLIENT_PARTNER']]
            partner_df = filtered_df.groupby('CLIENT_PARTNER', as_index=False).agg(OUTSTANDING_WIP = ('WIPOUTSTANDING', 'sum')).reset_index()
            yVal = 'Client Partner'
        elif partner_filter == 'All' and office_filter != 'All':
            filtered_df = wip_df[wip_df['OFFICE'] == office_filter].copy()
            partner_df = filtered_df[['WIPOUTSTANDING', 'CLIENT_PARTNER']]
            partner_df = filtered_df.groupby('CLIENT_PARTNER', as_index=False).agg(OUTSTANDING_WIP = ('WIPOUTSTANDING', 'sum')).reset_index()
            yVal = 'Client Partner'
        elif partner_filter != 'All' and office_filter == 'All':
            filtered_df = wip_df[wip_df['CLIENT_PARTNER'] == partner_filter].copy()
            partner_df = filtered_df[['WIPOUTSTANDING', 'OFFICE']]
            partner_df = filtered_df.groupby('OFFICE', as_index=False).agg(OUTSTANDING_WIP = ('WIPOUTSTANDING', 'sum')).reset_index()
            yVal = 'Client Office'
        else:
            filtered_df = wip_df[(wip_df['CLIENT_PARTNER'] == partner_filter) & (wip_df['OFFICE'] == office_filter)]
            partner_df = filtered_df[['WIPOUTSTANDING', 'OFFICE']]
            partner_df = filtered_df.groupby('OFFICE', as_index=False).agg(OUTSTANDING_WIP = ('WIPOUTSTANDING', 'sum')).reset_index()
            yVal = 'Client Office'

        partner_df = filtered_df[['WIPOUTSTANDING', 'CLIENT_PARTNER']]
        partner_df = filtered_df.groupby('CLIENT_PARTNER', as_index=False).agg(OUTSTANDING_WIP = ('WIPOUTSTANDING', 'sum')).reset_index()
        partner_visual.write(bar(partner_df, x='OUTSTANDING_WIP', y=yVal, orientation='h', barmode='group', title='Firm WIP by Client Partner', text='OUTSTANDING_WIP'))
        partner_table.write(filtered_df[['WIPOUTSTANDING', 'CLIENT_PARTNER', 'CLIENT', 'OFFICE']])

    except Exception as e:
        st.write(e)