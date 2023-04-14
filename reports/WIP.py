from numpy import sum, where
# from pandas import pivot_table
# from utilities.queries import get_rows
from utilities.click_handlers import convert_df
from plotly.express import bar, pie
from datetime import datetime

def level_1_wip(st):
    try:
        fye = st.session_state['today'].year if st.session_state['today'].month < 6 else st.session_state['today'].year + 1
        wip_df = st.session_state['wip'].copy()
        from pandas import to_datetime
        wip_df['WIPDATE'] = to_datetime(wip_df['WIPDATE'], format='%Y-%m-%d')
        # st.write(wip_df)
        wip_df = wip_df[wip_df['STAFFINDEX'] == st.session_state['user']['STAFFINDEX'].iloc[0]]
        fy_wip_df = wip_df[(wip_df['WIPDATE'] >= datetime(fye - 1, 6, 1).strftime('%Y-%m-%d')) & (wip_df['WIPDATE'] < datetime(fye, 6, 1).strftime('%Y-%m-%d'))]
        fy_wip_df['MONTH'] = fy_wip_df['WIPDATE'].dt.month
        fye_wip_service_df = fy_wip_df[['WIPHOURS', 'SERVICETITLE', 'MONTH']].groupby(['MONTH', 'SERVICETITLE'], as_index=False).agg(WIP_HOURS=('WIPHOURS', 'sum')).reset_index()[['MONTH', 'SERVICETITLE', 'WIP_HOURS']]
        st.write(bar(fye_wip_service_df, x='MONTH', y='WIP_HOURS', color='SERVICETITLE', title='WIP Hours by Month and Service'))
        # cy_wip_df = wip_df
        # py_wip_df = wip_df
        # st.write(fy_wip_df)
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
        partner_table.write(filtered_df[['WIPOUTSTANDING', 'CLIENT_PARTNER', 'CLIENT', 'OFFICE']].groupby(['CLIENT_PARTNER', 'CLIENT', 'OFFICE'], as_index=False).agg(OUTSTANDING_WIP=('WIPOUTSTANDING', 'sum')).reset_index()[['CLIENT_PARTNER', 'CLIENT', 'OFFICE', 'OUTSTANDING_WIP']])
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

        aging_table.write(filtered_df[['WIPOUTSTANDING', 'CLIENT_PARTNER', 'CLIENT', 'OFFICE', 'AGING_PERIOD']].groupby(['CLIENT_PARTNER', 'CLIENT', 'OFFICE', 'AGING_PERIOD'], as_index=False).agg(OUTSTANDING_WIP=('WIPOUTSTANDING', 'sum')).reset_index()[['CLIENT_PARTNER', 'CLIENT', 'OFFICE', 'AGING_PERIOD', 'OUTSTANDING_WIP']])
        aging_table.download_button(
            label='Download this data',
            data=aging_csv,
            file_name='Aging WIP.csv',
            key='aging_table_download'
        )

    except Exception as e:
        st.write(e)