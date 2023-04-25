from numpy import where
# from pandas import pivot_table
from utilities.queries import get_rows
from utilities.click_handlers import convert_df, go_to_top
from plotly.express import bar, pie
from datetime import datetime

h_bar_style = {'xaxis_title_font_size': 18, 'yaxis_title_font_size': 18, 'xaxis_tickfont_size': 18, 'title_font_size': 24, 'font_size': 18} # yaxis_tickfont_size needs to be set on each graph

v_bar_style = {'legend_font_size': 18, 'title_font_size': 24, 'yaxis_tickfont_size': 18, 'xaxis_tickfont_size': 18}

pie_style = {'legend_font_size': 18, 'title_font_size': 24, 'font_size': 18}

def my_hours_month_service(wip, st):
    fym = 5
    fye_sort = ['May', 'June', 'July', 'August', 'September', 'October', 'November', 'December', 'January', 'February', 'March', 'April']
    fye = st.session_state['today'].year if st.session_state['today'].month < fym else st.session_state['today'].year + 1

    st.write(f"WIPDATE >= '{datetime(fye - 1, fym, 1).strftime('%Y-%m-%d')}' and WIPDATE < '{datetime(fye, fym, 1).strftime('%Y-%m-%d')}' and BILLABLE == 'True'")

    fy_wip_df = wip.query(f"WIPDATE >= '{datetime(fye - 1, fym, 1).strftime('%Y-%m-%d')}' and WIPDATE < '{datetime(fye, fym, 1).strftime('%Y-%m-%d')}'", inplace=True)
    # fy_wip_df = wip[(wip['WIPDATE'] >= datetime(fye - 1, fym, 1).strftime('%Y-%m-%d')) & (wip['WIPDATE'] < datetime(fye, fym, 1).strftime('%Y-%m-%d')) & (wip['BILLABLE'] == 'True')]
    st.dataframe(fy_wip_df)
    fye_wip_service_df = fy_wip_df[['WIPHOURS', 'SERVICETITLE', 'MONTH']].groupby(['MONTH', 'SERVICETITLE'], as_index=False).agg(WIP_HOURS=('WIPHOURS', 'sum')).reset_index()[['MONTH', 'SERVICETITLE', 'WIP_HOURS']]

    fy_wip_service_colors = st.session_state['color_map'][st.session_state['color_map']['SERVICE'].isin(fye_wip_service_df['SERVICETITLE'].tolist())].set_index('SERVICE')['COLOR'].to_dict()

    wip_service_fig = bar(fye_wip_service_df, x='MONTH', y='WIP_HOURS', color='SERVICETITLE', title='WIP Hours by Month and Service', color_discrete_map=fy_wip_service_colors).update_xaxes(categoryorder='array', categoryarray=fye_sort).update_layout(v_bar_style)

    st.plotly_chart(wip_service_fig, use_container_width=True)

    month_service_csv = convert_df(fye_wip_service_df)
    st.download_button(
            label='Download this data',
            data=month_service_csv,
            file_name='WIP Hours by Month and Service.csv',
            key='WIP_month_service_download'
        )

def my_hours_pie_service(wip, st, year):
    wip_service_df = wip[wip['BILLABLE'] == 'True'][['WIPHOURS', 'SERVICETITLE']].groupby(['SERVICETITLE'], as_index=False).agg(WIP_HOURS=('WIPHOURS', 'sum')).reset_index()[['SERVICETITLE', 'WIP_HOURS']]
    wip_service_colors = st.session_state['color_map'][st.session_state['color_map']['SERVICE'].isin(wip_service_df['SERVICETITLE'].tolist())].set_index('SERVICE')['COLOR'].to_dict()
    wip_service_fig = pie(wip_service_df, values='WIP_HOURS', names='SERVICETITLE', title=f'{year} WIP Hours by Service Title', color_discrete_map=wip_service_colors, color='SERVICETITLE').update_layout(pie_style).update_traces(marker=dict(line=dict(color='#fff', width=1)))
    st.plotly_chart(wip_service_fig, use_container_width=True)
    
    hours_service_csv = convert_df(wip_service_df)
    st.download_button(
            label='Download this data',
            data=hours_service_csv,
            file_name=f'{year} WIP Hours by Service Title.csv',
            key=f'WIP_{year}_hours_service_download'
        )

