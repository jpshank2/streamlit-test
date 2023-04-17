from numpy import where
# from pandas import pivot_table
# from utilities.queries import get_rows
from utilities.click_handlers import convert_df
from plotly.express import bar, pie
from datetime import datetime

def level_1_wip(st):
    try:
        fym = 6
        fye = st.session_state['today'].year if st.session_state['today'].month < fym else st.session_state['today'].year + 1
        wip_df = st.session_state['wip'].copy()
        from pandas import to_datetime
        wip_df['WIPDATE'] = to_datetime(wip_df['WIPDATE'], format='%Y-%m-%d')
        wip_df = wip_df[wip_df['STAFFINDEX'] == st.session_state['user']['STAFFINDEX'].iloc[0]]
        

        fy_wip_df = wip_df[(wip_df['WIPDATE'] >= datetime(fye - 1, fym, 1).strftime('%Y-%m-%d')) & (wip_df['WIPDATE'] < datetime(fye, fym, 1).strftime('%Y-%m-%d')) & (wip_df['CONTINDEX'] < 900000)]
        
        fye_wip_service_df = fy_wip_df[['WIPHOURS', 'SERVICETITLE', 'MONTH']].groupby(['MONTH', 'SERVICETITLE'], as_index=False).agg(WIP_HOURS=('WIPHOURS', 'sum')).reset_index()[['MONTH', 'SERVICETITLE', 'WIP_HOURS']]

        wip_service_fig = bar(fye_wip_service_df, x='MONTH', y='WIP_HOURS', color='SERVICETITLE', title='WIP Hours by Month and Service').update_xaxes(categoryorder='array', categoryarray=['June', 'July', 'August', 'September', 'October', 'November', 'December', 'January', 'February', 'March', 'April', 'May'])
        st.plotly_chart(wip_service_fig, use_container_width=True)

        py_col, cy_col = st.columns(2)
        py_col.markdown('#### Prior Year Data')
        cy_col.markdown('#### Current Year Data')

        cy_wip_df = wip_df[(wip_df['WIPDATE'] >= datetime(st.session_state['today'].year - 1, st.session_state['today'].month, st.session_state['today'].day).strftime('%Y-%m-%d')) & (wip_df['WIPDATE'] < st.session_state['today'].strftime('%Y-%m-%d'))]
        
        cy_wip_service_df = cy_wip_df[cy_wip_df['CONTINDEX'] < 900000][['WIPHOURS', 'SERVICETITLE']].groupby(['SERVICETITLE'], as_index=False).agg(WIP_HOURS=('WIPHOURS', 'sum')).reset_index()[['SERVICETITLE', 'WIP_HOURS']]
        cy_wip_service_fig = pie(cy_wip_service_df, values='WIP_HOURS', names='SERVICETITLE', title='CY WIP Hours by Service Title')
        cy_col.plotly_chart(cy_wip_service_fig, use_container_width=True)

        py_wip_df = wip_df[(wip_df['WIPDATE'] >= datetime(st.session_state['today'].year - 2, st.session_state['today'].month, st.session_state['today'].day).strftime('%Y-%m-%d')) & (wip_df['WIPDATE'] < datetime(st.session_state['today'].year - 1, st.session_state['today'].month, st.session_state['today'].day).strftime('%Y-%m-%d'))]
        
        py_wip_service_df = py_wip_df[py_wip_df['CONTINDEX'] < 900000][['WIPHOURS', 'SERVICETITLE']].groupby(['SERVICETITLE'], as_index=False).agg(WIP_HOURS=('WIPHOURS', 'sum')).reset_index()[['SERVICETITLE', 'WIP_HOURS']]
        py_wip_service_fig = pie(py_wip_service_df, values='WIP_HOURS', names='SERVICETITLE', title='PY WIP Hours by Service Title')
        py_col.plotly_chart(py_wip_service_fig, use_container_width=True)

        cy_util_df = cy_wip_df[['STAFFINDEX', 'WIPHOURS', 'BILLABLEHOURS', 'NONBILLABLEHOURS']]
        cy_util_df = cy_util_df.groupby('STAFFINDEX').agg(TOTAL_HOURS=('WIPHOURS', 'sum'), BILLABLE_HOURS=('BILLABLEHOURS', 'sum'), NON_BILL_HOURS=('NONBILLABLEHOURS', 'sum')).reset_index()
        cy_util_df['UTILIZATION'] = round((cy_util_df['BILLABLE_HOURS'] / cy_util_df['TOTAL_HOURS']) * 100, 2)
        cy_util_df['UTILIZATION'] = cy_util_df['UTILIZATION'].astype(str)
        cy_util_df['UTILIZATION'] = cy_util_df['UTILIZATION'] + '%'

        cy_col.dataframe(cy_util_df[['TOTAL_HOURS', 'BILLABLE_HOURS', 'NON_BILL_HOURS', 'UTILIZATION']], use_container_width=True)

        py_util_df = py_wip_df[['STAFFINDEX', 'WIPHOURS', 'BILLABLEHOURS', 'NONBILLABLEHOURS']]
        py_util_df = py_util_df.groupby('STAFFINDEX').agg(TOTAL_HOURS=('WIPHOURS', 'sum'), BILLABLE_HOURS=('BILLABLEHOURS', 'sum'), NON_BILL_HOURS=('NONBILLABLEHOURS', 'sum')).reset_index()
        py_util_df['UTILIZATION'] = round((py_util_df['BILLABLE_HOURS'] / py_util_df['TOTAL_HOURS']) * 100, 2).astype(str) + '%'

        py_col.dataframe(py_util_df[['TOTAL_HOURS', 'BILLABLE_HOURS', 'NON_BILL_HOURS', 'UTILIZATION']], use_container_width=True)

        cy_real_df = cy_wip_df[['STAFFINDEX', 'BILLABLEHOURS', 'WIPBILLED', 'WIPAMOUNT']]
        cy_real_df = cy_real_df.groupby('STAFFINDEX').agg(BILLABLE_HOURS=('BILLABLEHOURS', 'sum'), WIP_BILLED=('WIPBILLED', 'sum'), WIP_AMOUNT=('WIPAMOUNT', 'sum')).reset_index()
        cy_real_df['REALIZATION'] = round((cy_real_df['WIP_BILLED'] / cy_real_df['WIP_AMOUNT']) * 100, 2).astype(str) + '%'
        cy_real_df['EFF_RATE'] = round((cy_real_df['WIP_BILLED'] / cy_real_df['BILLABLE_HOURS']), 2)

        cy_col.dataframe(cy_real_df[['WIP_AMOUNT', 'WIP_BILLED', 'REALIZATION', 'EFF_RATE']], use_container_width=True)

        py_real_df = py_wip_df[['STAFFINDEX', 'BILLABLEHOURS', 'WIPBILLED', 'WIPAMOUNT']]
        py_real_df = py_real_df.groupby('STAFFINDEX').agg(BILLABLE_HOURS=('BILLABLEHOURS', 'sum'), WIP_BILLED=('WIPBILLED', 'sum'), WIP_AMOUNT=('WIPAMOUNT', 'sum')).reset_index()
        py_real_df['REALIZATION'] = round((py_real_df['WIP_BILLED'] / py_real_df['WIP_AMOUNT']) * 100, 2).astype(str) + '%'
        py_real_df['EFF_RATE'] = round((py_real_df['WIP_BILLED'] / py_real_df['BILLABLE_HOURS']), 2)

        py_col.dataframe(py_real_df[['WIP_AMOUNT', 'WIP_BILLED', 'REALIZATION', 'EFF_RATE']], use_container_width=True)
        
        # cy_wip_df = wip_df
        # py_wip_df = wip_df
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
        wip_df = wip_df[(wip_df['CONTINDEX'] < 900000) & (wip_df['WIPOUTSTANDING'] != 0)]
        wip_df['WIPOUTSTANDING'] = wip_df['WIPOUTSTANDING'].round(2)
        wip_df['AGING_PERIOD'] = where(wip_df['AGING_PERIOD_SORT'] < 4, wip_df['OG_PERIOD'] + ' WIP', 'Overdue 90+ WIP')

        total_outstanding_wip = wip_df['WIPOUTSTANDING'].sum()

        static_one.metric(label='Target < $4M', value=total_outstanding_wip, delta=('Outstanding WIP' if total_outstanding_wip < 4000000 else '-Outstanding WIP'))

        partner_filter = filter_one.selectbox('Client Partner', ['All'] + [i for i in wip_df.CLIENT_PARTNER.unique()])
        office_filter = filter_two.selectbox('Client Office', ['All'] + [i for i in wip_df.OFFICE.unique()])

        if partner_filter == 'All' and office_filter == 'All':
            filtered_df = wip_df.copy()
            partner_df = filtered_df[['WIPOUTSTANDING', 'CLIENT_PARTNER']]
            partner_df = partner_df.groupby('CLIENT_PARTNER', as_index=False).agg(OUTSTANDING_WIP = ('WIPOUTSTANDING', 'sum')).reset_index()
            partner_y_val = 'CLIENT_PARTNER'
        elif partner_filter == 'All' and office_filter != 'All':
            filtered_df = wip_df[wip_df['OFFICE'] == office_filter].copy()
            partner_df = filtered_df[['WIPOUTSTANDING', 'CLIENT_PARTNER']]
            partner_df = partner_df.groupby('CLIENT_PARTNER', as_index=False).agg(OUTSTANDING_WIP = ('WIPOUTSTANDING', 'sum')).reset_index()
            partner_y_val = 'CLIENT_PARTNER'
        elif partner_filter != 'All' and office_filter == 'All':
            filtered_df = wip_df[wip_df['CLIENT_PARTNER'] == partner_filter].copy()
            partner_df = filtered_df[['WIPOUTSTANDING', 'OFFICE']]
            partner_df = partner_df.groupby('OFFICE', as_index=False).agg(OUTSTANDING_WIP = ('WIPOUTSTANDING', 'sum')).reset_index()
            partner_y_val = 'OFFICE'
        else:
            filtered_df = wip_df[(wip_df['CLIENT_PARTNER'] == partner_filter) & (wip_df['OFFICE'] == office_filter)]
            partner_df = filtered_df[['WIPOUTSTANDING', 'CLIENT']]
            partner_df = partner_df.groupby('CLIENT', as_index=False).agg(OUTSTANDING_WIP = ('WIPOUTSTANDING', 'sum')).reset_index()
            partner_y_val = 'CLIENT'

        partner_csv = convert_df(filtered_df[['WIPOUTSTANDING', 'CLIENT_PARTNER', 'CLIENT', 'OFFICE']].groupby(['CLIENT_PARTNER', 'CLIENT', 'OFFICE'], as_index=False).agg(OUTSTANDING_WIP=('WIPOUTSTANDING', 'sum')).reset_index())

        partner_visual.write(bar(partner_df, x='OUTSTANDING_WIP', y=partner_y_val, orientation='h', barmode='group', title='Firm WIP by Client Partner', text='OUTSTANDING_WIP'))
        partner_visual.download_button(
            label='Download this data',
            data=partner_csv,
            file_name='Outstanding WIP by Client Partner.csv',
            key='partner_visual_download'
        )
        partner_table.dataframe(filtered_df[['WIPOUTSTANDING', 'CLIENT_PARTNER', 'CLIENT', 'OFFICE']].groupby(['CLIENT_PARTNER', 'CLIENT', 'OFFICE'], as_index=False).agg(OUTSTANDING_WIP=('WIPOUTSTANDING', 'sum')).reset_index()[['CLIENT_PARTNER', 'CLIENT', 'OFFICE', 'OUTSTANDING_WIP']])
        partner_table.download_button(
            label='Download this data',
            data=partner_csv,
            file_name='Outstanding WIP by Client Partner.csv',
            key='partner_table_download'
        )

        aging_wip = filtered_df[['AGING_PERIOD', 'WIPOUTSTANDING']]
        aging_wip = aging_wip.groupby('AGING_PERIOD', as_index=False).agg(OUTSTANDING_WIP=('WIPOUTSTANDING', 'sum')).reset_index()

        aging_csv = convert_df(filtered_df[['WIPOUTSTANDING', 'CLIENT_PARTNER', 'CLIENT', 'OFFICE', 'AGING_PERIOD']].groupby(['CLIENT_PARTNER', 'CLIENT', 'OFFICE', 'AGING_PERIOD'], as_index=False).agg(OUTSTANDING_WIP=('WIPOUTSTANDING', 'sum')).reset_index()[['CLIENT_PARTNER', 'CLIENT', 'OFFICE', 'AGING_PERIOD', 'OUTSTANDING_WIP']])

        aging_visual.write(pie(aging_wip, values='OUTSTANDING_WIP', names='AGING_PERIOD', title='WIP Aging Periods'))
        aging_visual.download_button(
            label='Download this data',
            data=aging_csv,
            file_name='Aging WIP.csv',
            key='aging_visual_download'
        )

        aging_table.dataframe(filtered_df[['WIPOUTSTANDING', 'CLIENT_PARTNER', 'CLIENT', 'OFFICE', 'AGING_PERIOD']].groupby(['CLIENT_PARTNER', 'CLIENT', 'OFFICE', 'AGING_PERIOD'], as_index=False).agg(OUTSTANDING_WIP=('WIPOUTSTANDING', 'sum')).reset_index()[['CLIENT_PARTNER', 'CLIENT', 'OFFICE', 'AGING_PERIOD', 'OUTSTANDING_WIP']])
        aging_table.download_button(
            label='Download this data',
            data=aging_csv,
            file_name='Aging WIP.csv',
            key='aging_table_download'
        )

    except Exception as e:
        st.write(e)