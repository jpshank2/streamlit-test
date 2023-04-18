from numpy import where
# from pandas import pivot_table
# from utilities.queries import get_rows
from utilities.click_handlers import convert_df
from plotly.express import bar, pie
from datetime import datetime

h_bar_style = {'xaxis_title_font_size': 18, 'yaxis_title_font_size': 18, 'xaxis_tickfont_size': 18, 'title_font_size': 24, 'font_size': 18} # yaxis_tickfont_size needs to be set on each graph

v_bar_style = {'legend_font_size': 18, 'title_font_size': 24, 'yaxis_tickfont_size': 18, 'xaxis_tickfont_size': 18}

pie_style = {'legend_font_size': 18, 'title_font_size': 24, 'font_size': 18}

def level_1_wip(st):
    try:
        fym = 5
        fye = st.session_state['today'].year if st.session_state['today'].month < fym else st.session_state['today'].year + 1
        wip_df = st.session_state['wip'].copy()
        benchmark_df = st.session_state['wip'][['STAFFINDEX', 'LEVEL', 'BILLABLEHOURS', 'WIPHOURS', 'WIPDATE', 'WIPBILLED', 'WIPAMOUNT']].copy()
        benchmark_df = benchmark_df[benchmark_df['LEVEL'] == st.session_state['user']['LEVEL'].iloc[0]]
        
        from pandas import to_datetime
        wip_df['WIPDATE'] = to_datetime(wip_df['WIPDATE'], format='%Y-%m-%d')
        benchmark_df['WIPDATE'] = to_datetime(benchmark_df['WIPDATE'], format='%Y-%m-%d')

        cy_benchmark_df = benchmark_df[(benchmark_df['WIPDATE'] >= datetime(st.session_state['today'].year - 1, st.session_state['today'].month, st.session_state['today'].day).strftime('%Y-%m-%d')) & (benchmark_df['WIPDATE'] < st.session_state['today'].strftime('%Y-%m-%d'))][['STAFFINDEX', 'BILLABLEHOURS', 'WIPHOURS', 'WIPBILLED', 'WIPAMOUNT']]
        cy_benchmark_df = cy_benchmark_df.groupby('STAFFINDEX').agg(BILLABLE_HOURS=('BILLABLEHOURS', 'sum'), TOTAL_HOURS=('WIPHOURS', 'sum'), WIP_BILLED=('WIPBILLED', 'sum'), WIP_AMOUNT=('WIPAMOUNT', 'sum'))
        cy_benchmark_df['UTILIZATION'] = round((cy_benchmark_df['BILLABLE_HOURS'] / cy_benchmark_df['TOTAL_HOURS']) * 100, 2)
        cy_benchmark_df['REALIZATION'] = round((cy_benchmark_df['WIP_BILLED'] / cy_benchmark_df['WIP_AMOUNT']) * 100, 2)
        cy_benchmark_df['EFF_RATE'] = round((cy_benchmark_df['WIP_BILLED'] / cy_benchmark_df['BILLABLE_HOURS']), 2)

        cy_benchmark_util = cy_benchmark_df['UTILIZATION'].mean()
        cy_benchmark_real = cy_benchmark_df['REALIZATION'].mean()
        cy_benchmark_eff = cy_benchmark_df['EFF_RATE'].mean()

        cy_benchmark_df = None

        py_benchmark_df = benchmark_df[(benchmark_df['WIPDATE'] >= datetime(st.session_state['today'].year - 2, st.session_state['today'].month, st.session_state['today'].day).strftime('%Y-%m-%d')) & (benchmark_df['WIPDATE'] < datetime(st.session_state['today'].year - 1, st.session_state['today'].month, st.session_state['today'].day).strftime('%Y-%m-%d'))][['STAFFINDEX', 'BILLABLEHOURS', 'WIPHOURS', 'WIPBILLED', 'WIPAMOUNT']]
        py_benchmark_df = py_benchmark_df.groupby('STAFFINDEX').agg(BILLABLE_HOURS=('BILLABLEHOURS', 'sum'), TOTAL_HOURS=('WIPHOURS', 'sum'), WIP_BILLED=('WIPBILLED', 'sum'), WIP_AMOUNT=('WIPAMOUNT', 'sum'))
        py_benchmark_df['UTILIZATION'] = round((py_benchmark_df['BILLABLE_HOURS'] / py_benchmark_df['TOTAL_HOURS']) * 100, 2)
        py_benchmark_df['REALIZATION'] = round((py_benchmark_df['WIP_BILLED'] / py_benchmark_df['WIP_AMOUNT']) * 100, 2)
        py_benchmark_df['EFF_RATE'] = round((py_benchmark_df['WIP_BILLED'] / py_benchmark_df['BILLABLE_HOURS']), 2)

        py_benchmark_util = py_benchmark_df['UTILIZATION'].mean()
        py_benchmark_real = py_benchmark_df['REALIZATION'].mean()
        py_benchmark_eff = py_benchmark_df['EFF_RATE'].mean()

        py_benchmark_df = None
        benchmark_df = None

        wip_df = wip_df[wip_df['STAFFINDEX'] == st.session_state['user']['STAFFINDEX'].iloc[0]]
        

        fy_wip_df = wip_df[(wip_df['WIPDATE'] >= datetime(fye - 1, fym, 1).strftime('%Y-%m-%d')) & (wip_df['WIPDATE'] < datetime(fye, fym, 1).strftime('%Y-%m-%d')) & (wip_df['CONTINDEX'] < 900000)]
        
        fye_wip_service_df = fy_wip_df[['WIPHOURS', 'SERVICETITLE', 'MONTH']].groupby(['MONTH', 'SERVICETITLE'], as_index=False).agg(WIP_HOURS=('WIPHOURS', 'sum')).reset_index()[['MONTH', 'SERVICETITLE', 'WIP_HOURS']]

        fy_wip_service_colors = st.session_state['color_map'][st.session_state['color_map']['SERVICE'].isin(fye_wip_service_df['SERVICETITLE'].tolist())].set_index('SERVICE')['COLOR'].to_dict()

        wip_service_fig = bar(fye_wip_service_df, x='MONTH', y='WIP_HOURS', color='SERVICETITLE', title='WIP Hours by Month and Service', color_discrete_map=fy_wip_service_colors).update_xaxes(categoryorder='array', categoryarray=['May', 'June', 'July', 'August', 'September', 'October', 'November', 'December', 'January', 'February', 'March', 'April']).update_layout(v_bar_style)
        st.plotly_chart(wip_service_fig, use_container_width=True)

        py_col, cy_col = st.columns(2, gap='medium')
        py_col.markdown('#### Prior Year Data')
        cy_col.markdown('#### Current Year Data')

        cy_wip_df = wip_df[(wip_df['WIPDATE'] >= datetime(st.session_state['today'].year - 1, st.session_state['today'].month, st.session_state['today'].day).strftime('%Y-%m-%d')) & (wip_df['WIPDATE'] < st.session_state['today'].strftime('%Y-%m-%d'))]
        
        cy_wip_service_df = cy_wip_df[cy_wip_df['CONTINDEX'] < 900000][['WIPHOURS', 'SERVICETITLE']].groupby(['SERVICETITLE'], as_index=False).agg(WIP_HOURS=('WIPHOURS', 'sum')).reset_index()[['SERVICETITLE', 'WIP_HOURS']]
        cy_wip_service_colors = st.session_state['color_map'][st.session_state['color_map']['SERVICE'].isin(cy_wip_service_df['SERVICETITLE'].tolist())].set_index('SERVICE')['COLOR'].to_dict()
        cy_wip_service_fig = pie(cy_wip_service_df, values='WIP_HOURS', names='SERVICETITLE', title='CY WIP Hours by Service Title', color_discrete_map=cy_wip_service_colors, color='SERVICETITLE').update_layout(pie_style)
        cy_col.plotly_chart(cy_wip_service_fig, use_container_width=True)

        py_wip_df = wip_df[(wip_df['WIPDATE'] >= datetime(st.session_state['today'].year - 2, st.session_state['today'].month, st.session_state['today'].day).strftime('%Y-%m-%d')) & (wip_df['WIPDATE'] < datetime(st.session_state['today'].year - 1, st.session_state['today'].month, st.session_state['today'].day).strftime('%Y-%m-%d'))]
        
        py_wip_service_df = py_wip_df[py_wip_df['CONTINDEX'] < 900000][['WIPHOURS', 'SERVICETITLE']].groupby(['SERVICETITLE'], as_index=False).agg(WIP_HOURS=('WIPHOURS', 'sum')).reset_index()[['SERVICETITLE', 'WIP_HOURS']]
        py_wip_service_colors = st.session_state['color_map'][st.session_state['color_map']['SERVICE'].isin(py_wip_service_df['SERVICETITLE'].tolist())].set_index('SERVICE')['COLOR'].to_dict()
        py_wip_service_fig = pie(py_wip_service_df, values='WIP_HOURS', names='SERVICETITLE', title='PY WIP Hours by Service Title', color_discrete_map=py_wip_service_colors, color='SERVICETITLE').update_layout(pie_style)
        py_col.plotly_chart(py_wip_service_fig, use_container_width=True)

        cy_util_df = cy_wip_df[['STAFFINDEX', 'WIPHOURS', 'BILLABLEHOURS', 'NONBILLABLEHOURS']]
        cy_util_df = cy_util_df.groupby('STAFFINDEX').agg(TOTAL_HOURS=('WIPHOURS', 'sum'), BILLABLE_HOURS=('BILLABLEHOURS', 'sum'), NON_BILL_HOURS=('NONBILLABLEHOURS', 'sum')).reset_index()
        cy_util_df['UTILIZATION'] = round((cy_util_df['BILLABLE_HOURS'] / cy_util_df['TOTAL_HOURS']) * 100, 2).astype(str) + '%'

        cy_col.markdown('##### Current Year Hours and Utilization')
        cy_col.dataframe(cy_util_df[['TOTAL_HOURS', 'BILLABLE_HOURS', 'NON_BILL_HOURS', 'UTILIZATION']], use_container_width=True)

        py_util_df = py_wip_df[['STAFFINDEX', 'WIPHOURS', 'BILLABLEHOURS', 'NONBILLABLEHOURS']]
        py_util_df = py_util_df.groupby('STAFFINDEX').agg(TOTAL_HOURS=('WIPHOURS', 'sum'), BILLABLE_HOURS=('BILLABLEHOURS', 'sum'), NON_BILL_HOURS=('NONBILLABLEHOURS', 'sum')).reset_index()
        py_util_df['UTILIZATION'] = round((py_util_df['BILLABLE_HOURS'] / py_util_df['TOTAL_HOURS']) * 100, 2).astype(str) + '%'

        py_col.markdown('##### Prior Year Hours and Utilization')
        py_col.dataframe(py_util_df[['TOTAL_HOURS', 'BILLABLE_HOURS', 'NON_BILL_HOURS', 'UTILIZATION']], use_container_width=True)

        cy_real_df = cy_wip_df[['STAFFINDEX', 'BILLABLEHOURS', 'WIPBILLED', 'WIPAMOUNT']]
        cy_real_df = cy_real_df.groupby('STAFFINDEX').agg(BILLABLE_HOURS=('BILLABLEHOURS', 'sum'), WIP_BILLED=('WIPBILLED', 'sum'), WIP_AMOUNT=('WIPAMOUNT', 'sum')).reset_index()
        cy_real_df['REALIZATION'] = round((cy_real_df['WIP_BILLED'] / cy_real_df['WIP_AMOUNT']) * 100, 2).astype(str) + '%'
        cy_real_df['EFF_RATE'] = round((cy_real_df['WIP_BILLED'] / cy_real_df['BILLABLE_HOURS']), 2)
        cy_real_df.loc[:, 'billed_for_calc'] = cy_real_df['WIP_BILLED']
        cy_real_df.loc[:, 'amount_for_calc'] = cy_real_df['WIP_AMOUNT']
        cy_real_df['WIP_BILLED'] = cy_real_df['WIP_BILLED'].apply(lambda x: "${:,.2f}".format(x))
        cy_real_df['WIP_AMOUNT'] = cy_real_df['WIP_AMOUNT'].apply(lambda x: "${:,.2f}".format(x))
        cy_real_df['EFF_RATE'] = cy_real_df['EFF_RATE'].apply(lambda x: "${:,.2f}".format(x))

        cy_col.markdown('##### Current Year Effective Rate and Realization')
        cy_col.dataframe(cy_real_df[['WIP_AMOUNT', 'WIP_BILLED', 'EFF_RATE', 'REALIZATION']], use_container_width=True)

        cy_util, cy_real, cy_eff = cy_col.columns(3)

        cy_util.metric('Avg Utilization for Level CY', '{:.2f}%'.format(cy_benchmark_util), round(round((cy_util_df['BILLABLE_HOURS'].iloc[0] / cy_util_df['TOTAL_HOURS'].iloc[0]) * 100, 2) - cy_benchmark_util, 2))
        cy_real.metric('Avg Realization for Level CY', '{:.2f}%'.format(cy_benchmark_real), round(round((cy_real_df['billed_for_calc'].iloc[0] / cy_real_df['amount_for_calc'].iloc[0]) * 100, 2) - cy_benchmark_real, 2))
        cy_eff.metric('Avg Effective Rate for Level CY', '${:,.2f}%'.format(cy_benchmark_eff), round(round((cy_real_df['billed_for_calc'].iloc[0] / cy_real_df['BILLABLE_HOURS'].iloc[0]), 2) - cy_benchmark_eff, 2))

        py_real_df = py_wip_df[['STAFFINDEX', 'BILLABLEHOURS', 'WIPBILLED', 'WIPAMOUNT']]
        py_real_df = py_real_df.groupby('STAFFINDEX').agg(BILLABLE_HOURS=('BILLABLEHOURS', 'sum'), WIP_BILLED=('WIPBILLED', 'sum'), WIP_AMOUNT=('WIPAMOUNT', 'sum')).reset_index()
        py_real_df['REALIZATION'] = round((py_real_df['WIP_BILLED'] / py_real_df['WIP_AMOUNT']) * 100, 2).astype(str) + '%'
        py_real_df['EFF_RATE'] = round((py_real_df['WIP_BILLED'] / py_real_df['BILLABLE_HOURS']), 2)
        py_real_df.loc[:, 'billed_for_calc'] = py_real_df['WIP_BILLED']
        py_real_df.loc[:, 'amount_for_calc'] = py_real_df['WIP_AMOUNT']
        py_real_df['WIP_BILLED'] = py_real_df['WIP_BILLED'].apply(lambda x: "${:,.2f}".format(x))
        py_real_df['WIP_AMOUNT'] = py_real_df['WIP_AMOUNT'].apply(lambda x: "${:,.2f}".format(x))
        py_real_df['EFF_RATE'] = py_real_df['EFF_RATE'].apply(lambda x: "${:,.2f}".format(x))
        
        py_col.markdown('##### Prior Year Effective Rate and Realization')
        py_col.dataframe(py_real_df[['WIP_AMOUNT', 'WIP_BILLED', 'EFF_RATE', 'REALIZATION']], use_container_width=True)

        py_util, py_real, py_eff = py_col.columns(3)

        py_util.metric('Avg Utilization for Level PY', '{:.2f}%'.format(py_benchmark_util), round(round((py_util_df['BILLABLE_HOURS'].iloc[0] / py_util_df['TOTAL_HOURS'].iloc[0]) * 100, 2) - py_benchmark_util, 2))
        py_real.metric('Avg Realization for Level PY', '{:.2f}%'.format(py_benchmark_real), round(round((py_real_df['billed_for_calc'].iloc[0] / py_real_df['amount_for_calc'].iloc[0]) * 100, 2) - py_benchmark_real, 2))
        py_eff.metric('Avg Effective Rate for Level PY', '${:,.2f}%'.format(py_benchmark_eff), round(round((py_real_df['billed_for_calc'].iloc[0] / py_real_df['BILLABLE_HOURS'].iloc[0]), 2) - py_benchmark_eff, 2))

        cy_client_df = cy_wip_df[['CLIENT', 'BILLABLEHOURS', 'WIPBILLED', 'WIPAMOUNT']]
        cy_client_df = cy_client_df.groupby('CLIENT').agg(BILLABLE_HOURS=('BILLABLEHOURS', 'sum'), WIP_BILLED=('WIPBILLED', 'sum'), WIP_AMOUNT=('WIPAMOUNT', 'sum')).reset_index()
        cy_client_df['REALIZATION'] = round((cy_client_df['WIP_BILLED'] / cy_client_df['WIP_AMOUNT']) * 100, 2).astype(str) + '%'

        cy_col.markdown('##### Current Year Billable Hours and Realization by Client')
        cy_col.dataframe(cy_client_df[['CLIENT', 'BILLABLE_HOURS', 'REALIZATION']], use_container_width=True)

        py_client_df = py_wip_df[['CLIENT', 'BILLABLEHOURS', 'WIPBILLED', 'WIPAMOUNT']]
        py_client_df = py_client_df.groupby('CLIENT').agg(BILLABLE_HOURS=('BILLABLEHOURS', 'sum'), WIP_BILLED=('WIPBILLED', 'sum'), WIP_AMOUNT=('WIPAMOUNT', 'sum')).reset_index()
        py_client_df['REALIZATION'] = round((py_client_df['WIP_BILLED'] / py_client_df['WIP_AMOUNT']) * 100, 2).astype(str) + '%'

        py_col.markdown('##### Prior Year Billable Hours and Realization by Client')
        py_col.dataframe(py_client_df[['CLIENT', 'BILLABLE_HOURS', 'REALIZATION']], use_container_width=True)
        
        # cy_wip_df = wip_df
        # py_wip_df = wip_df
    except Exception as e:
        st.write(e)