def my_utilization(wip):
    total_hours = wip['WIPHOURS'].sum()
    billable_hours = wip['BILLABLEHOURS'].sum()
    
    return {'total_hours': total_hours, 'billable_hours': billable_hours, 'non_bill_hours': wip['NONBILLABLEHOURS'].sum(), 'utilization': round((billable_hours / total_hours) * 100, 2)}

def my_realization(wip):
    wip_amount = wip['WIPAMOUNT'].sum()
    wip_billed = wip['WIPBILLED'].sum()
    eff_rate = round((wip_billed / wip['BILLABLEHOURS'].sum()), 2)
    realization = round((wip_billed / wip_amount) * 100, 2)

    return {'wip_amount': wip_amount, 'wip_billed': wip_billed, 'eff_rate': eff_rate, 'realization': realization}

def my_benchmarks(wip, util, real, rate):
    benchmark_real_df = wip[wip['BILLABLE'] == 'True'].groupby('STAFFINDEX').agg(BILLABLE_HOURS=('BILLABLEHOURS', 'sum'), TOTAL_HOURS=('WIPHOURS', 'sum'), WIP_BILLED=('WIPBILLED', 'sum'), WIP_AMOUNT=('WIPAMOUNT', 'sum'))
    benchmark_real_df['REALIZATION'] = round((benchmark_real_df['WIP_BILLED'] / benchmark_real_df['WIP_AMOUNT']) * 100, 2)
    benchmark_real_df['EFF_RATE'] = round((benchmark_real_df['WIP_BILLED'] / benchmark_real_df['BILLABLE_HOURS']), 2)

    benchmark_util_df = wip.groupby('STAFFINDEX').agg(BILLABLE_HOURS=('BILLABLEHOURS', 'sum'), TOTAL_HOURS=('WIPHOURS', 'sum'), WIP_BILLED=('WIPBILLED', 'sum'), WIP_AMOUNT=('WIPAMOUNT', 'sum'))

    benchmark_util_df['UTILIZATION'] = round((benchmark_util_df['BILLABLE_HOURS'] / benchmark_util_df['TOTAL_HOURS']) * 100, 2)

    benchmark_util = benchmark_util_df['UTILIZATION'].mean()
    benchmark_real = benchmark_real_df['REALIZATION'].mean()
    benchmark_rate = benchmark_real_df['EFF_RATE'].mean()

    return {'util': {'average': benchmark_util, 'diff': (util - benchmark_util)}, 'real': {'average': benchmark_real, 'diff': (real - benchmark_real)}, 'rate': {'average': benchmark_rate, 'diff': (rate - benchmark_rate)}}

def my_hours_real_client(wip, st, year):
    wip = wip.groupby('CLIENT').agg(BILLABLE_HOURS=('BILLABLEHOURS', 'sum'), WIP_BILLED=('WIPBILLED', 'sum'), WIP_AMOUNT=('WIPAMOUNT', 'sum')).reset_index()
    wip['REALIZATION'] = round((wip['WIP_BILLED'] / wip['WIP_AMOUNT']) * 100, 2).astype(str) + '%'
    st.dataframe(wip[['CLIENT', 'BILLABLE_HOURS', 'REALIZATION']], use_container_width=True)

    hours_real_csv = convert_df(wip)
    st.download_button(
            label='Download this data',
            data=hours_real_csv,
            file_name=f'{year} WIP Hours by Client.csv',
            key=f'WIP_{year}_hours_real_download'
        )

