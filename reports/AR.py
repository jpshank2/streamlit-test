from numpy import where
from plotly.express import bar, pie
from utilities.queries import get_rows
from utilities.click_handlers import convert_df, go_to_top

h_bar_style = {'xaxis_title_font_size': 18, 'yaxis_title_font_size': 18, 'xaxis_tickfont_size': 18, 'title_font_size': 24, 'font_size': 18} # yaxis_tickfont_size needs to be set on each graph

v_bar_style = {'legend_font_size': 18, 'title_font_size': 24, 'yaxis_tickfont_size': 18, 'xaxis_tickfont_size': 18}

pie_style = {'legend_font_size': 18, 'title_font_size': 24, 'font_size': 18}


# def create_ar_reports(st):
#     try:
#         rows = get_rows("""SELECT AR.*, A.NAME AS CLIENT_NAME, C.*, D.AGING_PERIOD_SORT, D.AGING_PERIOD as OG_PERIOD 
#             from TRANS_AR AR 
#                 INNER JOIN DIM_CLIENT_MASTER C ON C.ContIndex = AR.ContIndex 
#                 INNER JOIN CLIENT_BMSS_SANDBOX_DB.ANONYMOUS.DIM_CLIENT_ANONYMOUS A ON A.CONTIDX = C.CONTINDEX
#                 INNER JOIN DIM_DATES D ON D.CALENDAR_DATE = AR.DEBTTRANDATE 
#             WHERE DEBTTRANUNPAID <> 0;""", st.session_state['today'])

#         office_office_AR = rows[['OFFICE', 'DEBTTRANUNPAID']]
#         office_office_AR = office_office_AR.groupby('OFFICE', as_index=False).agg(OUTSTANDING_AR = ('DEBTTRANUNPAID', 'sum')).reset_index()

#         levels = [
#             st.selectbox('Office', ['All'] + [i for i in office_office_AR.OFFICE.unique()])
#         ]


#         if levels[0] == 'All':
#             office_AR_DF = office_office_AR
#             yVal = 'OFFICE'
#             title = 'AR by Office w/ drilldown'
#         else:
#             office_partner_AR = rows[rows['OFFICE'] == levels[0]]
#             office_partner_AR = office_partner_AR[['CLIENTPARTNER', 'DEBTTRANUNPAID']]
#             levels.append(st.selectbox('Client Partner', ['All'] + [i for i in office_partner_AR.CLIENTPARTNER.unique()]))

#             office_AR_DF = office_partner_AR.groupby('CLIENTPARTNER', as_index=False).agg(OUTSTANDING_AR = ('DEBTTRANUNPAID', 'sum')).reset_index()
#             yVal = 'CLIENTPARTNER'
#             title = levels[0] + ' AR by Client Partner w/ drilldown'

#             if levels[1] != 'All':
#                 office_AR_DF = rows[(rows['OFFICE'] == levels[0]) & (rows['CLIENTPARTNER'] == levels[1])]
#                 office_AR_DF = office_AR_DF[['CLIENT_NAME', 'DEBTTRANUNPAID']]
#                 office_AR_DF = office_AR_DF.groupby('CLIENT_NAME', as_index=False).agg(OUTSTANDING_AR = ('DEBTTRANUNPAID', 'sum')).reset_index()
#                 yVal = 'CLIENT_NAME'
#                 title = f'{levels[1]}\'s {levels[0]} AR by Client w/ drilldown'
                
#         st.write(bar(office_AR_DF, x='OUTSTANDING_AR', y=yVal, orientation='h', barmode='group', title=title, text='OUTSTANDING_AR'))

#         partner_AR = rows[['CLIENTPARTNER', 'DEBTTRANUNPAID']].copy()
#         partner_AR = partner_AR.groupby('CLIENTPARTNER', as_index=False).agg(OUTSTANDING_AR=('DEBTTRANUNPAID', 'sum')).reset_index()