def level_2_wip(st):
    st.write('level 2')

def level_3_wip(st):
    st.write('level 3')

def level_4_wip(st):
    try:
        static_one, static_two, static_three, static_four, static_five = st.columns(5)
        filter_one, filter_two = st.columns(2)
        visuals_one, visuals_two = st.columns(2, gap='medium')
        partner_visual, partner_table = visuals_one.tabs(['Visual', 'Table'])
        current_visual, current_table = visuals_one.tabs(['Visual', 'Table'])
        office_visual, office_table = visuals_two.tabs(['Visual', 'Table'])
        aging_visual, aging_table = visuals_two.tabs(['Visual', 'Table'])
        dynamic_one, dynamic_two, dynamic_three, dynamic_four, dynamic_five = st.columns(5)

        wip_df = st.session_state['wip'].copy()
        wip_df = wip_df[(wip_df['CONTINDEX'] < 900000) & (wip_df['WIPOUTSTANDING'] != 0)]
        wip_df['WIPOUTSTANDING'] = wip_df['WIPOUTSTANDING'].round(2)
        wip_df['AGING_PERIOD'] = where(wip_df['AGING_PERIOD_SORT'] < 4, wip_df['OG_PERIOD'] + ' WIP', 'Overdue 90+ WIP')
        wip_df['CURRENTWIP'] = where(wip_df['AGING_PERIOD'] == '0-30 Days WIP', wip_df['WIPOUTSTANDING'], 0)
        wip_df['30_TO_60'] = where(wip_df['AGING_PERIOD'] == '31-60 Days WIP', wip_df['WIPOUTSTANDING'], 0)
        wip_df['60_TO_90'] = where(wip_df['AGING_PERIOD'] == '61-90 Days WIP', wip_df['WIPOUTSTANDING'], 0)
        wip_df['OVERDUEWIP'] = where(wip_df['AGING_PERIOD'] == 'Overdue 90+ WIP', wip_df['WIPOUTSTANDING'], 0)

        total_outstanding_wip = round(wip_df['WIPOUTSTANDING'].sum(), 2)
        percent_current = round((wip_df['CURRENTWIP'].sum() / total_outstanding_wip) * 100, 2)
        wip_30_60 = round((wip_df['30_TO_60'].sum() / total_outstanding_wip) * 100, 2)
        wip_60_90 = round((wip_df['60_TO_90'].sum() / total_outstanding_wip) * 100, 2)
        overdue_wip = round((wip_df['OVERDUEWIP'].sum() / total_outstanding_wip) * 100, 2)

        static_one.metric(label='Target < $4M', value='${:,.2f}'.format(total_outstanding_wip), delta=('Outstanding WIP' if total_outstanding_wip < 4000000 else '-Outstanding WIP'))
        static_two.metric(label='Target > 70%', value='{:.2f}%'.format(percent_current), delta=('% WIP in Current' if percent_current > 70 else '-% WIP in Current'))
        static_three.metric(label='Target < 20%', value='{:.2f}%'.format(wip_30_60), delta=('% WIP in 31-60 Days' if wip_30_60 < 20 else '-% WIP in 31-60 Days'))
        static_four.metric(label='Target < 15%', value='{:.2f}%'.format(wip_60_90), delta=('% WIP in 61-90 Days' if wip_60_90 < 15 else '-% WIP in 61-90 Days'))
        static_five.metric(label='Target < 5%', value='{:.2f}%'.format(overdue_wip), delta=('% WIP over 90 Days' if overdue_wip < 5 else '-% WIP over 90 Days'))

        partner_filter = filter_one.selectbox('Client Partner', ['All'] + [i for i in wip_df.CLIENT_PARTNER.sort_values().unique()])
        office_filter = filter_two.selectbox('Client Office', ['All'] + [i for i in wip_df.OFFICE.unique()])

        if partner_filter == 'All' and office_filter == 'All':
            filtered_df = wip_df.copy()

            partner_df = filtered_df[['WIPOUTSTANDING', 'CLIENT_PARTNER']]
            partner_df = partner_df.groupby('CLIENT_PARTNER', as_index=False).agg(OUTSTANDING_WIP = ('WIPOUTSTANDING', 'sum')).reset_index()
            partner_y_val = 'CLIENT_PARTNER'

            office_df = filtered_df[['WIPOUTSTANDING', 'OFFICE']]
            office_df = office_df.groupby('OFFICE', as_index=False).agg(OUTSTANDING_WIP = ('WIPOUTSTANDING', 'sum')).reset_index()
            office_y_val = 'OFFICE'
        elif partner_filter == 'All' and office_filter != 'All':
            filtered_df = wip_df[wip_df['OFFICE'] == office_filter].copy()
            partner_df = filtered_df[['WIPOUTSTANDING', 'CLIENT_PARTNER']]
            partner_df = partner_df.groupby('CLIENT_PARTNER', as_index=False).agg(OUTSTANDING_WIP = ('WIPOUTSTANDING', 'sum')).reset_index()
            partner_y_val = 'CLIENT_PARTNER'

            office_df = partner_df
            office_y_val = partner_y_val
        elif partner_filter != 'All' and office_filter == 'All':
            filtered_df = wip_df[wip_df['CLIENT_PARTNER'] == partner_filter].copy()
            partner_df = filtered_df[['WIPOUTSTANDING', 'OFFICE']]
            partner_df = partner_df.groupby('OFFICE', as_index=False).agg(OUTSTANDING_WIP = ('WIPOUTSTANDING', 'sum')).reset_index()
            partner_y_val = 'OFFICE'

            office_df = partner_df
            office_y_val = partner_y_val
        else:
            filtered_df = wip_df[(wip_df['CLIENT_PARTNER'] == partner_filter) & (wip_df['OFFICE'] == office_filter)]
            partner_df = filtered_df[['WIPOUTSTANDING', 'CLIENT']]
            partner_df = partner_df.groupby('CLIENT', as_index=False).agg(OUTSTANDING_WIP = ('WIPOUTSTANDING', 'sum')).reset_index()
            partner_y_val = 'CLIENT'

            office_df = partner_df
            office_y_val = partner_y_val

        partner_csv = convert_df(filtered_df[['WIPOUTSTANDING', 'CLIENT_PARTNER', 'CLIENT', 'OFFICE']].groupby(['CLIENT_PARTNER', 'CLIENT', 'OFFICE'], as_index=False).agg(OUTSTANDING_WIP=('WIPOUTSTANDING', 'sum')).reset_index())

        partner_fig = bar(partner_df, x='OUTSTANDING_WIP', y=partner_y_val, orientation='h', barmode='group', title='Firm WIP by Client Partner', text='OUTSTANDING_WIP').update_layout(h_bar_style).update_traces(texttemplate="%{value:$,.2f}")
        partner_visual.plotly_chart(partner_fig)
        partner_visual.download_button(
            label='Download this data',
            data=partner_csv,
            file_name='Outstanding WIP by Client Partner.csv',
            key='partner_visual_download'
        )
        partner_table.dataframe(filtered_df[['WIPOUTSTANDING', 'CLIENT_PARTNER', 'CLIENT', 'OFFICE']].groupby(['CLIENT_PARTNER', 'CLIENT', 'OFFICE'], as_index=False).agg(OUTSTANDING_WIP=('WIPOUTSTANDING', 'sum')).reset_index()[['CLIENT_PARTNER', 'CLIENT', 'OFFICE', 'OUTSTANDING_WIP']], use_container_width=True)
        partner_table.download_button(
            label='Download this data',
            data=partner_csv,
            file_name='Outstanding WIP by Client Partner.csv',
            key='partner_table_download'
        )

        office_csv = convert_df(filtered_df[['WIPOUTSTANDING', 'CLIENT_PARTNER', 'CLIENT', 'OFFICE']].groupby(['CLIENT_PARTNER', 'CLIENT', 'OFFICE'], as_index=False).agg(OUTSTANDING_WIP=('WIPOUTSTANDING', 'sum')).reset_index())

        office_fig = bar(office_df, x='OUTSTANDING_WIP', y=office_y_val, orientation='h', barmode='group', title='Firm WIP by Client Office', text='OUTSTANDING_WIP').update_layout(h_bar_style).update_traces(texttemplate="%{value:$,.2f}")
        office_visual.plotly_chart(office_fig)
        office_visual.download_button(
            label='Download this data',
            data=office_csv,
            file_name='Outstanding WIP by Client Office.csv',
            key='office_visual_download'
        )
        office_table.dataframe(filtered_df[['WIPOUTSTANDING', 'CLIENT_PARTNER', 'CLIENT', 'OFFICE']].groupby(['CLIENT_PARTNER', 'CLIENT', 'OFFICE'], as_index=False).agg(OUTSTANDING_WIP=('WIPOUTSTANDING', 'sum')).reset_index()[['CLIENT_PARTNER', 'CLIENT', 'OFFICE', 'OUTSTANDING_WIP']], use_container_width=True)
        office_table.download_button(
            label='Download this data',
            data=office_csv,
            file_name='Outstanding WIP by Client Office.csv',
            key='office_table_download'
        )

        aging_wip = filtered_df[['AGING_PERIOD', 'WIPOUTSTANDING']]
        aging_wip = aging_wip.groupby('AGING_PERIOD', as_index=False).agg(OUTSTANDING_WIP=('WIPOUTSTANDING', 'sum')).reset_index()

        aging_csv = convert_df(filtered_df[['WIPOUTSTANDING', 'CLIENT_PARTNER', 'CLIENT', 'OFFICE', 'AGING_PERIOD']].groupby(['CLIENT_PARTNER', 'CLIENT', 'OFFICE', 'AGING_PERIOD'], as_index=False).agg(OUTSTANDING_WIP=('WIPOUTSTANDING', 'sum')).reset_index()[['CLIENT_PARTNER', 'CLIENT', 'OFFICE', 'AGING_PERIOD', 'OUTSTANDING_WIP']])

        aging_fig = pie(aging_wip, values='OUTSTANDING_WIP', names='AGING_PERIOD', title='WIP Aging Periods').update_layout(pie_style)
        aging_visual.plotly_chart(aging_fig)
        aging_visual.download_button(
            label='Download this data',
            data=aging_csv,
            file_name='Aging WIP.csv',
            key='aging_visual_download'
        )

        aging_table.dataframe(filtered_df[['WIPOUTSTANDING', 'CLIENT_PARTNER', 'CLIENT', 'OFFICE', 'AGING_PERIOD']].groupby(['CLIENT_PARTNER', 'CLIENT', 'OFFICE', 'AGING_PERIOD'], as_index=False).agg(OUTSTANDING_WIP=('WIPOUTSTANDING', 'sum')).reset_index()[['CLIENT_PARTNER', 'CLIENT', 'OFFICE', 'AGING_PERIOD', 'OUTSTANDING_WIP']], use_container_width=True)
        aging_table.download_button(
            label='Download this data',
            data=aging_csv,
            file_name='Aging WIP.csv',
            key='aging_table_download'
        )

        current_csv = convert_df(filtered_df[['WIPOUTSTANDING', 'CLIENT_PARTNER', 'CLIENT', 'OFFICE']].groupby(['CLIENT_PARTNER', 'CLIENT', 'OFFICE'], as_index=False).agg(OUTSTANDING_WIP=('WIPOUTSTANDING', 'sum')).reset_index())

        current_df = filtered_df[['WIPOUTSTANDING', 'CURRENTWIP', 'OFFICE']]
        current_df = current_df.groupby(['OFFICE']).agg(CURRENT_WIP= ('CURRENTWIP', 'sum'), OUTSTANDING_WIP=('WIPOUTSTANDING', 'sum')).reset_index()
        current_df['PERCENT_CURRENT'] = round((current_df['CURRENT_WIP'] / current_df['OUTSTANDING_WIP']) * 100, 2)
        current_y_val = 'OFFICE'

        current_fig = bar(current_df, x='PERCENT_CURRENT', y=current_y_val, orientation='h', barmode='group', title='Percent Current WIP by Client Office', text='PERCENT_CURRENT').update_layout(h_bar_style).update_traces(texttemplate="%{value:.2f}%")
        current_visual.plotly_chart(current_fig)
        current_visual.download_button(
            label='Download this data',
            data=current_csv,
            file_name='Percentage Current WIP by Client Office.csv',
            key='current_visual_download'
        )
        current_table.dataframe(filtered_df[['WIPOUTSTANDING', 'CLIENT_PARTNER', 'CLIENT', 'OFFICE']].groupby(['CLIENT_PARTNER', 'CLIENT', 'OFFICE'], as_index=False).agg(OUTSTANDING_WIP=('WIPOUTSTANDING', 'sum')).reset_index()[['CLIENT_PARTNER', 'CLIENT', 'OFFICE', 'OUTSTANDING_WIP']], use_container_width=True)
        current_table.download_button(
            label='Download this data',
            data=current_csv,
            file_name='Percentage Current WIP by Client Office.csv',
            key='current_table_download'
        )

        filtered_outstanding_wip = round(filtered_df['WIPOUTSTANDING'].sum(), 2)
        filtered_percent_current = round((filtered_df['CURRENTWIP'].sum() / filtered_outstanding_wip) * 100, 2)
        filtered_wip_30_60 = round((filtered_df['30_TO_60'].sum() / filtered_outstanding_wip) * 100, 2)
        filtered_wip_60_90 = round((filtered_df['60_TO_90'].sum() / filtered_outstanding_wip) * 100, 2)
        filtered_overdue_wip = round((filtered_df['OVERDUEWIP'].sum() / filtered_outstanding_wip) * 100, 2)

        dynamic_one.metric(label='Target < $4M', value='${:,.2f}'.format(filtered_outstanding_wip), delta=('Outstanding WIP' if filtered_outstanding_wip < 4000000 else '-Outstanding WIP'))
        dynamic_two.metric(label='Target > 70%', value='{:.2f}%'.format(filtered_percent_current), delta=('% WIP in Current' if filtered_percent_current > 70 else '-% WIP in Current'))
        dynamic_three.metric(label='Target < 20%', value='{:.2f}%'.format(filtered_wip_30_60), delta=('% WIP in 31-60 Days' if filtered_wip_30_60 < 20 else '-% WIP in 31-60 Days'))
        dynamic_four.metric(label='Target < 15%', value='{:.2f}%'.format(filtered_wip_60_90), delta=('% WIP in 61-90 Days' if filtered_wip_60_90 < 15 else '-% WIP in 61-90 Days'))
        dynamic_five.metric(label='Target < 5%', value='{:.2f}%'.format(filtered_overdue_wip), delta=('% WIP over 90 Days' if filtered_overdue_wip < 5 else '-% WIP over 90 Days'))

    except Exception as e:
        st.write(e)