def level_1_wip(st):
    st.markdown('## WIP Reports')
    wip_df = get_rows(f"""SELECT WIP.WIPOUTSTANDING, 
    WIP.STAFFINDEX,
    S.LEVEL, 
    WIP.WIPHOURS, 
    WIP.WIPAMOUNT,
    WIP.WIPBILLED, 
    WIP.CONTINDEX, 
    WIP.WIPDATE, 
    WIP.SERVICETITLE, 
    CASE WHEN WIP.BILLABLE = 'True' THEN WIP.WIPHOURS ELSE 0 END AS BILLABLEHOURS, 
    CASE WHEN WIP.BILLABLE = 'False' THEN WIP.WIPHOURS ELSE 0 END AS NONBILLABLEHOURS,
    WIP.BILLABLE,
    C.CLIENT_PARTNER, 
    C.CLIENT, 
    C.OFFICE, 
    D.AGING_PERIOD_SORT, 
    D.AGING_PERIOD as OG_PERIOD, 
    D.MONTH_NAME AS MONTH
from TRANS_WIP WIP
    INNER JOIN DIM_CLIENT_MASTER C ON C.ContIndex = WIP.ContIndex 
    INNER JOIN DIM_DATES D ON D.CALENDAR_DATE = WIP.WIPDATE
    INNER JOIN DIM_STAFF_MASTER S ON S.STAFFINDEX = WIP.STAFFINDEX
WHERE WIPOUTSTANDING <> 0 AND TRANSTYPE IN (1, 2, 3)
    AND S.LEVEL = '{st.session_state['user']['LEVEL'].iloc[0]}';""")
    try:
        benchmark_df = wip_df[['STAFFINDEX', 'LEVEL', 'BILLABLEHOURS', 'WIPHOURS', 'WIPDATE', 'WIPBILLED', 'WIPAMOUNT', 'BILLABLE']].copy()
        wip_df = wip_df[wip_df['STAFFINDEX'] == st.session_state['user']['STAFFINDEX'].iloc[0]]
        
        from pandas import to_datetime
        wip_df['WIPDATE'] = to_datetime(wip_df['WIPDATE'], format='%Y-%m-%d')
        benchmark_df['WIPDATE'] = to_datetime(benchmark_df['WIPDATE'], format='%Y-%m-%d')

        wip_df = wip_df[wip_df['STAFFINDEX'] == st.session_state['user']['STAFFINDEX'].iloc[0]]
        cy_benchmark_df = benchmark_df[(benchmark_df['WIPDATE'] >= datetime(st.session_state['today'].year - 1, st.session_state['today'].month, st.session_state['today'].day).strftime('%Y-%m-%d')) & (benchmark_df['WIPDATE'] < st.session_state['today'].strftime('%Y-%m-%d'))][['STAFFINDEX', 'BILLABLEHOURS', 'WIPHOURS', 'WIPBILLED', 'WIPAMOUNT', 'BILLABLE']]
        py_benchmark_df = benchmark_df[(benchmark_df['WIPDATE'] >= datetime(st.session_state['today'].year - 2, st.session_state['today'].month, st.session_state['today'].day).strftime('%Y-%m-%d')) & (benchmark_df['WIPDATE'] < datetime(st.session_state['today'].year - 1, st.session_state['today'].month, st.session_state['today'].day).strftime('%Y-%m-%d'))]

        my_hours_month_service(wip_df, st)

        py_col, cy_col = st.columns(2, gap='medium')
        py_col.markdown('### Prior Year Data')
        cy_col.markdown('### Current Year Data')

        cy_wip_df = wip_df[(wip_df['WIPDATE'] >= datetime(st.session_state['today'].year - 1, st.session_state['today'].month, st.session_state['today'].day).strftime('%Y-%m-%d')) & (wip_df['WIPDATE'] < st.session_state['today'].strftime('%Y-%m-%d'))]

        py_wip_df = wip_df[(wip_df['WIPDATE'] >= datetime(st.session_state['today'].year - 2, st.session_state['today'].month, st.session_state['today'].day).strftime('%Y-%m-%d')) & (wip_df['WIPDATE'] < datetime(st.session_state['today'].year - 1, st.session_state['today'].month, st.session_state['today'].day).strftime('%Y-%m-%d'))]

        with py_col:
            my_hours_pie_service(py_wip_df, st, 'PY')

            st.markdown('#### Prior Year Hours and Utilization')
            my_py_util = my_utilization(py_wip_df[['WIPHOURS', 'BILLABLEHOURS', 'NONBILLABLEHOURS']])
            metric_util_one, metric_util_two = st.columns(2) 
            metric_util_three, metric_util_four = st.columns(2)
            metric_util_one.metric('Total Hours', '{:,.2f}'.format(my_py_util['total_hours']), '~~~', 'off')
            metric_util_three.metric('Billable Hours', '{:,.2f}'.format(my_py_util['billable_hours']), '~~~', 'off')
            metric_util_four.metric('Nonbillable Hours', '{:,.2f}'.format(my_py_util['non_bill_hours']), '~~~', 'off')
            metric_util_two.metric('Utilization', '{:,.2f}%'.format(my_py_util['utilization']), '~~~', 'off')

            st.markdown('#### Prior Year Effective Rate and Realization')
            my_py_real = my_realization(py_wip_df[py_wip_df['BILLABLE'] == 'True'][['BILLABLEHOURS', 'WIPBILLED', 'WIPAMOUNT']])
            metric_real_one, metric_real_two = st.columns(2) 
            metric_real_three, metric_real_four = st.columns(2)
            metric_real_one.metric('WIP Amount', '${:,.2f}'.format(my_py_real['wip_amount']), '~~~', 'off')
            metric_real_two.metric('WIP Billed', '${:,.2f}'.format(my_py_real['wip_billed']), '~~~', 'off')
            metric_real_three.metric('Effective Rate', '${:,.2f}'.format(my_py_real['eff_rate']), '~~~', 'off')
            metric_real_four.metric('Realization', '{:,.2f}%'.format(my_py_real['realization']), '~~~', 'off')

            py_benchmarks = my_benchmarks(py_benchmark_df, my_py_util['utilization'], my_py_real['realization'], my_py_real['eff_rate'])
            util, real, rate = st.columns(3)
            util.metric('Avg Utilization for Level PY', '{:.2f}%'.format(py_benchmarks['util']['average']), '{:,.2f}%'.format(py_benchmarks['util']['diff']))
            real.metric('Avg Realization for Level PY', '{:.2f}%'.format(py_benchmarks['real']['average']), '{:,.2f}%'.format(py_benchmarks['real']['diff']))
            rate.metric('Avg Effective Rate for Level PY', '${:,.2f}'.format(py_benchmarks['rate']['average']), '{:,.2f}'.format(py_benchmarks['rate']['diff']))
            
            st.markdown('#### Prior Year Billable Hours and Realization by Client')
            my_hours_real_client(py_wip_df[py_wip_df['BILLABLE'] == 'True'][['CLIENT', 'BILLABLEHOURS', 'WIPBILLED', 'WIPAMOUNT']], st, 'PY')

        with cy_col:
            my_hours_pie_service(cy_wip_df, st, 'CY')

            st.markdown('#### Current Year Hours and Utilization')
            my_cy_util = my_utilization(cy_wip_df[['WIPHOURS', 'BILLABLEHOURS', 'NONBILLABLEHOURS']])
            metric_util_one, metric_util_two = st.columns(2) 
            metric_util_three, metric_util_four = st.columns(2)
            metric_util_one.metric('Total Hours', '{:,.2f}'.format(my_cy_util['total_hours']), '{:,.2f}'.format(my_cy_util['total_hours'] - my_py_util['total_hours']))
            metric_util_three.metric('Billable Hours', '{:,.2f}'.format(my_cy_util['billable_hours']), '{:,.2f}'.format(my_cy_util['billable_hours'] - my_py_util['billable_hours']))
            metric_util_four.metric('Nonbillable Hours', '{:,.2f}'.format(my_cy_util['non_bill_hours']), '{:,.2f}'.format(my_cy_util['non_bill_hours'] - my_py_util['non_bill_hours']))
            metric_util_two.metric('Utilization', '{:,.2f}%'.format(my_cy_util['utilization']), '{:,.2f}%'.format(my_cy_util['utilization'] - my_py_util['utilization']))

            st.markdown('#### Current Year Effective Rate and Realization')
            my_cy_real = my_realization(cy_wip_df[cy_wip_df['BILLABLE'] == 'True'][['BILLABLEHOURS', 'WIPBILLED', 'WIPAMOUNT']])
            metric_real_one, metric_real_two = st.columns(2) 
            metric_real_three, metric_real_four = st.columns(2)
            metric_real_one.metric('WIP Amount', '${:,.2f}'.format(my_cy_real['wip_amount']), '{:,.2f}'.format(my_cy_real['wip_amount'] - my_py_real['wip_amount']))
            metric_real_two.metric('WIP Billed', '${:,.2f}'.format(my_cy_real['wip_billed']), '{:,.2f}'.format(my_cy_real['wip_billed'] - my_py_real['wip_billed']))
            metric_real_three.metric('Effective Rate', '${:,.2f}'.format(my_cy_real['eff_rate']), '{:,.2f}'.format(my_cy_real['eff_rate'] - my_py_real['eff_rate']))
            metric_real_four.metric('Realization', '{:,.2f}%'.format(my_cy_real['realization']), '{:,.2f}%'.format(my_cy_real['realization'] - my_py_real['realization']))

            cy_benchmarks = my_benchmarks(cy_benchmark_df, my_cy_util['utilization'], my_cy_real['realization'], my_cy_real['eff_rate'])
            util, real, rate = st.columns(3)
            util.metric('Avg Utilization for Level CY', '{:.2f}%'.format(cy_benchmarks['util']['average']), '{:,.2f}%'.format(cy_benchmarks['util']['diff']))
            real.metric('Avg Realization for Level CY', '{:.2f}%'.format(cy_benchmarks['real']['average']), '{:,.2f}%'.format(cy_benchmarks['real']['diff']))
            rate.metric('Avg Effective Rate for Level CY', '${:,.2f}'.format(cy_benchmarks['rate']['average']), '{:,.2f}'.format(cy_benchmarks['rate']['diff']))

            st.markdown('#### Prior Year Billable Hours and Realization by Client')
            my_hours_real_client(cy_wip_df[cy_wip_df['BILLABLE'] == 'True'][['CLIENT', 'BILLABLEHOURS', 'WIPBILLED', 'WIPAMOUNT']], st, 'CY')
        
        go_to_top(st.markdown)

    except Exception as e:
        st.write(e)