#         st.write(bar(partner_AR, y='CLIENTPARTNER', x='OUTSTANDING_AR', orientation='h', title='AR by Client Partner'))

#         aging_AR = rows[['AGING_PERIOD_SORT', 'OG_PERIOD', 'DEBTTRANUNPAID']].copy()
#         aging_AR['AGING_PERIOD'] = where(aging_AR['AGING_PERIOD_SORT'] < 4, aging_AR['OG_PERIOD'] + ' AR', 'Overdue 90+ AR')
#         aging_AR = aging_AR[['AGING_PERIOD', 'DEBTTRANUNPAID']]
#         aging_AR = aging_AR.groupby('AGING_PERIOD', as_index=False).agg(OUTSTANDING_AR=('DEBTTRANUNPAID', 'sum')).reset_index()
#         st.write(pie(aging_AR, values='OUTSTANDING_AR', names='AGING_PERIOD', title='AR Aging Periods'))
        
#     except Exception as e:
#         st.write(e)

def level_1_ar(st):
    return True

def level_2_ar(st):
    st.write('ar reports')

def level_3_ar(st):
    st.write('ar reports')

def level_4_ar(st):
    st.markdown('## AR Reports')
#     ar_df = get_rows(f"""SELECT AR.DEBTTRANUNPAID AS UNPAID_INVOICE, 
#     AR.DEBTTRANTYPE,
#     AR.CONTINDEX, 
#     AR.DEBTTRANDATE AS AR_DATE, 
#     CP.STAFFNAME AS CLIENT_PARTNER, 
#     A.NAME AS CLIENT, 
#     CASE 
#         WHEN C.OFFICE = 'BHM' THEN 'ATL'
#         WHEN C.OFFICE = 'GAD' THEN 'LAS'
#         WHEN C.OFFICE = 'HSV' THEN 'NYC'
#         WHEN C.OFFICE = 'AO' THEN 'MPS'
#         ELSE C.OFFICE
#     END AS OFFICE, 
#     D.AGING_PERIOD_SORT, 
#     D.AGING_PERIOD as OG_PERIOD, 
#     D.MONTH_NAME AS MONTH
# from TRANS_AR AR
#     INNER JOIN DIM_CLIENT_MASTER C ON C.ContIndex = AR.ContIndex 
#     INNER JOIN CLIENT_BMSS_SANDBOX_DB.ANONYMOUS.DIM_CLIENT_ANONYMOUS A ON A.CONTIDX = C.CONTINDEX AND A.NAME IS NOT NULL
#     INNER JOIN ANONYMOUS.DIM_STAFF_ANONYMOUS CP ON CP.STAFFIDX = C.CLIENT_PARTNER_IDX AND CP.STAFFNAME IS NOT NULL
#     INNER JOIN DIM_DATES D ON D.CALENDAR_DATE = AR.DEBTTRANDATE
# WHERE AR.DEBTTRANUNPAID <> 0 AND AR.DEBTTRANTYPE IN (3, 6);
# """, st.session_state['today'])

    static_one, static_two, static_three, static_four, static_five = st.columns(5)
    filter_one, filter_two = st.columns(2)
    visuals_one, visuals_two = st.columns(2, gap='medium')
    partner_visual, partner_table = visuals_one.tabs(['Visual', 'Table'])
    current_visual, current_table = visuals_one.tabs(['Visual', 'Table'])
    office_visual, office_table = visuals_two.tabs(['Visual', 'Table'])
    aging_visual, aging_table = visuals_two.tabs(['Visual', 'Table'])
    dynamic_one, dynamic_two, dynamic_three, dynamic_four, dynamic_five = st.columns(5)

    try:
        static_metric_ar_df = get_rows("""SELECT SUM(DEBTTRANUNPAID) AS UNPAID_INVOICE
                ,ROUND(SUM(
                    CASE WHEN D.AGING_PERIOD_SORT = 1 THEN AR.DEBTTRANUNPAID
                    ELSE 0 END
                ) / SUM(DEBTTRANUNPAID), 4) * 100 AS PERCENT_CURR
                ,ROUND(SUM(
                    CASE WHEN D.AGING_PERIOD_SORT = 2 THEN AR.DEBTTRANUNPAID
                    ELSE 0 END
                ) / SUM(DEBTTRANUNPAID), 4) * 100 AS PERCENT_31_60
                ,ROUND(SUM(
                    CASE WHEN D.AGING_PERIOD_SORT = 3 THEN AR.DEBTTRANUNPAID
                    ELSE 0 END
                ) / SUM(DEBTTRANUNPAID), 4) * 100 AS PERCENT_61_90
                ,ROUND(SUM(
                    CASE WHEN D.AGING_PERIOD_SORT > 3 THEN AR.DEBTTRANUNPAID
                    ELSE 0 END
                ) / SUM(DEBTTRANUNPAID), 4) * 100 AS PERCENT_OVERDUE
            FROM TRANS_AR AR
                INNER JOIN DIM_DATES D ON D.CALENDAR_DATE = AR.DEBTTRANDATE
            WHERE AR.DEBTTRANUNPAID <> 0 AND AR.DEBTTRANTYPE IN (3, 6);""", st.session_state['today'])

        static_one.metric(label='Target < $2M', value='${:,.2f}'.format(static_metric_ar_df['UNPAID_INVOICE'].iloc[0]), delta=('Outstanding AR' if static_metric_ar_df['UNPAID_INVOICE'].iloc[0] < 2000000 else '-Outstanding AR'))
        static_two.metric(label='Target > 75%', value='{:.2f}%'.format(static_metric_ar_df['PERCENT_CURR'].iloc[0]), delta=('% AR in Current' if static_metric_ar_df['PERCENT_CURR'].iloc[0] > 75 else '-% AR in Current'))
        static_three.metric(label='Target < 15%', value='{:.2f}%'.format(static_metric_ar_df['PERCENT_31_60'].iloc[0]), delta=('% AR in 31-60 Days' if static_metric_ar_df['PERCENT_31_60'].iloc[0] < 15 else '-% AR in 31-60 Days'))
        static_four.metric(label='Target < 10%', value='{:.2f}%'.format(static_metric_ar_df['PERCENT_61_90'].iloc[0]), delta=('% AR in 61-90 Days' if static_metric_ar_df['PERCENT_61_90'].iloc[0] < 10 else '-% AR in 61-90 Days'))
        static_five.metric(label='Target < 5%', value='{:.2f}%'.format(static_metric_ar_df['PERCENT_OVERDUE'].iloc[0]), delta=('% AR over 90 Days' if static_metric_ar_df['PERCENT_OVERDUE'].iloc[0] < 5 else '-% AR over 90 Days'))

        unpaid_ar_df = get_rows("""SELECT SUM(AR.DEBTTRANUNPAID) AS UNPAID_INVOICE, 
            CP.STAFFNAME AS CLIENT_PARTNER, 
            A.NAME AS CLIENT, 
            CASE 
                WHEN C.OFFICE = 'BHM' THEN 'ATL'
                WHEN C.OFFICE = 'GAD' THEN 'LAS'
                WHEN C.OFFICE = 'HSV' THEN 'NYC'
                WHEN C.OFFICE = 'AO' THEN 'MPS'
                ELSE C.OFFICE
            END AS OFFICE
        from TRANS_AR AR
            INNER JOIN DIM_CLIENT_MASTER C ON C.ContIndex = AR.ContIndex 
            INNER JOIN CLIENT_BMSS_SANDBOX_DB.ANONYMOUS.DIM_CLIENT_ANONYMOUS A ON A.CONTIDX = C.CONTINDEX AND A.NAME IS NOT NULL
            INNER JOIN ANONYMOUS.DIM_STAFF_ANONYMOUS CP ON CP.STAFFIDX = C.CLIENT_PARTNER_IDX AND CP.STAFFNAME IS NOT NULL
        WHERE AR.DEBTTRANUNPAID <> 0 AND AR.DEBTTRANTYPE IN (3, 6)
        GROUP BY CP.STAFFNAME, 
            A.NAME, 
            CASE 
                WHEN C.OFFICE = 'BHM' THEN 'ATL'
                WHEN C.OFFICE = 'GAD' THEN 'LAS'
                WHEN C.OFFICE = 'HSV' THEN 'NYC'
                WHEN C.OFFICE = 'AO' THEN 'MPS'
                ELSE C.OFFICE
            END;""", st.session_state['today'])

        partner_filter = filter_one.selectbox('Client Partner', ['All'] + [i for i in unpaid_ar_df.CLIENT_PARTNER.unique()], key='ar_partner_filter')

        office_filter = filter_two.selectbox('Client Office', ['All'] + [i for i in unpaid_ar_df.OFFICE.unique()], key='ar_office_filter')

    except Exception as e:
        st.write(e)
    
    try:

        if partner_filter == 'All' and office_filter == 'All':
            filtered_df = unpaid_ar_df.copy()

            partner_df = filtered_df[['UNPAID_INVOICE', 'CLIENT_PARTNER']]
            partner_df = partner_df.groupby('CLIENT_PARTNER', as_index=False).agg(OUTSTANDING_AR = ('UNPAID_INVOICE', 'sum')).reset_index()
            partner_y_val = 'CLIENT_PARTNER'

            office_df = filtered_df[['UNPAID_INVOICE', 'OFFICE']]
            office_df = office_df.groupby('OFFICE', as_index=False).agg(OUTSTANDING_AR = ('UNPAID_INVOICE', 'sum')).reset_index()
            office_y_val = 'OFFICE'
        elif partner_filter == 'All' and office_filter != 'All':
            filtered_df = unpaid_ar_df[unpaid_ar_df['OFFICE'] == office_filter].copy()
            partner_df = filtered_df[['UNPAID_INVOICE', 'CLIENT_PARTNER']]
            partner_df = partner_df.groupby('CLIENT_PARTNER', as_index=False).agg(OUTSTANDING_AR = ('UNPAID_INVOICE', 'sum')).reset_index()
            partner_y_val = 'CLIENT_PARTNER'

            office_df = partner_df
            office_y_val = partner_y_val
        elif partner_filter != 'All' and office_filter == 'All':
            filtered_df = unpaid_ar_df[unpaid_ar_df['CLIENT_PARTNER'] == partner_filter].copy()
            partner_df = filtered_df[['UNPAID_INVOICE', 'OFFICE']]
            partner_df = partner_df.groupby('OFFICE', as_index=False).agg(OUTSTANDING_AR = ('UNPAID_INVOICE', 'sum')).reset_index()
            partner_y_val = 'OFFICE'

            office_df = partner_df
            office_y_val = partner_y_val
        else:
            filtered_df = unpaid_ar_df[(unpaid_ar_df['CLIENT_PARTNER'] == partner_filter) & (unpaid_ar_df['OFFICE'] == office_filter)]
            partner_df = filtered_df[['UNPAID_INVOICE', 'CLIENT']]
            partner_df.columns = ['OUTSTANDING_AR', 'CLIENT']
            # partner_df = partner_df.groupby('CLIENT', as_index=False).agg(OUTSTANDING_AR = ('UNPAID_INVOICE', 'sum')).reset_index()
            partner_y_val = 'CLIENT'

            office_df = partner_df
            office_y_val = partner_y_val

        partner_csv = convert_df(filtered_df[['UNPAID_INVOICE', 'CLIENT_PARTNER', 'CLIENT', 'OFFICE']].groupby(['CLIENT_PARTNER', 'CLIENT', 'OFFICE'], as_index=False).agg(OUTSTANDING_AR=('UNPAID_INVOICE', 'sum')).reset_index())

        partner_fig = bar(partner_df, x='OUTSTANDING_AR', y=partner_y_val, orientation='h', barmode='group', title='Firm AR by Client Partner', text='OUTSTANDING_AR').update_layout(h_bar_style).update_traces(texttemplate="%{value:$,.2f}")
        partner_visual.plotly_chart(partner_fig)
        partner_visual.download_button(
            label='Download this data',
            data=partner_csv,
            file_name='Outstanding AR by Client Partner.csv',
            key='AR_partner_visual_download'
        )
        partner_table.dataframe(filtered_df[['UNPAID_INVOICE', 'CLIENT_PARTNER', 'CLIENT', 'OFFICE']].groupby(['CLIENT_PARTNER', 'CLIENT', 'OFFICE'], as_index=False).agg(OUTSTANDING_AR=('UNPAID_INVOICE', 'sum')).reset_index()[['CLIENT_PARTNER', 'CLIENT', 'OFFICE', 'OUTSTANDING_AR']], use_container_width=True)
        partner_table.download_button(
            label='Download this data',
            data=partner_csv,
            file_name='Outstanding AR by Client Partner.csv',
            key='AR_partner_table_download'
        )

        office_csv = convert_df(filtered_df[['UNPAID_INVOICE', 'CLIENT_PARTNER', 'CLIENT', 'OFFICE']].groupby(['CLIENT_PARTNER', 'CLIENT', 'OFFICE'], as_index=False).agg(OUTSTANDING_AR=('UNPAID_INVOICE', 'sum')).reset_index())

        office_fig = bar(office_df, x='OUTSTANDING_AR', y=office_y_val, orientation='h', barmode='group', title='Firm AR by Client Office', text='OUTSTANDING_AR').update_layout(h_bar_style).update_traces(texttemplate="%{value:$,.2f}")
        office_visual.plotly_chart(office_fig)
        office_visual.download_button(
            label='Download this data',
            data=office_csv,
            file_name='Outstanding AR by Client Office.csv',
            key='AR_office_visual_download'
        )
        office_table.dataframe(filtered_df[['UNPAID_INVOICE', 'CLIENT_PARTNER', 'CLIENT', 'OFFICE']].groupby(['CLIENT_PARTNER', 'CLIENT', 'OFFICE'], as_index=False).agg(OUTSTANDING_AR=('UNPAID_INVOICE', 'sum')).reset_index()[['CLIENT_PARTNER', 'CLIENT', 'OFFICE', 'OUTSTANDING_AR']], use_container_width=True)
        office_table.download_button(
            label='Download this data',
            data=office_csv,
            file_name='Outstanding AR by Client Office.csv',
            key='AR_office_table_download'
        )
    
    except Exception as e:
        st.write(e)

    try:

        aging_df = get_rows("""SELECT SUM(AR.DEBTTRANUNPAID) AS UNPAID_INVOICE, 
            CP.STAFFNAME AS CLIENT_PARTNER, 
            A.NAME AS CLIENT, 
            CASE 
                WHEN C.OFFICE = 'BHM' THEN 'ATL'
                WHEN C.OFFICE = 'GAD' THEN 'LAS'
                WHEN C.OFFICE = 'HSV' THEN 'NYC'
                WHEN C.OFFICE = 'AO' THEN 'MPS'
                ELSE C.OFFICE
            END AS OFFICE,
            CASE WHEN D.AGING_PERIOD_SORT > 3 THEN 'Overdue AR'
                ELSE D.AGING_PERIOD
            END AS AGING_PERIOD
        from TRANS_AR AR
            INNER JOIN DIM_CLIENT_MASTER C ON C.ContIndex = AR.ContIndex 
            INNER JOIN CLIENT_BMSS_SANDBOX_DB.ANONYMOUS.DIM_CLIENT_ANONYMOUS A ON A.CONTIDX = C.CONTINDEX AND A.NAME IS NOT NULL
            INNER JOIN ANONYMOUS.DIM_STAFF_ANONYMOUS CP ON CP.STAFFIDX = C.CLIENT_PARTNER_IDX AND CP.STAFFNAME IS NOT NULL
            INNER JOIN DIM_DATES D ON D.CALENDAR_DATE = AR.DEBTTRANDATE
        WHERE AR.DEBTTRANUNPAID <> 0 AND AR.DEBTTRANTYPE IN (3, 6)
        GROUP BY CP.STAFFNAME, 
            A.NAME, 
            CASE 
                WHEN C.OFFICE = 'BHM' THEN 'ATL'
                WHEN C.OFFICE = 'GAD' THEN 'LAS'
                WHEN C.OFFICE = 'HSV' THEN 'NYC'
                WHEN C.OFFICE = 'AO' THEN 'MPS'
                ELSE C.OFFICE
            END,
            CASE WHEN D.AGING_PERIOD_SORT > 3 THEN 'Overdue AR'
                ELSE D.AGING_PERIOD
            END;""", st.session_state['today'])
        
        if partner_filter == 'All' and office_filter == 'All':
            filtered_df = aging_df.copy()

        elif partner_filter == 'All' and office_filter != 'All':
            filtered_df = aging_df[aging_df['OFFICE'] == office_filter].copy()
            
        elif partner_filter != 'All' and office_filter == 'All':
            filtered_df = aging_df[aging_df['CLIENT_PARTNER'] == partner_filter].copy()
            
        else:
            filtered_df = aging_df[(aging_df['CLIENT_PARTNER'] == partner_filter) & (aging_df['OFFICE'] == office_filter)]
            

        aging_AR = filtered_df[['AGING_PERIOD', 'UNPAID_INVOICE']]
        aging_AR = aging_AR.groupby('AGING_PERIOD', as_index=False).agg(OUTSTANDING_AR=('UNPAID_INVOICE', 'sum')).reset_index()

        aging_csv = convert_df(filtered_df[['UNPAID_INVOICE', 'CLIENT_PARTNER', 'CLIENT', 'OFFICE', 'AGING_PERIOD']].groupby(['CLIENT_PARTNER', 'CLIENT', 'OFFICE', 'AGING_PERIOD'], as_index=False).agg(OUTSTANDING_AR=('UNPAID_INVOICE', 'sum')).reset_index()[['CLIENT_PARTNER', 'CLIENT', 'OFFICE', 'AGING_PERIOD', 'OUTSTANDING_AR']])

        aging_fig = pie(aging_AR, values='OUTSTANDING_AR', names='AGING_PERIOD', title='AR Aging Periods').update_layout(pie_style)
        aging_visual.plotly_chart(aging_fig)
        aging_visual.download_button(
            label='Download this data',
            data=aging_csv,
            file_name='Aging AR.csv',
            key='AR_aging_visual_download'
        )

        aging_table.dataframe(filtered_df[['UNPAID_INVOICE', 'CLIENT_PARTNER', 'CLIENT', 'OFFICE', 'AGING_PERIOD']].groupby(['CLIENT_PARTNER', 'CLIENT', 'OFFICE', 'AGING_PERIOD'], as_index=False).agg(OUTSTANDING_AR=('UNPAID_INVOICE', 'sum')).reset_index()[['CLIENT_PARTNER', 'CLIENT', 'OFFICE', 'AGING_PERIOD', 'OUTSTANDING_AR']], use_container_width=True)
        aging_table.download_button(
            label='Download this data',
            data=aging_csv,
            file_name='Aging AR.csv',
            key='AR_aging_table_download'
        )

        current_csv = convert_df(filtered_df[['UNPAID_INVOICE', 'CLIENT_PARTNER', 'CLIENT', 'OFFICE']].groupby(['CLIENT_PARTNER', 'CLIENT', 'OFFICE'], as_index=False).agg(OUTSTANDING_AR=('UNPAID_INVOICE', 'sum')).reset_index())

        filtered_df['CURRENTAR'] = where(filtered_df['AGING_PERIOD'] == '0-30 Days', filtered_df['UNPAID_INVOICE'], 0)
        filtered_df['30_TO_60'] = where(filtered_df['AGING_PERIOD'] == '31-60 Days', filtered_df['UNPAID_INVOICE'], 0)
        filtered_df['60_TO_90'] = where(filtered_df['AGING_PERIOD'] == '61-90 Days', filtered_df['UNPAID_INVOICE'], 0)
        filtered_df['OVERDUEAR'] = where(filtered_df['AGING_PERIOD'] == 'Overdue AR', filtered_df['UNPAID_INVOICE'], 0)

        current_df = filtered_df[['UNPAID_INVOICE', 'CURRENTAR', 'OFFICE']]
        current_df = current_df.groupby(['OFFICE']).agg(CURRENT_AR= ('CURRENTAR', 'sum'), OUTSTANDING_AR=('UNPAID_INVOICE', 'sum')).reset_index()
        current_df['PERCENT_CURRENT'] = round((current_df['CURRENT_AR'] / current_df['OUTSTANDING_AR']) * 100, 2)
        current_y_val = 'OFFICE'

        current_fig = bar(current_df, x='PERCENT_CURRENT', y=current_y_val, orientation='h', barmode='group', title='Percent Current AR by Client Office', text='PERCENT_CURRENT').update_layout(h_bar_style).update_traces(texttemplate="%{value:.2f}%")
        current_visual.plotly_chart(current_fig)
        current_visual.download_button(
            label='Download this data',
            data=current_csv,
            file_name='Percentage Current AR by Client Office.csv',
            key='AR_current_visual_download'
        )
        current_table.dataframe(filtered_df[['UNPAID_INVOICE', 'CLIENT_PARTNER', 'CLIENT', 'OFFICE']].groupby(['CLIENT_PARTNER', 'CLIENT', 'OFFICE'], as_index=False).agg(OUTSTANDING_AR=('UNPAID_INVOICE', 'sum')).reset_index()[['CLIENT_PARTNER', 'CLIENT', 'OFFICE', 'OUTSTANDING_AR']], use_container_width=True)
        current_table.download_button(
            label='Download this data',
            data=current_csv,
            file_name='Percentage Current AR by Client Office.csv',
            key='AR_current_table_download'
        )

        filtered_outstanding_AR = round(filtered_df['UNPAID_INVOICE'].sum(), 2)
        filtered_percent_current = round((filtered_df['CURRENTAR'].sum() / filtered_outstanding_AR) * 100, 2)
        filtered_AR_30_60 = round((filtered_df['30_TO_60'].sum() / filtered_outstanding_AR) * 100, 2)
        filtered_AR_60_90 = round((filtered_df['60_TO_90'].sum() / filtered_outstanding_AR) * 100, 2)
        filtered_overdue_AR = round((filtered_df['OVERDUEAR'].sum() / filtered_outstanding_AR) * 100, 2)

        dynamic_one.metric(label='Target < $4M', value='${:,.2f}'.format(filtered_outstanding_AR), delta=('Outstanding AR' if filtered_outstanding_AR < 4000000 else '-Outstanding AR'))
        dynamic_two.metric(label='Target > 70%', value='{:.2f}%'.format(filtered_percent_current), delta=('% AR in Current' if filtered_percent_current > 70 else '-% AR in Current'))
        dynamic_three.metric(label='Target < 20%', value='{:.2f}%'.format(filtered_AR_30_60), delta=('% AR in 31-60 Days' if filtered_AR_30_60 < 20 else '-% AR in 31-60 Days'))
        dynamic_four.metric(label='Target < 15%', value='{:.2f}%'.format(filtered_AR_60_90), delta=('% AR in 61-90 Days' if filtered_AR_60_90 < 15 else '-% AR in 61-90 Days'))
        dynamic_five.metric(label='Target < 5%', value='{:.2f}%'.format(filtered_overdue_AR), delta=('% AR over 90 Days' if filtered_overdue_AR < 5 else '-% AR over 90 Days'))

        go_to_top(st.markdown)
    except Exception as e:
        st.write(e)