def level_2_wip(st):
    st.write('level 2')

def level_3_wip(st):
    st.write('level 3')

def level_4_wip(st):
    st.markdown('## WIP Reports')
    wip_df = get_rows(f"""SELECT WIP.WIPOUTSTANDING, 
    WIP.STAFFINDEX,
    S.LEVEL, 
    WIP.WIPHOURS, 
    WIP.WIPAMOUNT,
    WIP.WIPBILLED, 
    WIP.CONTINDEX, 
    WIP.WIPDATE, 
    WIP.SERVICETITLE, 
    CASE WHEN WIP.BILLABLE = 'True' THEN WIP.WIPHOURS ELSE 0 END AS BILLABLEHOURS, 
    CASE WHEN WIP.BILLABLE = 'False' THEN WIP.WIPHOURS ELSE 0 END AS NONBILLABLEHOURS,
    WIP.BILLABLE,
    C.CLIENT_PARTNER, 
    C.CLIENT, 
    C.OFFICE, 
    D.AGING_PERIOD_SORT, 
    D.AGING_PERIOD as OG_PERIOD, 
    D.MONTH_NAME AS MONTH
from TRANS_WIP WIP
    INNER JOIN DIM_CLIENT_MASTER C ON C.ContIndex = WIP.ContIndex 
    INNER JOIN DIM_DATES D ON D.CALENDAR_DATE = WIP.WIPDATE
    INNER JOIN DIM_STAFF_MASTER S ON S.STAFFINDEX = WIP.STAFFINDEX
WHERE WIPOUTSTANDING <> 0 AND TRANSTYPE IN (1, 2, 3);""")

    try:
        static_one, static_two, static_three, static_four, static_five = st.columns(5)
        filter_one, filter_two = st.columns(2)
        visuals_one, visuals_two = st.columns(2, gap='medium')
        partner_visual, partner_table = visuals_one.tabs(['Visual', 'Table'])
        current_visual, current_table = visuals_one.tabs(['Visual', 'Table'])
        office_visual, office_table = visuals_two.tabs(['Visual', 'Table'])
        aging_visual, aging_table = visuals_two.tabs(['Visual', 'Table'])
        dynamic_one, dynamic_two, dynamic_three, dynamic_four, dynamic_five = st.columns(5)

        wip_df = wip_df[(wip_df['BILLABLE'] == 'True') & (wip_df['WIPOUTSTANDING'] != 0)]
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
            key='WIP_partner_visual_download'
        )
        partner_table.dataframe(filtered_df[['WIPOUTSTANDING', 'CLIENT_PARTNER', 'CLIENT', 'OFFICE']].groupby(['CLIENT_PARTNER', 'CLIENT', 'OFFICE'], as_index=False).agg(OUTSTANDING_WIP=('WIPOUTSTANDING', 'sum')).reset_index()[['CLIENT_PARTNER', 'CLIENT', 'OFFICE', 'OUTSTANDING_WIP']], use_container_width=True)
        partner_table.download_button(
            label='Download this data',
            data=partner_csv,
            file_name='Outstanding WIP by Client Partner.csv',
            key='WIP_partner_table_download'
        )

        office_csv = convert_df(filtered_df[['WIPOUTSTANDING', 'CLIENT_PARTNER', 'CLIENT', 'OFFICE']].groupby(['CLIENT_PARTNER', 'CLIENT', 'OFFICE'], as_index=False).agg(OUTSTANDING_WIP=('WIPOUTSTANDING', 'sum')).reset_index())

        office_fig = bar(office_df, x='OUTSTANDING_WIP', y=office_y_val, orientation='h', barmode='group', title='Firm WIP by Client Office', text='OUTSTANDING_WIP').update_layout(h_bar_style).update_traces(texttemplate="%{value:$,.2f}")
        office_visual.plotly_chart(office_fig)
        office_visual.download_button(
            label='Download this data',
            data=office_csv,
            file_name='Outstanding WIP by Client Office.csv',
            key='WIP_office_visual_download'
        )
        office_table.dataframe(filtered_df[['WIPOUTSTANDING', 'CLIENT_PARTNER', 'CLIENT', 'OFFICE']].groupby(['CLIENT_PARTNER', 'CLIENT', 'OFFICE'], as_index=False).agg(OUTSTANDING_WIP=('WIPOUTSTANDING', 'sum')).reset_index()[['CLIENT_PARTNER', 'CLIENT', 'OFFICE', 'OUTSTANDING_WIP']], use_container_width=True)
        office_table.download_button(
            label='Download this data',
            data=office_csv,
            file_name='Outstanding WIP by Client Office.csv',
            key='WIP_office_table_download'
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
            key='WIP_aging_visual_download'
        )

        aging_table.dataframe(filtered_df[['WIPOUTSTANDING', 'CLIENT_PARTNER', 'CLIENT', 'OFFICE', 'AGING_PERIOD']].groupby(['CLIENT_PARTNER', 'CLIENT', 'OFFICE', 'AGING_PERIOD'], as_index=False).agg(OUTSTANDING_WIP=('WIPOUTSTANDING', 'sum')).reset_index()[['CLIENT_PARTNER', 'CLIENT', 'OFFICE', 'AGING_PERIOD', 'OUTSTANDING_WIP']], use_container_width=True)
        aging_table.download_button(
            label='Download this data',
            data=aging_csv,
            file_name='Aging WIP.csv',
            key='WIP_aging_table_download'
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
            key='WIP_current_visual_download'
        )
        current_table.dataframe(filtered_df[['WIPOUTSTANDING', 'CLIENT_PARTNER', 'CLIENT', 'OFFICE']].groupby(['CLIENT_PARTNER', 'CLIENT', 'OFFICE'], as_index=False).agg(OUTSTANDING_WIP=('WIPOUTSTANDING', 'sum')).reset_index()[['CLIENT_PARTNER', 'CLIENT', 'OFFICE', 'OUTSTANDING_WIP']], use_container_width=True)
        current_table.download_button(
            label='Download this data',
            data=current_csv,
            file_name='Percentage Current WIP by Client Office.csv',
            key='WIP_current_table_download'
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

        go_to_top(st.markdown)
    except Exception as e:
        st.write(e)